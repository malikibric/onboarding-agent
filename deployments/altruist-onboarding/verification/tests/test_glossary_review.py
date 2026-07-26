"""Tests for the explicit human domain-review contract."""

from __future__ import annotations

import json
from pathlib import Path

DEPLOYMENT_ROOT = Path(__file__).resolve().parents[2]


def test_glossary_review_is_not_claimed_without_a_reviewer():
    review = json.loads(
        (DEPLOYMENT_ROOT / "knowledge" / "glossary-review.json").read_text()
    )
    assert review["status"] == "pending"
    assert review["reviewer"] is None
    assert review["reviewed_at"] is None
    assert review["high_risk_terms"]
