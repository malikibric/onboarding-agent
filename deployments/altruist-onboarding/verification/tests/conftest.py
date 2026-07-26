"""Shared fixtures.

The suite is built around one idea: a validator that has never been seen to fail is
not known to work. Every check gets a negative test that deliberately breaks the
deployment and asserts the specific code fires.
"""

from __future__ import annotations

import copy
import datetime as _dt
import sys
from pathlib import Path

import pytest

# The package lives one level up from tests/.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agentcheck import Deployment, load  # noqa: E402

DEPLOYMENT_ROOT = Path(__file__).resolve().parents[2]
TODAY = _dt.date(2026, 7, 26)


@pytest.fixture(scope="session")
def real() -> Deployment:
    """The actual deployment, loaded from disk."""
    return load(DEPLOYMENT_ROOT)


@pytest.fixture
def dep(real: Deployment) -> Deployment:
    """A deep copy, safe to mutate in a test."""
    return Deployment(
        root=real.root,
        factbase=copy.deepcopy(real.factbase),
        boundaries=copy.deepcopy(real.boundaries),
        suite=copy.deepcopy(real.suite),
        prose=dict(real.prose),
    )


def codes(findings) -> set[str]:
    return {f.code for f in findings}


def blocking_codes(findings) -> set[str]:
    return {f.code for f in findings if f.severity.value == "block"}
