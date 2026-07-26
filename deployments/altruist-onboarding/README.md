# Altruist New-Hire Onboarding Agent

A first-days orientation assistant for a new Altruist hire, built from public documents only. Its most important behaviour is **refusing accurately**, not answering fluently.

Built on the `core/` five-layer scaffold. Architecture and safety boundaries come from `AUDIT_altruist_onboarding_agent.md`.

**Release status: blocked, and correctly so.** Every gate a machine can decide is green. The three that remain need a named human, and the builder cannot supply one — see [Current state](#current-state-honestly). Run `./check.sh` for the authoritative answer; the prose in this file is a summary, and summaries drift.

## Start here

| If you want to… | Read |
|---|---|
| Understand what the agent is and does | `AGENT.md` |
| Know what it may state and how confidently | `knowledge/factbase.json`, `knowledge/source-registry.md` |
| Know what it refuses and where that routes | `knowledge/boundaries.json` |
| Understand the layout and why | `docs/architecture.md` |
| Know what was decided and what was given up | `docs/decisions.md` |
| Know what is not trustworthy yet | `docs/assumptions-and-unknowns.md` |
| Know what was not built and why | `docs/deferred.md` |
| Know what is tested and what is not | `docs/test-strategy.md`, `docs/test-results.md` |
| See the agent actually answering | `docs/behavioural-results.md`, `runtime/transcripts/` |
| Test `/onboard` yourself in Claude Code | `docs/manual-onboard-test.md` |
| Know what to do next | `docs/risks-and-next-steps.md` |

## Try it in Claude Code

```bash
cd deployments/altruist-onboarding   # this directory — commands are discovered relative to it
claude
```

Then type `/onboard`, or `/onboard <your first question>`.

The command is at `.claude/commands/onboard.md`. It imports `runtime/system-prompt.txt` — the same specification the automated evaluator uses — so the interactive persona and the tested one are the same rules, reused rather than restated.

**One honest difference.** The automated path additionally runs a deterministic pre-send check (`validate_output` in `runtime/agent_runtime.py`) that blocks a leaked or fabricated answer in code. The interactive path does not have that code-level gate — only the same prompt-level instructions. Same rules, weaker enforcement.

Three manual scenarios have been run and each produced a fix (`docs/onboarding-iteration-log.md`); five remain. `docs/manual-onboard-test.md` has the script and says which is which.

## Verify it

```bash
./check.sh                                        # build-time gates + last behavioural result
cd verification && python3 -m pytest tests/ -q    # 128 tests (structural + grader + runtime)
python3 runtime/build_prompt.py                   # compose the system prompt from artifacts
python3 runtime/run_eval.py --regrade             # re-score existing transcripts, no model calls
```

The live behavioural run makes model calls and needs both variables set:

```bash
ALTRUIST_MODEL=<pinned-model-id> \
ALTRUIST_CLAUDE_CONFIG_DIR=/isolated/claude-config \
  python3 runtime/run_eval.py --workers 3         # ~114s for 46 cases
```

Build-time checks are **stdlib-only** so release gating never depends on an install. `pytest` is needed for the test suite; the live run additionally needs the `claude` CLI.

The release gate blocks missing, stale, incomplete, or failed behavioural results — and blocks separately if any file under `knowledge/` is newer than the recorded run.

## One mechanic worth knowing before you edit anything

The system prompt is **built, not written**. Eleven files (listed in `runtime/prompt-manifest.json`) are hashed into `prompt_digest`; `check.sh` compares that hash against the one recorded in `runtime/results.json`.

**Editing any of those eleven — including a typo fix — invalidates the behavioural evidence** and requires a fresh live run before release. Everything else (`docs/`, this file, `runtime/*.py`, `check.sh`, `verification/`) is free to edit. Full explanation in `docs/architecture.md`.

## Current state, honestly

**Verified:**
- 32 answerable facts, each with a tier, provenance, and a checked date
- 19 quarantined claims that cannot leak into answers — enforced mechanically, tested twice
- 15 declared refusal boundaries, every one covered by at least one test
- 3 wired procedures; read-only access with everything else explicitly withheld
- 12 build-time gates and 128 tests, all proven to fire against deliberately broken input
- A controlled runtime boundary: bearer auth, pinned model configuration, session repetition handling, redacted audit logging, fail-closed pre-send output checks
- **A complete behavioural run: 46/46 cases graded, 32/32 refuse, 14/14 answer, 0 fabrications, 0 leaks** (`runtime/results.json`, `docs/behavioural-results.md`)
- A Claude Code slash command (`/onboard`) reusing that same specification

**Blocked on three named humans — no further building closes these:**
- **The correction loop has no assigned owner.** Specified precisely in `feedback/corrections.md`; needs a real internal person. The builder cannot invent one.
- **The glossary has no domain reviewer.** `knowledge/glossary-review.json` lists nine high-risk financial-services terms awaiting a qualified reviewer and date.
- **The quality sample has no reviewer.** `runtime/quality-results.json` passes its automated checks, but its five-scenario human review is `pending`.

**Known gaps, stated rather than buried:**
- **Nothing is externally verified.** All three source documents assert facts about Altruist without a single resolvable URL. Every fact carries `external_verified: false`. The tier system records document provenance inside this repository — not verification against the world.
- **The recorded run used a model alias, not a pinned id.** `results.json` says `"model": "sonnet"`, so the result is real but not reproducible against a fixed model (NS-12).
- **Two written skills are not wired in.** `skills/explain.md` and `skills/ask-better-questions.md` exist but are absent from `build_prompt.py`'s `SOURCE_FILES`, so the agent never receives them (NS-09, DF-11).
- **Five of eight manual `/onboard` scenarios are unrun,** including the repeated-request-to-guess case — the failure mode this agent exists to prevent.

**Before a real launch:** record the three human sign-offs, pin a real model id and re-run, and decide NS-09 and NS-10.

## Controlled runtime

```bash
export ALTRUIST_MODEL='your-pinned-model-id'
export ALTRUIST_RUNTIME_TOKEN='a-secret-runtime-token'
export ALTRUIST_CORRECTION_OWNER='named-owner'
export ALTRUIST_CORRECTION_BACKUP='named-backup'
export ALTRUIST_CLAUDE_CONFIG_DIR='/isolated/claude-config'
python3 runtime/server.py
```

All five are required and the server refuses to start without them — including the two correction-loop names, which the runtime never reads. That is deliberate: it makes the unassignable human dependency block startup instead of being quietly forgotten.

The server exposes `POST /answer` and requires `Authorization: Bearer …`. The evaluator and server share the same runtime boundary and use only the isolated Claude config and an allowlisted environment, so a benchmark cannot take a safer path than production.

The runtime stores only hashed session/question/answer identifiers and word counts in `runtime/conversation-log.jsonl`; the log is mode `0600` and pruned by `ALTRUIST_LOG_RETENTION_DAYS` (30 days by default). Raw conversation text is kept in evaluation transcripts only.

Optional: `ALTRUIST_RUNTIME_HOST` (default `127.0.0.1`), `ALTRUIST_RUNTIME_PORT` (default `8080`), `ALTRUIST_RUNTIME_TIMEOUT` (default `180`).

## The highest-leverage thing you can do

Fill `knowledge/internal/13-people-and-contacts.TEMPLATE.md`.

It unblocks five refusal boundaries at once and converts the weakest part of every internal refusal — *"I don't know who fills that slot"* — into something the hire can act on. All seven internal templates are empty by design, but this one costs the least and returns the most.

Note that filling anything under `knowledge/` invalidates the recorded behavioural run by design — budget a re-run alongside it.
