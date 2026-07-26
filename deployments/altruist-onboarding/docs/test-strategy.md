# Test Strategy

## What is actually testable here

This deployment is a knowledge base, a set of procedures, and gates — not a running program with a chat loop. That constrains what testing can honestly claim.

| Layer | Testable deterministically? | How |
|---|---|---|
| Fact base integrity | Yes | `agentcheck` — schema, tiers, provenance, dates, uniqueness |
| Citation resolution | Yes | `agentcheck` — every `[ALT-###]` resolves to an answerable fact |
| Boundary integrity | Yes | `agentcheck` — routes exist on disk, topics declared, no duplicates |
| Eval coverage | Yes | `agentcheck` — every boundary has a refusal case; ship-gate minimum |
| Published-count drift | Yes | `agentcheck` — registry table vs fact base |
| Knowledge prose hygiene | Yes | `core/enforcement/validate.py` + `rules.json` |
| **Whether an answer is actually safe** | **No** | Human pass — TG-01 |

The last row is the honest limit and is stated everywhere it matters rather than buried here.

## Principle: a validator that has never failed is not known to work

Every check has a **negative test** that deliberately breaks the deployment and asserts the specific code fires. Positive tests ("the real deployment passes") are necessary but prove almost nothing on their own — they would also pass if the checks did nothing.

That principle caught a real bug during the build: `check_citations` crashed on a prose path outside the deployment root, found by the negative test for the orphan-fact warning. A reporting convenience was able to crash the check that produced the finding. Fixed in `_display_path`.

It also caught a real design smell: the `COMPETITOR-001` lint rule fired on `01-company-and-mission.md`, which contained an *instruction not to compare* — a rule living in a knowledge file. That is a nouns-vs-verbs violation `core` warns about explicitly. Fixed by moving the rule to `CLAUDE.md` §10.

## Test inventory — 128 tests

| File | Count | Covers |
|---|---|---|
| `test_grader.py` | 38 | Grader calibration, locked to real transcripts — refusal markers, name detectors, leakage, attribution decay |
| `test_evals_and_registry.py` | 23 | Coverage invariants, ship gate, registry drift, CLI contract |
| `test_factbase.py` | 23 | Schema, tiers, sources, sensitivity, dates, quarantine, the PLAN invariant |
| `test_enforcement_rules.py` | 19 | Every lint rule fires; validator is an unmodified copy of core's |
| `test_citations_and_boundaries.py` | 16 | Citation resolution, the two citation forms, route existence, topic coverage |
| `test_runtime.py` | 8 | Session repetition, question normalization, and the pre-send output policy |
| `test_glossary_review.py` | 1 | The glossary review record cannot silently self-approve |

Counts are hand-written and therefore exactly the kind of thing `RG001` exists to catch
elsewhere. Regenerate them with `cd verification && python3 -m pytest tests/ -q --collect-only`
rather than trusting this table.

### Invariants worth naming

- **`test_plan_sourced_fact_is_rejected` / `test_plan_as_secondary_source_still_rejected`** — the central safety property. `new-agent.md` cannot make a claim answerable, and cannot launder one by appearing alongside a real source.
- **`test_every_boundary_has_a_refusal_case`** — a boundary nobody tests is a boundary nobody has confirmed the agent honours.
- **`test_regulatory_claims_remain_quarantined`** — the four critical claims. A regression here means the agent can tell a new hire something about entity structure or coverage that nobody has confirmed.
- **`test_known_sensitive_facts_are_marked`** — silently unmarking `ALT-028` would let Hazel's security messaging be stated bare.
- **`test_nothing_currently_claims_external_verification`** — an honesty check on the delivery itself.
- **`test_suite_covers_the_answer_refuse_seam`** — ANS-12 (answer with attribution) against REF-26/REF-27 (refuse the assurance). The sharpest seam in the design; both sides stay tested.
- **`test_validator_is_unmodified_copy_of_core`** — byte-equality with `core/enforcement/validate.py`. A drifted copy means the deployment is no longer running the scaffold's enforcement.
- **`test_cli_fails_closed_on_missing_deployment`** — a tool that reports success on a deployment it could not load is worse than no tool.
- **`test_all_declared_rules_have_a_firing_test`** — adding a lint rule without a test that trips it is how a rule silently stops working.

## Running

```
./check.sh                                        # release gate: agentcheck + lint
cd verification && python3 -m pytest tests/ -q    # full suite
cd verification && python3 -m agentcheck --strict # warnings block too
```

## Test gaps — stated, not hidden

### TG-01 — Behavioural testing **[CLOSED for the primary suite; the supplemental sample still needs a human]**
The recorded run in `runtime/results.json` now covers all 46 cases with none errored:
32/32 must_refuse, 14/14 must_answer, 0 fabrications, 0 leaks, `gate_met: true`. The
evaluator and release script require every case to be graded before a result can pass, and
that condition is met. What remains open is not the primary suite but the supplemental one:
`runtime/quality-results.json` passed its automated checks, and its five-scenario human
review sample is still `pending` — `check.sh` blocks on that, correctly.

**Residual limitation** (does not reopen TG-01, but is real): refusal detection in the grader is recall-limited — it screens conservatively in the safe direction (a missed marker fails a good case, never passes a bad one) and every verdict is backed by a retained transcript for human audit. Full detail and the run history are in `docs/behavioural-results.md`.

**Interim mitigation still stands.** Absence of access (`tools/access-policy.md`) bounds the damage from any behavioural failure regardless of what the agent says.

`evals/quality-scenarios.json` defines the multi-turn, prompt-injection, paraphrase,
contradiction, and human-sampling scenarios. They have been run (`python3 runtime/run_quality.py`)
and the automated portion passes, but the release gate deliberately does not treat an
automated pass on a *quality* sample as sufficient: `human_review.status` is still `pending`
and `check.sh` blocks until a named reviewer and date are recorded.

### TG-02 — Lint cannot detect an uncited claim that should have been cited
`FACT-001` requires at least one citation per file. It cannot detect a third paragraph that quietly asserts something unsourced. Human review job.

### TG-03 — Glossary definitions are unreviewed by a domain expert
`02-glossary.md` was written from general knowledge. The definitions are believed correct but no one with financial-services expertise has checked them, and a subtly wrong definition of SIPC or wash sale would be taught confidently. Assumption A-04.

### TG-04 — Attribution wording is untested with real users
"Altruist's public materials describe…" is a judgment (A-06). Too weak and a hire hears it as fact; too heavy and every answer becomes caveat. No user testing.

### TG-05 — Regex cannot distinguish quotation from assertion
Documented in `enforcement/gates.md`. `rules.json` is scoped to `knowledge/public/*.md` and deliberately excludes `CLAUDE.md` and `skills/`, which quote forbidden phrasings as counterexamples. A known miss: the entitlement rule does not match the bare `you get`.

### TG-06 — No test that the knowledge is *useful*
Everything here tests safety and consistency. Nothing tests whether a new hire is better off. The 14 `must_answer` cases are the closest proxy — they exist specifically because an agent that refuses everything passes every safety test and fails its purpose — and they now all pass live. Passing them means the agent answered without fabricating; it does not mean the answer helped anyone.

## Ship criteria

| Criterion | Status |
|---|---|
| `agentcheck` exits 0 | **Met** |
| Knowledge lint exits 0 on all public files | **Met** |
| 128 tests pass (119 structural/grader + 8 runtime + 1 glossary gate) | **Met** |
| Every boundary has a refusal case | **Met** (15/15) |
| ≥20 must_refuse cases | **Met** (32) |
| Published counts match fact base | **Met** |
| **Behavioural release gate** | **Met** — all 46 cases graded, 32/32 refuse, 14/14 answer, 0 fabrications, 0 leaks |
| **Glossary domain review** | **Blocked — `glossary-review.json` requires a qualified reviewer and date** |
| **Quality-sample human review** | **Blocked — `quality-results.json` `human_review` requires a reviewer and date** |
| **Correction-loop owner** | **Specified, not assigned** — documented human dependency in `feedback/corrections.md` (U-03) |

**The three open criteria all require a named human.** No amount of further building closes
them, and the builder cannot supply a name — that is the same fabrication the agent itself
refuses. `check.sh` exits 1 until all three are recorded.
