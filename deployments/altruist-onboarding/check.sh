#!/usr/bin/env bash
# Release gate. Exit 0 = cleared to ship. Exit 1 = blocked, with reasons.
#
# Five sections, each independent:
#   1. agentcheck --strict   structural integrity of facts, boundaries, and eval coverage
#   2. domain-review gates   the glossary needs a named human reviewer
#   3. knowledge-base lint   core's validate.py over knowledge/public/*.md
#   4. last behavioural run  results.json must be complete, clean, and current
#   5. quality scenarios     supplemental suite plus its human review sample
#
# Sections 2 and 5 can only be cleared by a person recording their name and a date.
# That is the design, not an oversight — see docs/risks-and-next-steps.md NS-07, NS-13.
#
# The live behavioural run itself is separate and costs model calls: runtime/run_eval.py.
# Arguments to this script are forwarded to agentcheck.

set -uo pipefail
cd "$(dirname "$0")"

status=0

echo "==> Structural verification (agentcheck)"
if ! (cd verification && python3 -m agentcheck --strict "$@"); then
  status=1
fi

echo
echo "==> Domain-review gates"
if [ ! -f knowledge/glossary-review.json ]; then
  echo "  BLOCK  glossary review record is missing"
  status=1
else
  if ! python3 - <<'PY'
import json
import sys
from pathlib import Path

review = json.loads(Path("knowledge/glossary-review.json").read_text())
if review.get("status") != "approved" or not review.get("reviewer") or not review.get("reviewed_at"):
    print("  BLOCK  glossary requires an identified domain reviewer and approval date")
    sys.exit(1)
print(f"  ok    glossary approved by {review['reviewer']} on {review['reviewed_at']}")
PY
  then
    status=1
  fi
fi

echo
echo "==> Knowledge-base lint (core validate.py)"
lint_failed=0
for f in knowledge/public/*.md; do
  if out=$(python3 enforcement/validate.py "$f" --rules enforcement/rules.json 2>&1); then
    echo "  ok    $f"
  else
    lint_failed=1
    status=1
    echo "  BLOCK $f"
    echo "$out" | sed 's/^/        /'
  fi
done
[ "$lint_failed" -eq 0 ] && echo "  all public knowledge files pass"

echo
echo "==> Last behavioural run (runtime/results.json)"
if [ ! -f runtime/results.json ]; then
  echo "  WARN  no behavioural run on record — run: python3 runtime/run_eval.py"
  status=1
else
  if ! python3 - <<'PY'
import json, pathlib
import hashlib
import sys
status = 0
r = json.loads(pathlib.Path("runtime/results.json").read_text())
mr, ma = r["must_refuse"], r["must_answer"]
print(f"  must_refuse : {mr['passed']}/{mr.get('graded', mr.get('total'))} graded ({mr['pct']}%)")
print(f"  must_answer : {ma['passed']}/{ma.get('graded', ma.get('total'))} graded ({ma['pct']}%)")
print(f"  fabrications: {r['fabrications']}   leaks: {r.get('leaks', 'n/a')}")
if r.get("fabrications", 0) or r.get("leaks", 0):
    print("  BLOCK  behavioral results contain fabrications or leaks")
    status = 1
errored = r.get("errored", [])
if errored:
    print(f"  ERRORED     : {len(errored)} infra/spend-limit (re-run): {', '.join(errored)}")
    status = 1
res_m = pathlib.Path("runtime/results.json").stat().st_mtime
newer = [str(p) for p in pathlib.Path("knowledge").rglob("*") if p.is_file() and p.stat().st_mtime > res_m]
if newer:
    print(f"  BLOCK  knowledge changed since this run ({len(newer)} file(s)) — re-run runtime/run_eval.py")
    status = 1
if not r.get("gate_met"):
    print("  BLOCK  last behavioural run did not fully meet the gate (see above)")
    status = 1
if not r.get("model"):
    print("  BLOCK  behavioral result has no pinned model identifier")
    status = 1
if len(r.get("results", [])) != len(json.loads(pathlib.Path("evals/refusal-suite.json").read_text())["cases"]):
    print("  BLOCK  behavioral result does not cover the complete eval suite")
    status = 1
manifest = pathlib.Path("runtime/prompt-manifest.json")
prompt = pathlib.Path("runtime/system-prompt.txt")
if not manifest.exists() or not prompt.exists():
    print("  BLOCK  prompt manifest or artifact is missing — run runtime/build_prompt.py")
    status = 1
else:
    m = json.loads(manifest.read_text())
    digest = hashlib.sha256(prompt.read_bytes()).hexdigest()
    if m.get("prompt_digest") != digest:
        print("  BLOCK  prompt artifact hash does not match manifest")
        status = 1
    from runtime.build_prompt import source_digest
    if m.get("source_digest") != source_digest():
        print("  BLOCK  prompt manifest is stale relative to source artifacts")
        status = 1
    if r.get("prompt_digest") != digest:
        print("  BLOCK  behavioural results were produced with a different prompt")
        status = 1
if status:
    sys.exit(1)
PY
  then
    status=1
  fi
fi

echo
echo "==> Supplemental quality scenarios"
if [ ! -f runtime/quality-results.json ]; then
  echo "  BLOCK  no quality scenario run — run: python3 runtime/run_quality.py"
  status=1
else
  if ! python3 - <<'PY'
import hashlib
import json
import pathlib
import sys

scenario_path = pathlib.Path("evals/quality-scenarios.json")
result_path = pathlib.Path("runtime/quality-results.json")
scenarios = json.loads(scenario_path.read_text())
results = json.loads(result_path.read_text())
if results.get("scenario_digest") != hashlib.sha256(scenario_path.read_bytes()).hexdigest():
    print("  BLOCK  quality results are stale relative to quality scenarios")
    sys.exit(1)
if not results.get("passed"):
    print("  BLOCK  supplemental quality scenarios did not pass")
    sys.exit(1)
review = results.get("human_review", {})
if review.get("status") != "approved" or not review.get("reviewer") or not review.get("reviewed_at"):
    print("  BLOCK  quality sample requires human review and approval date")
    sys.exit(1)
print("  ok    supplemental scenarios and human sample are approved")
PY
  then
    status=1
  fi
fi

echo
if [ "$status" -eq 0 ]; then
  echo "PASSED — build-time gates clear. See behavioural result above and docs/behavioural-results.md."
else
  echo "BLOCKED — fix every line marked BLOCK above before shipping."
  echo "         A BLOCK on a review record needs a named person and a date, not a code change."
fi
exit "$status"
