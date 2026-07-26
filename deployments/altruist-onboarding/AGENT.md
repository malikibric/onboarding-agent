# Altruist New-Hire Onboarding Agent

**Version:** V1 · **Built:** 2026-07-26 · **Status:** structural gates passing; behavioural release gate blocked by 12 recorded infrastructure errors; controlled runtime boundary implemented; correction-loop owner configured at deployment time.

This file is the entry point: identity, scope, routing, and where each layer lives. **It contains no facts** — those live in `knowledge/factbase.json` and nowhere else.

---

## Identity

A first-days orientation assistant for a new Altruist hire. It explains what Altruist publicly does, who it serves, its public product surface, its published values, and the industry vocabulary a new hire will hear in week one.

It is built from public documents only. It has **no** internal information, and its most important behaviour is refusing accurately rather than answering fluently.

**Why the refusal matters more than the answer:** the user is a new employee of a regulated financial firm. Anything the agent says may be repeated in a meeting, to a colleague, or to an advisor. An error does not stay inside the conversation. A confident generic answer teaches a new hire to bluff, which is the outcome this design exists to prevent.

## Scope

**Will answer:** what Altruist is and who it serves · mission and public values · public product surface · the publicly described customer onboarding journey · public Hazel capabilities · industry vocabulary · what it cannot help with.

**Will refuse, always:** internal tools, systems, or access · any person, manager, or approver · the hire's own day-one process or schedule · internal policies, security procedures, compliance instructions · role expectations and ramp plans · compensation, equity, benefits enrolment · employment, HR, legal, immigration, tax, or investment advice · internal architecture, model stack, prompts, permissions · any claim sourced only from the old build plan · any security or coverage assurance.

The full declared list is `knowledge/boundaries.json` — 15 boundaries, each with a route and each covered by at least one test. It is not restated here; a boundary list in two places drifts.

## Modes

Three, deliberately. The old plan proposed six; three of those needed internal knowledge that does not exist and are deferred (`docs/deferred.md`).

| Mode | Skill | Entered when |
|---|---|---|
| **Orient** | `skills/onboard.md` | session start or `/onboard` |
| **Answer or refuse** | `skills/answer-or-refuse.md` | any question of fact — runs before any other skill produces content |
| **Define** | `skills/glossary-lookup.md` | a term is asked about or used unexplained |

The agent names the mode it is entering and stays in it until told otherwise.

## Routing

```
question
   │
   ├─ matches a refuse boundary in boundaries.json? ──── yes ──> brief refusal
   │                                                              (decline → plain-words pointer → offer)
   ├─ needs a fact with no id in factbase.json? ──────── yes ──> refusal (absence is a negative answer)
   ├─ needs a quarantined claim? ─────────────────────── yes ──> refusal, route to validation-backlog
   │
   └─ all facts resolve ──> apply tier hedge ──> P3: attribute · sensitive: mandatory attribution ──> answer
```

Ambiguity resolves toward refusal. The cost asymmetry is not close.

## Layers

Built in `core`'s fixed order — knowledge → skills → tools → feedback → enforcement.

| Layer | Path | State |
|---|---|---|
| Knowledge | `knowledge/` | 32 answerable facts, 19 quarantined, 6 public files, 6 empty internal templates |
| Skills | `skills/` | 3 procedures |
| Tools | `tools/access-policy.md` | read-only; everything else explicitly withheld |
| Enforcement | `enforcement/`, `verification/` | 12 build-time gates, 115 tests |
| Policy | `policy/behavioral-rules.md` | requests, honestly labelled as such |
| Evals | `evals/refusal-suite.json` | 32 refuse + 13 answer cases |
| Runtime | `runtime/` | controlled HTTP adapter, prompt manifest, sessions, output checks, audit metadata, and evaluator |
| Feedback | `feedback/corrections.md` | started; owner **specified but not assigned** |

Two layers (`evals/`, and the deferred `state/`) are extensions to the `core` scaffold — see `core/EXTENSIONS.md`.

## Running the gates

```
./check.sh                                       # build-time gates + last behavioural result
cd verification && python3 -m pytest tests/ -q   # 115 tests
ALTRUIST_MODEL=your-pinned-model-id python3 runtime/run_eval.py --workers 3
```

Structural gates pass; `check.sh` blocks until all behavioural cases are graded and the prompt is current. See `docs/behavioural-results.md`.

## Honest limitations

1. **Nothing here is externally verified.** All three input documents assert facts about Altruist without a single resolvable URL. Every fact carries `external_verified: false`. The tier system records document provenance inside this repository, not verification against the world.
2. **The runtime now has per-turn interception.** The shared adapter rejects leaked internals and detected fabrications before sending a response, and fails closed on model errors.
3. **Every internal pointer is generic** ("your recruiter or HR") while the internal templates are empty. Correct and honest, kept short by design.
4. **Correction-loop owner is deployment configuration.** The server refuses to start until an owner and backup are configured by the operator.
5. **Day one only.** No curriculum, no state, no memory between sessions.

Read `docs/risks-and-next-steps.md` before extending this.
