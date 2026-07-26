"""The enforcement layer: core's validate.py, repointed at the knowledge base.

These tests exist because a lint that has only ever passed is not known to work.
Each rule gets a string that must trip it.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import DEPLOYMENT_ROOT

VALIDATE = DEPLOYMENT_ROOT / "enforcement" / "validate.py"
RULES = DEPLOYMENT_ROOT / "enforcement" / "rules.json"
PUBLIC = sorted((DEPLOYMENT_ROOT / "knowledge" / "public").glob("*.md"))


def run_validator(path: Path):
    proc = subprocess.run(
        [sys.executable, str(VALIDATE), str(path), "--rules", str(RULES), "--json"],
        capture_output=True, text=True,
    )
    return proc.returncode, json.loads(proc.stdout)


def test_validator_and_rules_exist():
    assert VALIDATE.exists(), "core validate.py must be present in enforcement/"
    assert RULES.exists()


def test_validator_is_unmodified_copy_of_core():
    """We reuse core's validator rather than forking it. A drifted copy means the
    deployment is no longer running the scaffold's enforcement."""
    core = DEPLOYMENT_ROOT.parents[1] / "core" / "enforcement" / "validate.py"
    assert core.exists(), "core validator not found — check repo layout"
    assert VALIDATE.read_bytes() == core.read_bytes(), (
        "enforcement/validate.py has drifted from core/enforcement/validate.py"
    )


@pytest.mark.parametrize("path", PUBLIC, ids=lambda p: p.name)
def test_public_knowledge_passes_lint(path):
    code, payload = run_validator(path)
    assert code == 0, f"{path.name} blocked: {payload['failures']}"


def test_every_public_file_is_covered():
    assert len(PUBLIC) == 6, "expected six public knowledge files"


# --------------------------------------------------------------------------- #
# Each rule must be shown to fire.
# --------------------------------------------------------------------------- #

VIOLATIONS = [
    ("FACT-001", "A file with no fact citation at all."),
    ("NAME-001", "[ALT-001] Your manager will meet you."),
    ("ROUTE-001", "[ALT-001] Ask HR about that."),
    ("PROMISE-001", "[ALT-001] You'll receive a laptop."),
    ("GENERIC-001", "[ALT-001] Typically your first week is orientation."),
    ("TOOL-001", "[ALT-001] Everything lives in Confluence."),
    ("COMPETITOR-001", "[ALT-001] Advisors switch from Schwab."),
    ("ASSURE-001", "[ALT-001] Client data is fully secure."),
]


@pytest.mark.parametrize("rule_id,text", VIOLATIONS, ids=[r for r, _ in VIOLATIONS])
def test_rule_fires(rule_id, text, tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text(text, encoding="utf-8")
    code, payload = run_validator(bad)
    assert code == 1, f"{rule_id} did not block"
    assert any(rule_id in f for f in payload["failures"]), (
        f"{rule_id} did not fire; got {payload['failures']}"
    )


def test_all_declared_rules_have_a_firing_test():
    """Coverage guard: adding a rule without a test that trips it is how a rule
    silently stops working."""
    declared = {r["id"] for r in json.loads(RULES.read_text())["rules"]}
    tested = {rid for rid, _ in VIOLATIONS}
    assert declared == tested, f"untested rules: {declared - tested}"


def test_every_rule_cites_its_knowledge_source():
    """core's convention: each rule traces to the knowledge line it enforces."""
    for rule in json.loads(RULES.read_text())["rules"]:
        assert rule.get("source", "").strip(), f"{rule['id']} has no source"
        assert rule.get("severity") == "block"
