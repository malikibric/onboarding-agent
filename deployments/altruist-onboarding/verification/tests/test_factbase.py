"""Fact base integrity — including the invariant the whole design rests on."""

from __future__ import annotations

import datetime as _dt

from agentcheck.checks import check_factbase
from conftest import TODAY, blocking_codes


def test_real_factbase_is_clean(real):
    assert blocking_codes(check_factbase(real, TODAY)) == set()


# --------------------------------------------------------------------------- #
# The central safety invariant
# --------------------------------------------------------------------------- #

def test_plan_sourced_fact_is_rejected(dep):
    """new-agent.md must never be able to make a claim answerable.

    This is the audit's core finding rendered as a test. If someone promotes a
    quarantined claim by adding PLAN as its source, the build must stop.
    """
    dep.facts[0]["sources"] = ["PLAN"]
    assert "FB007" in blocking_codes(check_factbase(dep, TODAY))


def test_plan_as_secondary_source_still_rejected(dep):
    """PLAN alongside a real source is still PLAN. No laundering."""
    dep.facts[0]["sources"] = ["PACK", "PLAN"]
    assert "FB007" in blocking_codes(check_factbase(dep, TODAY))


def test_plan_in_corroborated_by_is_allowed(real):
    """PLAN may corroborate — it just carries no authority."""
    corroborated = [f for f in real.facts if "PLAN" in f.get("corroborated_by", [])]
    assert corroborated, "expected some facts corroborated by PLAN"
    assert "FB007" not in blocking_codes(check_factbase(real, TODAY))


# --------------------------------------------------------------------------- #
# Field and tier integrity
# --------------------------------------------------------------------------- #

def test_missing_required_field_is_rejected(dep):
    del dep.facts[0]["checked"]
    assert "FB001" in blocking_codes(check_factbase(dep, TODAY))


def test_invalid_tier_is_rejected(dep):
    dep.facts[0]["tier"] = "A"
    assert "FB002" in blocking_codes(check_factbase(dep, TODAY))


def test_duplicate_id_is_rejected(dep):
    dep.facts[1]["id"] = dep.facts[0]["id"]
    assert "FB004" in blocking_codes(check_factbase(dep, TODAY))


def test_id_colliding_with_quarantine_is_rejected(dep):
    dep.quarantine[0]["id"] = dep.facts[0]["id"]
    assert "FB004" in blocking_codes(check_factbase(dep, TODAY))


def test_undeclared_source_document_is_rejected(dep):
    dep.facts[0]["sources"] = ["WIKIPEDIA"]
    assert "FB005" in blocking_codes(check_factbase(dep, TODAY))


def test_empty_sources_is_rejected(dep):
    dep.facts[0]["sources"] = []
    assert "FB005" in blocking_codes(check_factbase(dep, TODAY))


def test_p1_without_pack_is_rejected(dep):
    fact = next(f for f in dep.facts if f["tier"] == "P1")
    fact["sources"] = ["SEC"]
    assert "FB008" in blocking_codes(check_factbase(dep, TODAY))


def test_p3_without_sec_is_rejected(dep):
    fact = next(f for f in dep.facts if f["tier"] == "P3")
    fact["sources"] = ["PACK"]
    assert "FB009" in blocking_codes(check_factbase(dep, TODAY))


# --------------------------------------------------------------------------- #
# Sensitive facts
# --------------------------------------------------------------------------- #

def test_sensitive_fact_without_attribution_is_rejected(dep):
    """A sensitive fact with no attribution can be stated bare. That is the
    exact failure the Hazel security messaging case exists to prevent."""
    fact = next(f for f in dep.facts if f.get("sensitive"))
    fact["attribution"] = "   "
    assert "FB006" in blocking_codes(check_factbase(dep, TODAY))


def test_all_sensitive_facts_currently_have_attribution(real):
    sensitive = [f for f in real.facts if f.get("sensitive")]
    assert len(sensitive) >= 4, "expected the known sensitive facts to be present"
    for fact in sensitive:
        assert fact.get("attribution", "").strip(), f"{fact['id']} is sensitive with no attribution"


def test_known_sensitive_facts_are_marked(real):
    """Regression guard: these four were identified in the audit as requiring
    mandatory attribution. Silently unmarking one is a safety regression."""
    marked = {f["id"] for f in real.facts if f.get("sensitive")}
    for fid in ("ALT-011", "ALT-027", "ALT-028", "ALT-031"):
        assert fid in marked, f"{fid} must remain marked sensitive"


# --------------------------------------------------------------------------- #
# Dates
# --------------------------------------------------------------------------- #

def test_malformed_date_is_rejected(dep):
    dep.facts[0]["checked"] = "July 2026"
    assert "FB003" in blocking_codes(check_factbase(dep, TODAY))


def test_future_date_is_rejected(dep):
    dep.facts[0]["checked"] = "2027-01-01"
    assert "FB003" in blocking_codes(check_factbase(dep, TODAY))


def test_stale_fact_warns_but_does_not_block(dep):
    dep.facts[0]["checked"] = "2020-01-01"
    findings = check_factbase(dep, TODAY)
    assert "FB010" in {f.code for f in findings}
    assert "FB010" not in blocking_codes(findings)


def test_external_verified_without_source_is_rejected(dep):
    """Claiming verification without recording what verified it is the exact
    unearned-confidence pattern this system is built to refuse."""
    dep.facts[0]["external_verified"] = True
    assert "FB013" in blocking_codes(check_factbase(dep, TODAY))


def test_nothing_currently_claims_external_verification(real):
    """Honesty check on the delivery itself: no fact in this system has been
    verified against a resolvable external source, and none may claim to be."""
    assert all(f.get("external_verified") is False for f in real.facts)


# --------------------------------------------------------------------------- #
# Quarantine
# --------------------------------------------------------------------------- #

def test_quarantine_missing_field_is_rejected(dep):
    del dep.quarantine[0]["priority"]
    assert "FB011" in blocking_codes(check_factbase(dep, TODAY))


def test_quarantine_invalid_priority_is_rejected(dep):
    dep.quarantine[0]["priority"] = "urgent"
    assert "FB011" in blocking_codes(check_factbase(dep, TODAY))


def test_regulatory_claims_remain_quarantined(real):
    """The audit's highest-blast-radius findings. If any of these becomes
    answerable without external verification, the agent can tell a new hire
    something about entity structure or coverage that nobody has confirmed."""
    quarantined = {q["id"] for q in real.quarantine}
    for qid in ("ALT-Q03", "ALT-Q04", "ALT-Q05", "ALT-Q06"):
        assert qid in quarantined, f"{qid} must remain quarantined"

    critical = {q["id"] for q in real.quarantine if q["priority"] == "critical"}
    assert critical == {"ALT-Q03", "ALT-Q04", "ALT-Q05", "ALT-Q06"}
