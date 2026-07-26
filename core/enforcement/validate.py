#!/usr/bin/env python3
"""
Pre-release validator. Checks an agent's output against hard rules before it ships.

The point: these rules do not depend on the model deciding to follow them.
Exit 0 = clear to send. Exit 1 = blocked.

Usage:
    python validate.py output.txt --rules rules.json
    python validate.py output.txt --rules rules.json --json
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_amount(raw):
    """Parse a number in US (61,450.00) or European (61.450,00 / 61 450,00) format.

    A single separator followed by exactly three digits is read as grouping,
    so an ambiguous "61.450" becomes 61450, not 61.45 — a threshold check
    must over-read before it under-reads. Anything it can't classify raises,
    and the caller fails the rule closed.
    """
    s = raw.strip().replace(" ", "").rstrip(".,")
    if "," in s and "." in s:
        dec = max(s.rfind(","), s.rfind("."))
        whole = s[:dec].replace(",", "").replace(".", "")
        frac = s[dec + 1:]
        if not (whole.isdigit() and frac.isdigit()):
            raise ValueError(f"ambiguous number: {raw!r}")
        return float(whole + "." + frac)
    if "," in s or "." in s:
        sep = "," if "," in s else "."
        parts = s.split(sep)
        if len(parts) == 2 and parts[1] and (len(parts[1]) != 3 or parts[0] in ("", "0")):
            return float((parts[0] or "0") + "." + parts[1])
        if all(p.isdigit() and len(p) == 3 for p in parts[1:]) and parts[0].isdigit() and parts[0] != "0":
            return float("".join(parts))  # grouping: 61.450 or 1.234.567
        raise ValueError(f"ambiguous number: {raw!r}")
    return float(s)


def check_required(text, rule):
    """Something that must be present."""
    found = re.search(rule["pattern"], text, re.IGNORECASE | re.MULTILINE)
    return bool(found), None if found else f"missing: {rule['description']}"


def check_forbidden(text, rule):
    """Something that must never appear."""
    found = re.search(rule["pattern"], text, re.IGNORECASE | re.MULTILINE)
    if found:
        return False, f"forbidden content present: {rule['description']} -> '{found.group(0)[:60]}'"
    return True, None


def check_threshold(text, rule):
    """A numeric value that must stay under a limit — escalation triggers."""
    matches = re.findall(rule["pattern"], text, re.IGNORECASE)
    if not matches:
        # No value found is not the same as a value under the limit.
        return True, f"no value matched — {rule['description']} not verified"
    for m in matches:
        value = parse_amount(m if isinstance(m, str) else m[0])
        if value > rule["max"]:
            return False, (
                f"{rule['description']}: found {value:,.2f}, "
                f"limit {rule['max']:,.2f} — requires {rule.get('escalate_to', 'human approval')}"
            )
    return True, None


CHECKS = {
    "required": check_required,
    "forbidden": check_forbidden,
    "threshold": check_threshold,
}


def validate(text, rules):
    failures, warnings = [], []

    for rule in rules:
        rule_id = rule.get("id", "?")
        check = CHECKS.get(rule.get("type"))
        if not check:
            warnings.append(f"[{rule_id}] unknown rule type '{rule.get('type')}' — skipped")
            continue

        try:
            passed, message = check(text, rule)
        except Exception as e:
            # A rule that can't run is a failure, not a pass. Fail closed.
            failures.append(f"[{rule_id}] rule could not be evaluated: {e}")
            continue

        if not passed:
            (failures if rule.get("severity", "block") == "block" else warnings).append(
                f"[{rule_id}] {message}"
            )
        elif message:
            warnings.append(f"[{rule_id}] {message}")

    return failures, warnings


def report(failures, warnings, as_json):
    if as_json:
        print(json.dumps({
            "passed": not failures,
            "failures": failures,
            "warnings": warnings,
        }, indent=2))
    else:
        if failures:
            print("BLOCKED — not cleared to send\n")
            for f in failures:
                print(f"  ✗ {f}")
        else:
            print("PASSED — cleared to send")
        if warnings:
            print("\nWarnings (not blocking):")
            for w in warnings:
                print(f"  ! {w}")
    sys.exit(1 if failures else 0)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("output", help="file containing the agent's output")
    p.add_argument("--rules", required=True, help="rules JSON")
    p.add_argument("--json", action="store_true", help="machine-readable result")
    args = p.parse_args()

    try:
        text = Path(args.output).read_text(encoding="utf-8")
    except OSError as e:
        report([f"could not read output file: {e}"], [], args.json)
    try:
        rules = json.loads(Path(args.rules).read_text(encoding="utf-8"))["rules"]
        if not isinstance(rules, list):
            raise ValueError('"rules" must be a list')
    except (OSError, ValueError, KeyError, TypeError) as e:
        report([f"could not load rules: {e}"], [], args.json)

    failures, warnings = validate(text, rules)
    report(failures, warnings, args.json)


if __name__ == "__main__":
    main()
