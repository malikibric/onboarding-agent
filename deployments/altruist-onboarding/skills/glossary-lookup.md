# Skill: glossary-lookup

**Owns:** defining an industry term. Starts when a term is asked about or used unexplained; stops when the definition lands and the prior thread resumes.
**Triggered by:** the hire asks what a term means, or uses one incorrectly, or the agent is about to use one for the first time in a session.
**Knowledge required:** `knowledge/public/02-glossary.md`; `knowledge/CLAUDE.md` §2.

---

## Steps

**1. Classify the term**
- Do: decide whether it is (a) general industry vocabulary, (b) an Altruist-specific claim, or (c) internal jargon.
- Done when: classified. This determines everything downstream and is the step most likely to be skipped.
- If it fails (unclear): treat as (c) internal and refuse. A term the agent cannot place is more likely internal shorthand than industry standard.

**2a. General industry term → define it**
- Do: one plain sentence, then a second only if the term has a common confusion worth pre-empting.
- Done when: a beginner could use the word in a sentence.
- **Provenance rule:** these definitions are general industry knowledge, not sourced from Altruist material. Do not attach a fact id to a definition, and do not imply Altruist supplied it.

**2b. Altruist-specific claim → hand to `answer-or-refuse`**
- Do: if the question is really "what does Altruist do about X", it is a fact question, not a vocabulary question. Route it.
- Done when: routed. Example: "what's a model marketplace" is 2a; "how many models does Altruist have" is a fact question, and the count is quarantined (`ALT-Q10`).

**2c. Internal jargon → refuse**
- Do: hand to `answer-or-refuse`, boundary `B-01`.
- Done when: a brief refusal is delivered. Internal codenames, system nicknames, and team shorthand are exactly the vocabulary the agent must not guess at — a plausible-sounding definition of an internal term is worse than no definition, because the hire will repeat it.

**3. Flag the two confusions on first relevant use**
- Do: when custodian, advisor, or client first come up, state the distinction explicitly — the custodian holds assets, the advisor advises, and "client" means the advisor's end investor rather than Altruist's customer.
- Done when: stated once per session.
- If it fails: this is the highest-value correction in the glossary. Do not let it slide because it seems basic.

**4. Return to the prior thread** — a definition is an interruption, not a new topic.

---

## Stop conditions

Halt and hand to a human when:
- The term is internal jargon (`B-01`).
- Defining the term would require explaining what a protection covers in a specific case, or a coverage amount (`B-15`) — define SIPC and FDIC as concepts, never as applied coverage.
- The question behind the term is really a request for tax, investment, or financial advice (`B-11`).

## Output

Goes to: the new hire, in conversation.
Format: one to two sentences. Plain language, no jargon inside the definition of jargon.
Must pass: no definition may introduce an unattributed Altruist claim.

## Known gaps

- **The glossary is fixed and hand-maintained.** Terms outside `02-glossary.md` fall to step 1's judgment. Adding a term is a knowledge-layer edit plus a correction-log entry, not something the agent does at runtime.
- **Internal vocabulary is not populated.** `core/` calls vocabulary the highest-value section of a knowledge layer, and this agent has only the *industry* half of it. Altruist's internal terms — the ones a hire actually needs in week one — remain unknown. The controlled `knowledge/internal/16-internal-vocabulary.TEMPLATE.md` exists, but must be filled from an authorised internal source before it can support answers.
