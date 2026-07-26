"""Citation resolution, boundary integrity, and topic coverage."""

from __future__ import annotations

from pathlib import Path

from agentcheck.checks import check_boundaries, check_citations
from conftest import blocking_codes


# --------------------------------------------------------------------------- #
# Citations
# --------------------------------------------------------------------------- #

def test_real_citations_are_clean(real):
    assert blocking_codes(check_citations(real)) == set()


def test_unknown_fact_citation_is_rejected(dep):
    path = next(iter(dep.prose))
    dep.prose = {path: "Altruist does a thing. [ALT-999]"}
    assert "CI001" in blocking_codes(check_citations(dep))


def test_citing_a_quarantined_claim_as_fact_is_rejected(dep):
    """The bracketed form means 'answerable'. Using it for a quarantined claim
    is how an unverified regulatory detail would leak into prose."""
    path = next(iter(dep.prose))
    dep.prose = {path: "Altruist has four legal entities. [ALT-003]"}
    dep.factbase["quarantine"].append({
        "id": "ALT-003", "topic": "x", "claim": "y",
        "sources": ["PLAN"], "reason": "z", "priority": "low",
    })
    dep.factbase["facts"] = [f for f in dep.facts if f["id"] != "ALT-003"]
    assert "CI002" in blocking_codes(check_citations(dep))


def test_dangling_quarantine_reference_is_rejected(dep):
    path = next(iter(dep.prose))
    dep.prose = {path: "Not answerable: see ALT-Q99."}
    assert "CI003" in blocking_codes(check_citations(dep))


def test_bare_quarantine_reference_is_not_treated_as_a_citation(real):
    """Prose must be able to name a quarantined claim in order to say it is NOT
    answerable. The two citation forms exist precisely to allow this."""
    findings = check_citations(real)
    assert not [f for f in findings if f.code in ("CI001", "CI002")]
    joined = "".join(real.prose.values())
    assert "ALT-Q" in joined, "expected prose to reference quarantined claims explicitly"


def test_uncited_fact_warns_only(dep):
    dep.prose = {Path("stub.md"): "No citations here."}
    findings = check_citations(dep)
    assert "CI004" in {f.code for f in findings}
    assert "CI004" not in blocking_codes(findings)


# --------------------------------------------------------------------------- #
# Boundaries
# --------------------------------------------------------------------------- #

def test_real_boundaries_are_clean(real):
    assert blocking_codes(check_boundaries(real)) == set()


def test_route_slot_must_exist_on_disk(dep):
    """A refusal that routes the hire to a file that does not exist sends them
    nowhere, which is worse than saying 'I don't know'."""
    dep.boundary_list[0]["route_slot"] = "knowledge/internal/99-does-not-exist.md"
    assert "BD002" in blocking_codes(check_boundaries(dep))


def test_all_route_slots_currently_resolve(real):
    slots = [b["route_slot"] for b in real.boundary_list if b.get("route_slot")]
    assert slots, "expected boundaries to route somewhere"
    for slot in slots:
        assert (real.root / slot).exists(), f"route_slot missing: {slot}"


def test_null_route_slot_is_allowed(real):
    """Some boundaries legitimately have nowhere internal to route — financial
    advice goes to a licensed professional, not an Altruist template."""
    nulls = [b["id"] for b in real.boundary_list if b.get("route_slot") is None]
    assert "B-11" in nulls


def test_duplicate_boundary_id_is_rejected(dep):
    dep.boundary_list[1]["id"] = dep.boundary_list[0]["id"]
    assert "BD001" in blocking_codes(check_boundaries(dep))


def test_boundary_without_triggers_is_rejected(dep):
    dep.boundary_list[0]["triggers"] = []
    assert "BD003" in blocking_codes(check_boundaries(dep))


def test_missing_boundary_field_is_rejected(dep):
    del dep.boundary_list[0]["source"]
    assert "BD003" in blocking_codes(check_boundaries(dep))


def test_invalid_disposition_is_rejected(dep):
    dep.boundary_list[0]["disposition"] = "maybe"
    assert "BD005" in blocking_codes(check_boundaries(dep))


def test_undeclared_answerable_topic_is_rejected(dep):
    """Catches a fact added under a topic the boundary layer never sanctioned —
    it becomes stateable with no boundary reasoning behind it."""
    dep.facts[0]["topic"] = "internal-architecture"
    assert "BD004" in blocking_codes(check_boundaries(dep))


def test_critical_boundaries_are_present(real):
    """Regression guard on the three boundaries the audit called critical."""
    ids = {b["id"] for b in real.boundary_list}
    for bid in ("B-13", "B-14", "B-15"):
        assert bid in ids

    approval = next(b for b in real.boundary_list if b["id"] == "B-13")
    assert approval["disposition"] == "refuse", (
        "B-13 must refuse. The old plan required the agent to name an approver; "
        "with the org chart empty that could only be satisfied by fabrication."
    )
