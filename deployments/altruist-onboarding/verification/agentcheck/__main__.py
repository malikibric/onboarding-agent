"""CLI entry point. Exit 0 = clear to ship, exit 1 = blocked."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .checks import run_all
from .loaders import ArtifactError, load
from .model import Report


def _default_root() -> Path:
    # verification/agentcheck/__main__.py -> deployment root is two levels up.
    return Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agentcheck",
        description="Build-time verification of the agent's knowledge, boundaries, and eval coverage.",
    )
    parser.add_argument("--root", type=Path, default=None, help="deployment directory (default: autodetect)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--strict", action="store_true", help="treat warnings as blocking")
    args = parser.parse_args(argv)

    root = args.root or _default_root()

    try:
        dep = load(root)
    except ArtifactError as e:
        # A deployment that cannot be loaded fails closed. Never report success.
        if args.json:
            print(json.dumps({"passed": False, "error": str(e)}, indent=2))
        else:
            print(f"BLOCKED — could not load deployment\n\n  x {e}")
        return 1

    report = Report(run_all(dep))
    blocking = list(report.blocking)
    warnings = list(report.warnings)
    if args.strict:
        blocking += warnings
        warnings = []

    if args.json:
        print(json.dumps({
            "passed": not blocking,
            "root": str(dep.root),
            "counts": {
                "facts": len(dep.facts),
                "quarantined": len(dep.quarantine),
                "boundaries": len(dep.boundary_list),
                "cases": len(dep.cases),
            },
            "blocking": [{"code": f.code, "message": f.message, "location": f.location} for f in blocking],
            "warnings": [{"code": f.code, "message": f.message, "location": f.location} for f in warnings],
        }, indent=2))
        return 1 if blocking else 0

    print(f"agentcheck — {dep.root}")
    print(
        f"  {len(dep.facts)} answerable facts · {len(dep.quarantine)} quarantined · "
        f"{len(dep.boundary_list)} boundaries · {len(dep.cases)} eval cases\n"
    )

    if blocking:
        print("BLOCKED — not cleared to ship\n")
        for f in blocking:
            print(f"  x {f.render()}")
    else:
        print("PASSED — knowledge base and boundaries are internally consistent")

    if warnings:
        print("\nWarnings (not blocking):")
        for f in warnings:
            print(f"  ! {f.render()}")

    if not blocking:
        print(
            "\nNote: this verifies DECLARED knowledge and coverage, not live answers.\n"
            "The live behavioural pass is separate: python3 runtime/run_eval.py (see docs/behavioural-results.md)."
        )
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
