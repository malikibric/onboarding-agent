"""Loading the deployment's declared artifacts.

Every loader fails loudly. A verification tool that silently treats a missing or
malformed artifact as "nothing to check" reports success on a broken deployment,
which is worse than no tool at all.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ArtifactError(Exception):
    """An artifact is missing or unreadable. Always fatal — never warn-and-continue."""


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ArtifactError(f"missing required artifact: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ArtifactError(f"{path}: invalid JSON — {e}") from e
    if not isinstance(data, dict):
        raise ArtifactError(f"{path}: expected a JSON object at the top level")
    return data


@dataclass
class Deployment:
    """Everything the checks need, loaded once.

    `root` is the deployment directory (the one containing knowledge/, skills/, ...).
    """

    root: Path
    factbase: dict[str, Any]
    boundaries: dict[str, Any]
    suite: dict[str, Any]
    prose: dict[Path, str] = field(default_factory=dict)

    # -- convenience accessors -------------------------------------------------

    @property
    def facts(self) -> list[dict[str, Any]]:
        return self.factbase.get("facts", [])

    @property
    def quarantine(self) -> list[dict[str, Any]]:
        return self.factbase.get("quarantine", [])

    @property
    def documents(self) -> dict[str, Any]:
        return self.factbase.get("documents", {})

    @property
    def boundary_list(self) -> list[dict[str, Any]]:
        return self.boundaries.get("boundaries", [])

    @property
    def answerable_topics(self) -> list[str]:
        return self.boundaries.get("answerable_topics", [])

    @property
    def cases(self) -> list[dict[str, Any]]:
        return self.suite.get("cases", [])

    def fact_by_id(self, fact_id: str) -> dict[str, Any] | None:
        return next((f for f in self.facts if f.get("id") == fact_id), None)

    def quarantine_by_id(self, q_id: str) -> dict[str, Any] | None:
        return next((q for q in self.quarantine if q.get("id") == q_id), None)


def load(root: Path) -> Deployment:
    """Load a deployment directory. Raises ArtifactError if anything required is absent."""
    root = root.resolve()
    if not root.is_dir():
        raise ArtifactError(f"not a directory: {root}")

    factbase = _load_json(root / "knowledge" / "factbase.json")
    boundaries = _load_json(root / "knowledge" / "boundaries.json")
    suite = _load_json(root / "evals" / "refusal-suite.json")

    public_dir = root / "knowledge" / "public"
    if not public_dir.is_dir():
        raise ArtifactError(f"missing required directory: {public_dir}")

    prose = {p: p.read_text(encoding="utf-8") for p in sorted(public_dir.glob("*.md"))}
    if not prose:
        raise ArtifactError(f"no prose knowledge files found in {public_dir}")

    return Deployment(
        root=root,
        factbase=factbase,
        boundaries=boundaries,
        suite=suite,
        prose=prose,
    )
