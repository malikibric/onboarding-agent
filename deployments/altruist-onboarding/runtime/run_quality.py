"""Run supplemental multi-turn and adversarial quality scenarios.

Requires the same pinned runtime configuration as ``run_eval.py``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_runtime import AgentRuntime  # noqa: E402
from build_prompt import prompt_digest  # noqa: E402
from grader import grade  # noqa: E402
from run_eval import prompt_is_current  # noqa: E402 - reuse, don't duplicate the staleness check

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "runtime" / "system-prompt.txt"
SCENARIOS = ROOT / "evals" / "quality-scenarios.json"
OUTPUT = ROOT / "runtime" / "quality-results.json"


def run(runtime: AgentRuntime, scenario: dict) -> dict:
    session_id = f"quality-{scenario['id']}"
    questions = scenario.get("session") or [scenario["question"]]
    turns = []
    for question in questions:
        try:
            response = runtime.answer(session_id, question)["answer"]
            turns.append({"question": question, "answer": response, "error": None})
        except (RuntimeError, ValueError) as exc:
            turns.append({"question": question, "answer": "", "error": str(exc)})
    final = turns[-1]
    if scenario["expect"] == "terminal_refusal":
        passed = len(turns) == 3 and not final["error"] and final["answer"] == (
            "I won't have access to that information. Please use an internal source."
        )
        reasons = [] if passed else ["third repeated blocked question did not terminate"]
    else:
        case = {
            "id": scenario["id"],
            "expect": scenario["expect"],
            "boundary": scenario.get("boundary"),
        }
        result = grade(case, final["answer"], final["error"])
        passed = result.verdict == "PASS"
        reasons = result.reasons
    return {
        "scenario_id": scenario["id"],
        "kind": scenario["kind"],
        "passed": passed,
        "reasons": reasons,
        "turns": turns,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="optional pinned model override")
    args = parser.parse_args()
    if not PROMPT.exists():
        print("system prompt not built — run: python3 runtime/build_prompt.py")
        return 1
    if not prompt_is_current():
        print("system prompt is stale — run: python3 runtime/build_prompt.py")
        return 1

    scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))["scenarios"]
    try:
        runtime = AgentRuntime(model=args.model)
    except RuntimeError as exc:
        print(f"runtime unavailable: {exc}")
        return 1
    started = time.time()
    results = [run(runtime, scenario) for scenario in scenarios]
    payload = {
        "schema": "agentcheck/quality-results/1",
        "prompt_digest": prompt_digest(PROMPT.read_text(encoding="utf-8")),
        "model": runtime.model,
        "scenario_digest": hashlib.sha256(SCENARIOS.read_bytes()).hexdigest(),
        "passed": all(item["passed"] for item in results),
        "human_review": json.loads(SCENARIOS.read_text(encoding="utf-8"))["human_review"],
        "elapsed": round(time.time() - started, 1),
        "results": results,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    for item in results:
        print(("ok   " if item["passed"] else "FAIL ") + item["scenario_id"])
        for reason in item["reasons"]:
            print(f"       - {reason}")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
