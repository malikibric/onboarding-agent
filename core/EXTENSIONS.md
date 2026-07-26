# Scaffold Extensions

Two layers that the five-layer scaffold does not have, and which some deployments need. Recorded here so an addition is a **declared divergence** rather than an undocumented one — otherwise the next deployment inherits a shape that does not match this master and nobody knows whether that was deliberate.

Neither is added to `core/` itself. A deployment that needs one creates it and points here.

---

## `evals/` — forward-looking assessment

**The gap.** `feedback/` is backward-looking: a human corrects the agent, the correction goes into knowledge. That loop only runs *after* something has gone wrong in front of a real user.

**What `evals/` adds.** A fixed set of cases with expected dispositions, run before release. For a knowledge-bounded agent the highest-value form is a **refusal suite**: given a question, does the agent correctly decline rather than answer?

**Why it is not duplication.** `feedback/` records what went wrong once. `evals/` prevents a known class of failure from recurring. They meet at the correction loop: an out-of-scope failure logged in `feedback/` should add a case to `evals/`, so the fix is permanent rather than conversational.

**Shape that worked** (see `deployments/altruist-onboarding/evals/refusal-suite.json`):
- Cases carry an id, the question, an expected disposition, and the boundary or facts they exercise.
- `must_refuse` and `must_answer` both present — an agent that refuses everything passes every safety test and fails its purpose.
- Adversarial cases: hypothetical framing, explicit guess requests, false authority, roleplay requests, leading specifics.
- A build-time check proves every declared boundary has at least one case. Coverage is the property that makes the suite meaningful.

**Grading is human** unless the agent is wired to a runtime. Say so; do not report a structural coverage check as a behavioural pass.

---

## `state/` — longitudinal memory

**The gap.** The scaffold assumes an agent that runs a procedure and finishes. An agent that works with the same person over weeks needs to remember where they are.

**What `state/` would add.** Typically a profile (who the user is), progress (where they are in a sequence), and a gap log (what they got wrong, scheduled for retest).

**Why it is not in `core/`.** Because it is the layer most likely to be added carelessly. State means storing data about a person, which requires answers the scaffold has no opinion on: who operates the agent, what may be stored, for how long, who can read it. Adding a `state/` template to the master would make it look like a default rather than a decision.

**Precondition before building it:** a named operator, a retention rule, and an access rule. The Altruist deployment deferred `state/` on exactly these grounds (`docs/deferred.md` DF-05) and runs stateless.

---

## Fill order with extensions

The original order holds — knowledge → skills → tools → feedback → enforcement — because each layer depends on the one before.

- `evals/` slots in **after skills** (you cannot write cases before you know what the agent does) and **before enforcement** (coverage becomes something enforcement can gate).
- `state/` slots in **after tools**, because whether you may store anything is an access decision.

Enforcement stays last and separate. It is still the only layer that must hold when everything above it is wrong.
