"""Core types for verification findings.

A finding is either BLOCK (release is not clear) or WARN (visible, not blocking).
The split matters: if everything blocks, people route around the system and
nothing is enforced. Keep blocking findings few and genuinely absolute.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    BLOCK = "block"
    WARN = "warn"


@dataclass(frozen=True)
class Finding:
    """One rule violation, traceable to a code and a location."""

    code: str
    severity: Severity
    message: str
    location: str = ""

    def render(self) -> str:
        where = f" ({self.location})" if self.location else ""
        return f"[{self.code}] {self.message}{where}"


def block(code: str, message: str, location: str = "") -> Finding:
    return Finding(code, Severity.BLOCK, message, location)


def warn(code: str, message: str, location: str = "") -> Finding:
    return Finding(code, Severity.WARN, message, location)


@dataclass
class Report:
    findings: list[Finding]

    @property
    def blocking(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.BLOCK]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.WARN]

    @property
    def passed(self) -> bool:
        return not self.blocking
