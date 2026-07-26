"""The checks.

Scope discipline, stated up front: these validate the agent's *declared knowledge and
boundaries at build time*. They do not inspect a live conversation and cannot tell you
whether a given answer was safe. The audit established why — this agent's output is
conversational, so there is no pre-send artifact to gate, and its dominant failure mode
is knowledge-borne rather than phrasing-borne. Runtime safety rests on absence of access
(see tools/access-policy.md). See docs/test-strategy.md gap TG-01.
"""

from __future__ import annotations

import datetime as _dt
import re
from typing import Any, Callable

from .loaders import Deployment
from .model import Finding, block, warn

# Bracketed [ALT-123] in prose = a citation of an answerable fact.
# Bare ALT-Q12 in prose = a reference to a quarantined claim.
# The two forms are deliberately distinct so prose can name a quarantined claim
# (to say it is NOT answerable) without that reading as a citation.
CITATION_RE = re.compile(r"\[ALT-(\d{3})\]")
QUARANTINE_REF_RE = re.compile(r"\bALT-Q(\d{2})\b")

VALID_TIERS = {"P1", "P2", "P3"}
VALID_DISPOSITIONS = {"refuse", "answer"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
STALENESS_DAYS = 180

REQUIRED_FACT_FIELDS = ("id", "topic", "statement", "tier", "sources", "checked", "external_verified")
REQUIRED_QUARANTINE_FIELDS = ("id", "topic", "claim", "sources", "reason", "priority")
REQUIRED_BOUNDARY_FIELDS = ("id", "topic", "disposition", "description", "source", "triggers")


# --------------------------------------------------------------------------- #
# Fact base
# --------------------------------------------------------------------------- #

def check_factbase(dep: Deployment, today: _dt.date) -> list[Finding]:
    out: list[Finding] = []
    seen: set[str] = set()
    declared_docs = set(dep.documents)

    for fact in dep.facts:
        fid = fact.get("id", "<no id>")
        loc = f"factbase.json:{fid}"

        missing = [f for f in REQUIRED_FACT_FIELDS if f not in fact]
        if missing:
            out.append(block("FB001", f"fact missing required field(s): {', '.join(missing)}", loc))
            continue

        if fid in seen:
            out.append(block("FB004", f"duplicate id {fid}", loc))
        seen.add(fid)

        tier = fact["tier"]
        if tier not in VALID_TIERS:
            out.append(block("FB002", f"invalid tier {tier!r} (expected one of {sorted(VALID_TIERS)})", loc))
            continue

        sources = fact["sources"]
        if not isinstance(sources, list) or not sources:
            out.append(block("FB005", "sources must be a non-empty list", loc))
            continue

        unknown = [s for s in sources if s not in declared_docs]
        if unknown:
            out.append(block("FB005", f"sources reference undeclared document(s): {', '.join(unknown)}", loc))

        # The central safety invariant. new-agent.md carries no authority: it may put a
        # claim into quarantine, never into the answerable set. If this ever fires, an
        # unverified claim from the old plan has been promoted without verification.
        if "PLAN" in sources:
            out.append(block(
                "FB007",
                "answerable fact lists PLAN (new-agent.md) as a source. PLAN has no authority; "
                "it may appear in corroborated_by only. Move this fact to quarantine or find a real source.",
                loc,
            ))

        if tier == "P1" and "PACK" not in sources:
            out.append(block("FB008", "tier P1 requires PACK in sources", loc))
        if tier in ("P2", "P3") and "SEC" not in sources:
            out.append(block("FB009", f"tier {tier} requires SEC in sources", loc))

        if fact.get("sensitive") and not str(fact.get("attribution", "")).strip():
            out.append(block(
                "FB006",
                "fact is marked sensitive but has no attribution string; sensitive facts "
                "cannot be stated without their mandatory framing",
                loc,
            ))

        if fact.get("external_verified") is True and not str(fact.get("external_source", "")).strip():
            out.append(block(
                "FB013",
                "fact claims external_verified=true but records no external_source",
                loc,
            ))

        out.extend(_check_date(fact.get("checked"), today, loc))

    out.extend(_check_quarantine(dep, seen))
    return out


def _check_date(raw: Any, today: _dt.date, loc: str) -> list[Finding]:
    try:
        checked = _dt.date.fromisoformat(str(raw))
    except (TypeError, ValueError):
        return [block("FB003", f"checked date {raw!r} is not an ISO date (YYYY-MM-DD)", loc)]

    if checked > today:
        return [block("FB003", f"checked date {checked} is in the future", loc)]

    age = (today - checked).days
    if age > STALENESS_DAYS:
        # Keep inspection non-blocking for maintainers; the release gate runs --strict
        # and promotes this warning to a blocking freshness failure.
        return [warn("FB010", f"fact last checked {age} days ago (window {STALENESS_DAYS})", loc)]
    return []


def _check_quarantine(dep: Deployment, fact_ids: set[str]) -> list[Finding]:
    out: list[Finding] = []
    seen: set[str] = set()

    for entry in dep.quarantine:
        qid = entry.get("id", "<no id>")
        loc = f"factbase.json:quarantine:{qid}"

        missing = [f for f in REQUIRED_QUARANTINE_FIELDS if f not in entry]
        if missing:
            out.append(block("FB011", f"quarantine entry missing field(s): {', '.join(missing)}", loc))
            continue

        if qid in seen or qid in fact_ids:
            out.append(block("FB004", f"duplicate id {qid}", loc))
        seen.add(qid)

        if entry["priority"] not in VALID_PRIORITIES:
            out.append(block(
                "FB011",
                f"invalid priority {entry['priority']!r} (expected one of {sorted(VALID_PRIORITIES)})",
                loc,
            ))
    return out


# --------------------------------------------------------------------------- #
# Citations in prose
# --------------------------------------------------------------------------- #

def _display_path(path: Any, root: Any) -> str:
    """Path for a finding message, relative to the deployment where possible.

    Falls back to the raw path rather than raising: a reporting convenience must
    never be able to crash the check that produces the finding.
    """
    try:
        return str(path.relative_to(root))
    except (ValueError, AttributeError):
        return str(path)


def check_citations(dep: Deployment) -> list[Finding]:
    out: list[Finding] = []
    answerable = {f["id"] for f in dep.facts if "id" in f}
    quarantined = {q["id"] for q in dep.quarantine if "id" in q}
    cited: set[str] = set()

    for path, text in dep.prose.items():
        rel = _display_path(path, dep.root)

        for m in CITATION_RE.finditer(text):
            fid = f"ALT-{m.group(1)}"
            cited.add(fid)
            if fid in answerable:
                continue
            if fid in quarantined:
                out.append(block(
                    "CI002",
                    f"prose cites {fid} as an answerable fact, but it is quarantined",
                    str(rel),
                ))
            else:
                out.append(block("CI001", f"prose cites unknown fact {fid}", str(rel)))

        for m in QUARANTINE_REF_RE.finditer(text):
            qid = f"ALT-Q{m.group(1)}"
            if qid not in quarantined:
                out.append(block(
                    "CI003",
                    f"prose references {qid} but no such quarantine entry exists",
                    str(rel),
                ))

    for fid in sorted(answerable - cited):
        out.append(warn(
            "CI004",
            f"fact {fid} is answerable but never cited in knowledge/public/ — "
            "it may be unreachable to the agent in practice",
            "factbase.json",
        ))
    return out


# --------------------------------------------------------------------------- #
# Boundaries
# --------------------------------------------------------------------------- #

def check_boundaries(dep: Deployment) -> list[Finding]:
    out: list[Finding] = []
    seen: set[str] = set()

    for b in dep.boundary_list:
        bid = b.get("id", "<no id>")
        loc = f"boundaries.json:{bid}"

        missing = [f for f in REQUIRED_BOUNDARY_FIELDS if f not in b]
        if missing:
            out.append(block("BD003", f"boundary missing field(s): {', '.join(missing)}", loc))
            continue

        if bid in seen:
            out.append(block("BD001", f"duplicate boundary id {bid}", loc))
        seen.add(bid)

        if b["disposition"] not in VALID_DISPOSITIONS:
            out.append(block("BD005", f"invalid disposition {b['disposition']!r}", loc))

        if not b["triggers"]:
            out.append(block("BD003", "boundary has no triggers; eval coverage cannot exercise it", loc))

        slot = b.get("route_slot")
        if slot and not (dep.root / slot).exists():
            # A route pointing at a file that does not exist sends the hire nowhere.
            out.append(block("BD002", f"route_slot does not exist on disk: {slot}", loc))

    out.extend(_check_topic_coverage(dep))
    return out


def _check_topic_coverage(dep: Deployment) -> list[Finding]:
    """Every topic carrying an answerable fact must be declared answerable.

    Catches the silent case where a fact is added under a topic the boundary layer
    never sanctioned — the fact becomes stateable with no boundary reasoning behind it.
    """
    declared = set(dep.answerable_topics)
    out: list[Finding] = []
    for topic in sorted({f.get("topic", "") for f in dep.facts if f.get("topic")}):
        if topic not in declared:
            out.append(block(
                "BD004",
                f"topic {topic!r} carries answerable facts but is not in boundaries.json answerable_topics",
                "boundaries.json",
            ))
    return out


# --------------------------------------------------------------------------- #
# Eval suite
# --------------------------------------------------------------------------- #

MIN_MUST_REFUSE = 20  # audit ship gate


def check_eval_suite(dep: Deployment) -> list[Finding]:
    out: list[Finding] = []
    boundary_ids = {b["id"] for b in dep.boundary_list if "id" in b}
    answerable = {f["id"]: f for f in dep.facts if "id" in f}
    seen: set[str] = set()
    covered: set[str] = set()
    refuse_count = 0

    for case in dep.cases:
        cid = case.get("id", "<no id>")
        loc = f"refusal-suite.json:{cid}"

        if cid in seen:
            out.append(block("EV001", f"duplicate case id {cid}", loc))
        seen.add(cid)

        expect = case.get("expect")
        if expect == "must_refuse":
            refuse_count += 1
            bid = case.get("boundary")
            if not bid:
                out.append(block("EV002", "must_refuse case declares no boundary", loc))
            elif bid not in boundary_ids:
                out.append(block("EV002", f"case references unknown boundary {bid}", loc))
            else:
                covered.add(bid)

        elif expect in ("must_answer", "must_answer_with_attribution"):
            facts = case.get("facts", [])
            for fid in facts:
                if fid not in answerable:
                    out.append(block(
                        "EV004",
                        f"case expects an answer using {fid}, which is not an answerable fact",
                        loc,
                    ))
            if expect == "must_answer_with_attribution":
                needs = [
                    fid for fid in facts
                    if fid in answerable
                    and (answerable[fid].get("sensitive") or answerable[fid].get("tier") == "P3")
                ]
                if not needs:
                    out.append(block(
                        "EV005",
                        "case demands attribution but cites no P3 or sensitive fact — "
                        "nothing requires the attribution wrapper",
                        loc,
                    ))
        else:
            out.append(block("EV007", f"unknown expect value {expect!r}", loc))

    if refuse_count < MIN_MUST_REFUSE:
        out.append(block(
            "EV006",
            f"only {refuse_count} must_refuse cases; ship gate requires at least {MIN_MUST_REFUSE}",
            "refusal-suite.json",
        ))

    for bid in sorted(boundary_ids - covered):
        out.append(block(
            "EV003",
            f"boundary {bid} has no must_refuse case; it is declared but never tested",
            "refusal-suite.json",
        ))
    return out


# --------------------------------------------------------------------------- #
# Source registry drift
# --------------------------------------------------------------------------- #

_TIER_ROW_RE = re.compile(r"^\|\s*(P1|P2|P3)\s*\|\s*(\d+)\s*\|", re.MULTILINE)
_TOTAL_ROW_RE = re.compile(r"^\|\s*\*\*Answerable total\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|", re.MULTILINE)
_QUARANTINE_ROW_RE = re.compile(r"^\|\s*Quarantined\s*\|\s*(\d+)\s*\|", re.MULTILINE)


def check_source_registry(dep: Deployment) -> list[Finding]:
    """The registry publishes counts. Prove they still match the fact base.

    A human-written summary of a machine-readable file drifts the moment someone
    edits one and not the other. This is the cheapest possible guard against the
    system making an unverified claim about itself.
    """
    path = dep.root / "knowledge" / "source-registry.md"
    if not path.exists():
        return [block("RG001", "source-registry.md is missing", "knowledge/")]

    text = path.read_text(encoding="utf-8")
    actual = {t: sum(1 for f in dep.facts if f.get("tier") == t) for t in VALID_TIERS}
    out: list[Finding] = []
    claimed_tiers: dict[str, int] = {}

    for tier, count in _TIER_ROW_RE.findall(text):
        claimed_tiers[tier] = int(count)

    if not claimed_tiers:
        return [block("RG001", "source-registry.md publishes no tier counts to verify", "source-registry.md")]

    for tier, claimed in sorted(claimed_tiers.items()):
        if claimed != actual[tier]:
            out.append(block(
                "RG001",
                f"registry claims {claimed} {tier} facts, fact base has {actual[tier]}",
                "source-registry.md",
            ))

    total_match = _TOTAL_ROW_RE.search(text)
    if total_match and int(total_match.group(1)) != len(dep.facts):
        out.append(block(
            "RG001",
            f"registry claims {total_match.group(1)} answerable facts, fact base has {len(dep.facts)}",
            "source-registry.md",
        ))

    q_match = _QUARANTINE_ROW_RE.search(text)
    if q_match and int(q_match.group(1)) != len(dep.quarantine):
        out.append(block(
            "RG001",
            f"registry claims {q_match.group(1)} quarantined claims, fact base has {len(dep.quarantine)}",
            "source-registry.md",
        ))
    return out


# --------------------------------------------------------------------------- #

CHECKS: tuple[Callable[..., list[Finding]], ...] = (
    check_factbase,
    check_citations,
    check_boundaries,
    check_eval_suite,
    check_source_registry,
)


def run_all(dep: Deployment, today: _dt.date | None = None) -> list[Finding]:
    today = today or _dt.date.today()
    findings: list[Finding] = []
    findings.extend(check_factbase(dep, today))
    findings.extend(check_citations(dep))
    findings.extend(check_boundaries(dep))
    findings.extend(check_eval_suite(dep))
    findings.extend(check_source_registry(dep))
    return findings
