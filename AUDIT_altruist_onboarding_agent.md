# Comparative Audit — Altruist Onboarding Agent

**Audit date:** 2026-07-25
**Documents under review:**
- `altruist_onboarding_agent_knowledge.md` (primary grounding document — scope, safety boundaries, factual discipline)
- `new-agent.md` ("Build Plan v1" — older strategic draft, not authoritative)

**Architectural authority:** `core/` (five-layer deployment scaffold) + `README.md` (method)

**Trust labels used throughout:**
- **[V]** Verified from primary knowledge pack
- **[O]** Supported by old plan but needs validation
- **[I]** Inferred from structure (core folder / method docs)
- **[M]** Missing and must be created

---

## A. Executive assessment

There are **three competing architectures** in this repository and no document acknowledges the other two.

| Source | Proposed structure |
|---|---|
| `core/` | Five layers: `knowledge/CLAUDE.md` (one file, 12 fixed sections) → `skills/` → `tools/` → `feedback/` → `enforcement/` |
| Knowledge pack §"Recommended knowledge structure" | Twelve numbered files (`01_company_overview.md` … `15_role_specific_ramps_TEMPLATE.md`) |
| `new-agent.md` §4 | `AGENT.md` + `knowledge/00-09` + `skills/` + `state/` + `evals/` |

Nothing can be built until this is resolved. Section H resolves it.

**The three findings that matter most:**

1. **`new-agent.md` §10 "Enforcement" is not enforcement.** All six rules are prompt text. `core/enforcement/gates.md` states the test explicitly: *"if the agent can be talked out of it, it isn't enforcement."* The old plan's strongest-sounding section is, by the foundation's own definition, its weakest. **Critical.**

2. **`new-agent.md` enforcement rule 5 mandates fabrication.** It requires the agent to flag compliance-touching decisions and *"name who would need to approve."* The agent has zero internal org knowledge — the org chart is an empty template (pack §7). The knowledge pack forbids exactly this (§Guardrails: *"Do not provide compliance, legal, or operational instructions unless explicitly present in verified internal files"*). A rule that cannot be satisfied truthfully will be satisfied falsely. **Critical — must be deleted, not softened.**

3. **`new-agent.md` §9 instructs a new employee to write internal information into agent files.** *"Anything the hire learns internally that fills an open question gets written to `knowledge/internal/`."* This is unclassified internal-data capture inside a regulated firm, authorized by nobody, with no policy behind it — and the confidentiality policy template (pack §14) is empty. **Critical — must be removed from V1 entirely.**

**The fair counterweight:** `new-agent.md` contains four genuinely valuable contributions that the knowledge pack lacks and `core/` does not provide — the tiered-source discipline, the three-part unknown-answer response, mode routing, and the observation that one knowledge layer can serve multiple roles via different skills layers. These survive scrutiny and should be kept. The problem with the old plan is not its ideas; it is that its verified facts, its unverified facts, its industry generalizations, and its inventions are all typeset identically.

**Overall verdict on `new-agent.md`:** roughly 30% reusable as-is, 40% reusable after rewriting, 30% must be discarded. The detail is seductive and mostly ungrounded — its precision is presentational, not evidentiary. Detail is not evidence.

---

## B. What the primary knowledge pack establishes

### B1. What it clearly establishes [V]

**Verified public facts it commits to:**

| Claim | Where |
|---|---|
| Wealth platform / AI-forward custodian for independent advisors & RIAs | §Company overview |
| Mission: make independent financial advice better, more affordable, more accessible | §Company overview |
| 6,000+ advisors | §Customer and product context |
| 25+ integrations (CRM, financial planning, custodial AI workflows) | §Customer and product context |
| Product surface: account creation, transfers/ACATs, billing, reporting, integrations, client portal, custody, model marketplace, high-yield cash, trading | §Customer and product context |
| Hazel = publicly marketed AI platform; draws on real-time custodial data + CRM, email, notes | §Customer and product context |
| "Many firms are up and running in about 30 days" | §Onboarding and operating model |
| Clients receive a dedicated onboarding manager | §Onboarding and operating model |
| Public arc: join & set firm preferences → onboard clients → configure portfolios/fees/integrations → go live | §Onboarding and operating model |
| Core values: **Kindness, Brilliance, Grit** | §Company values and culture |
| Offices: Los Angeles, San Francisco, Dallas | §Company values and culture |

Note the *shape* of these facts: qualitative, hedged, attributed to public positioning. No funding figures, no founder, no entity structure, no dated announcements, no market-share numbers. That restraint is the document's central discipline, not an oversight.

### B2. Boundaries it enforces [V]

**Must-not-pretend-to-know list** (§Agent behavior guidance): internal tools or URLs; names of managers or teammates; security procedures; internal policies or handbook details; exact first-week meeting schedule; private architecture, prompts, permissions, or customer data flows; compensation and benefits beyond public careers copy.

**Guardrails**: always separate public facts from unknown internal information; never fabricate internal processes, tools, employee names, org structures, policies; short structured answers; beginner-friendly finance explanations; when uncertain, name the *source category* needed; no compliance/legal/operational instructions absent verified internal files; **treat public marketing copy as positioning, not proof of internal process**.

That last guardrail is the most under-appreciated line in the pack, and it is the line `new-agent.md` breaks most often.

**Escalation categories**: access setup, payroll/benefits specifics, security/compliance instructions, team structure, role-specific expectations, manager-specific priorities, legal/policy questions.

### B3. What internal knowledge is explicitly missing [V]

Six template files, all marked *"Status: unknown externally"*: org chart (§7), internal tools (§8), day-one process (§9), people and contacts (§10), policies and compliance (§11), role-specific ramps (§12).

Read against `new-agent.md`, this list is devastating: templates 7, 10, 11 and 12 are precisely the knowledge the old plan's curriculum, enforcement rule 5, and stakeholder role-play all assume exists.

### B4. What it implies about the agent's role inside a HarperOS-style system [I]

The pack never names the five layers, but it maps onto them cleanly:

- **Knowledge** — explicit (public facts + internal templates + glossary)
- **Skills** — one procedure only: the `/onboard` day-one flow, 7 steps
- **Tools** — silent
- **Feedback** — silent
- **Enforcement** — present as prose only, in the Guardrails section

So the pack is a **strong knowledge layer, a thin skills layer, and no tools/feedback/enforcement layer**. `core/`'s fill order (knowledge → skills → tools → feedback → enforcement) says that is the correct place to be stalled. The pack stopped exactly where it ran out of verifiable material, which is the disciplined failure mode.

**The intended role, stated plainly [I]:** a *bounded public-knowledge orientation assistant* whose most important behavior is accurate refusal. Not a coach, not a trainer, not a compliance advisor.

### B5. Weaknesses in the pack itself (it is not above audit)

- **No source URLs, no per-fact retrieval dates.** "Public-source notes" is one paragraph. Nothing in the pack can be re-verified or aged out. **[M]**
- **Escalation rules name categories, not checkable triggers.** `core/`'s checklist: *"No entry in section 11 depends on the agent's subjective confidence."* "When asked about team structure" is closer to a topic than a trigger. **[M]**
- **The 12-file structure conflicts with `core/`'s one-domain-one-CLAUDE.md rule** and bypasses the decidability checklist, which is written against the template. **[M]**
- **Values (Kindness/Brilliance/Grit) are stated but not operationalized.** Under `core/`'s test — *could an agent act differently because this line exists?* — as written, no.
- **No stated operator model.** Who deploys this: the hire, HR, or the manager? Unaddressed, and it determines the entire tools/state/PII posture. **[M]**

---

## C. Critical review of the old plan

Classified into the four requested buckets. Section references are to `new-agent.md`.

### Bucket 1 — Supported by the primary knowledge pack

| Item | § | Note |
|---|---|---|
| Public-information-only constraint | §3 | Matches pack exactly; the framing "a feature, not an apology" is a genuine improvement in tone |
| Never guess at internal knowledge | §3, §10.1 | Direct restatement of pack guardrail |
| Anti-goal: polished confident generic answers harm a new hire | §1 | The best sentence in the document. Operationalizes the pack's core anxiety |
| Empty `knowledge/internal/` placeholder | §4 | Structurally identical to the pack's six `_TEMPLATE` files |
| Known-unknowns list (`09-open-questions.md`) | §5E | Maps to `core/` CLAUDE.md §12; correctly refuses to guess |
| 6,000+ advisors; 25+ integrations | §5A | Only two numeric claims in the old plan that the pack independently corroborates |
| Product surface (broad strokes) | §5A | Overlaps the pack, but with added specifics — see Bucket 3 |
| Glossary need | §4, §7 | Pack §6 requests the same; `core/` calls vocabulary the highest-value section |
| Open decision: "one hire or repeatable system?" | §14.3 | Correct question, and the pack implies the answer (a reusable knowledge structure) |

### Bucket 2 — Reasonable extension of the primary knowledge pack

These are not in the pack but are compatible with it and with `core/`.

| Item | § | Why it survives |
|---|---|---|
| **Tier A/B/C/D source classification with dates** | §5 | Refines `core/`'s 3-state tagging with source *class*. Compatible if mapped onto core's vocabulary rather than replacing it (see H3) |
| **Three-part unknown-answer response** (public / assumption required / exact question + who to ask) | §3 | The single most valuable transplant in the document. The pack's escalation rules are a topic list; this makes them a *procedure*. Correctly identified by the old plan as the highest-value output |
| **Named mode routing** | §8 | Real fix for real drift; maps onto `core/skills/` one-file-per-procedure |
| **One knowledge layer, forked skills per role** | §2 | Precisely `core/`'s nouns/verbs separation, arrived at independently. Strong signal |
| **Profile capture in session one** | §2 | Legitimate — this is user-supplied, not fabricated. Creates a storage obligation, not a truth problem (see F7) |
| **State layer** (`profile` / `progress` / `gap-log`) | §4, §9 | `core/` has **no** state layer. Genuine gap for any longitudinal agent. Must be declared as an extension to core, not smuggled in |
| **Eval layer** (checkpoints) | §4 | `core/feedback/` is backward-looking (human corrections); checkpoints are forward-looking assessment. Complementary, not duplicative |
| **Assessment format: strong → vague → unsafe assumption → missed stakeholder → rewrite → harder follow-up** | §10.3 | Fixed and checkable. Better engineered than the rest of §10 |
| **Research queue, priority-ordered** | §12 | The mechanism that could actually retire the unverified facts. Reusable as a validation backlog |
| **Curriculum clock keyed to start date** | §7 | Structure, not fact-claims. Ungrounded but low-risk |

### Bucket 3 — Assumption that requires validation

Not wrong — **unverified inside this repository**, and stated with a confidence the sourcing does not carry.

| Item | § | The problem |
|---|---|---|
| Founded 2018 by Jason Wenk; HQ Culver City | §5A | Absent from pack. Pack lists LA/SF/Dallas. Marked Tier A but no URL, no retrieval date |
| **Four-entity structure table** (Corp / LLC / Financial LLC / Advisors LLC) with regulator mapping | §5A | Highest blast radius in the document. Marked *"a new hire must know this on day one"* — so it is designed to be repeated aloud in a regulated firm. Zero in-repo verification path |
| Series F $152M, ~$1.9B valuation, ~$602M raised, named investors | §5B | Tier B. Volatile financial data hardcoded as values — `core/` blocking check: *"No volatile data hardcoded"* |
| AUM tripled two years; T3 market share 2.85% → 6.25%; All-Star categories | §5B | Tier B, precise, unverifiable here, ages fast |
| Third-largest custodian by RIA count (Nov 2025) | §5B | Ranking claim; ages fast; competitive-sensitive if repeated |
| Named enterprise clients (Ritholtz ~$6B, Bryn Mawr/WSFS, Sowell, Gerber Kawasaki) | §5B | Named third parties with dollar figures. Wrong = embarrassing externally |
| SSG acquisition, +1,600 advisors; Altruist Clearing launch ~2024 | §5B | Unverified in repo |
| Hazel dates (Sept 9 2025 launch, Nov 18 2025 custodial unification, Feb 10 2026 tax) | §5C | Pack corroborates only the *capability*, never the dates or the "first AI platform to…" claim |
| Thyme (YC) acquisition as Hazel's basis | §5C | Absent from pack |
| Hazel pricing $60/seat/mo, $600/yr; works for advisors custodying elsewhere | §5C | Volatile commercial data hardcoded |
| ~1,600 RIA firms subscribed in four weeks (Mar 2026) | §5C | Tier B trade press, highly perishable |
| Regulatory posture: SEC/FINRA/OCC, 53 states, SIPC + Lloyd's excess, Customer Protection Rule segregation, Asset Protection Guarantee | §5A | Marked Tier A. **The most dangerous unverified block** — a new hire repeating a wrong coverage or guarantee detail to an advisor is a real incident |
| "30+ account types", "500+ models", margin/SBLOC/fully-paid lending, personalized indexing, alternatives, options | §5A | Specificity inflation over the pack's unnumbered product list |
| Advisor segments Breakaway / Established / Enterprise | §5A | Plausible; absent from pack; drives the old plan's "which segment?" framing |
| Onboarding milestones at **day 5 / day 15 / day 30** | §5A | Pack says "about 30 days" and describes unnumbered stages. The old plan adds day numbers. Textbook specificity inflation |
| Headcount ~857 (Tier C) | §15 | Correctly tiered; still, employee-count data in an onboarding agent invites org questions it cannot answer |

**Systemic defect across this entire bucket:** the tier labels are applied to *paragraphs and sections*, never to individual facts, and there is not one URL in the document. A tier without a resolvable source is a confidence marker with nothing behind it — it makes claims *look* audited without being auditable. This is more dangerous than no tiering at all, because it suppresses the reader's skepticism.

### Bucket 4 — In conflict with the knowledge pack, or too speculative

| Item | § | Verdict |
|---|---|---|
| **Enforcement rule 5: name who would need to approve a compliance-touching change** | §10.5 | **Direct conflict.** Pack forbids compliance/operational instruction absent verified internal files, and forbids inventing names/org structure. The org chart is an empty template. Rule mandates fabrication. **Delete.** |
| **§9: hire writes internal learnings into `knowledge/internal/`** | §9, §7 | **Direct conflict + unmanaged risk.** Unclassified internal-data capture, no approval gate, no retention policy, no authority. **Delete from V1.** |
| **§10 framed as "Enforcement"** | §10 | **Conflicts with `core/enforcement/gates.md`.** All six items are prompt text = requests. Rename to `policy/behavioral-rules.md`; build real enforcement separately |
| **§5D Tier D: "custodial data correctness is the moat… the sentence a new engineer should internalize in week one"** | §5D | Tier label is correct discipline; the *instruction to internalize an inference as conviction* undoes it. Teaching a labeled guess as a week-one belief is how confident fabrication enters a human. Keep the analysis, delete the instruction |
| **Hazel architecture claim: "architectural rather than algorithmic — clean, permissioned custodial data underneath"** | §5C | Conflicts with pack §5's explicit boundary: *"do not infer internal model stack, evaluation methods, prompt architecture, or permissions."* Analyst attribution does not cure it |
| **"No training on customer data"** stated as commitment | §5C | Pack: *treat public marketing copy as positioning, not proof.* A security/data-handling assurance repeated by a new hire to a client is a compliance event. Must carry an explicit "public statement, not verified control" wrapper |
| **§1 success criteria: 3–6 months → 30 days** | §1 | Unsourced baseline, unsourced target, no measurement instrument. Aspiration presented as spec |
| **§11 scoring bars (Day 7 ≥3.0; Day 30 ≥4.0 no axis <3; Day 60 ≥4.0 no axis <4)** | §11 | Invented numbers with no calibration data. False precision on a human-assessment scale |
| **Day-90 milestone: "onboard the next new hire"** | §1 | Assumes org practice the agent cannot know |
| **§6 Layer 2 failure modes** (ACAT rejects, corporate actions mid-rebalance, T+1 breaks, sweep reconciliation, fee-billing error replication, RMD deadlines, wash sales, performance disagreement) | §6 | **Salvageable but mislabeled.** These are credible *industry* failure modes. Presented in-context they read as claims about Altruist's systems. Reframe as an industry primer with an explicit "not a claim about Altruist" header |
| **§6 Layer 3 AI risks** | §6 | Mostly safe — framed as open questions, not assertions. Keep, but strip any implication the agent knows where Hazel's approval gate sits |
| **§7 Week-3 engineering syllabus** (idempotency, reconciliation, audit trails, observability) | §7 | Generic good practice; no Altruist grounding; assumes an engineering hire |
| **§13 hour estimates (3h / 4h / 2h / 1.5h…)** | §13 | False precision. Harmless, but symptomatic of the document's habit of dressing guesses as plans |
| **Tool roadmap: "Later: internal doc sources, calendar, Slack"** | §4 | Conflicts with `core/tools/access-policy.md`: access decided before connecting, worst-case column mandatory. Naming future integrations without worst-case analysis is how over-granting starts |
| **Web search as a standing tool** | §4 | Justified reasoning (staleness), unmanaged consequence: retrieved content enters answers at runtime with **no tier assignment rule**. The tiering system covers the fact base and silently exempts live retrieval — its largest hole |

### C-extra: what the old plan silently dropped

`new-agent.md` contains **zero** culture or values content. Kindness / Brilliance / Grit, the benefits messaging, and the office locations are among the **best-verified material in the pack** and are directly relevant to a first-week hire. The old plan replaced the verified-and-soft with the unverified-and-hard. That trade is the document's character in miniature. **[V] — restore.**

---

## D. Direct comparison: alignment vs conflict

### D1. Where the old plan strengthens the pack's direction

1. **Turns refusal into a product.** The pack says "acknowledge the gap and point them to the correct internal source." The old plan's three-part response makes refusal *productive* and teaches a transferable professional habit. This is a real upgrade and should be adopted. **[O → adopt]**
2. **Names the drift problem.** *"Left unrouted, models drift into whatever mode the previous message resembled."* True, and the pack's single linear `/onboard` flow has no answer for it. **[O → adopt]**
3. **Sees the reuse argument.** §2's "one knowledge base, different skills layer per role" independently reaches `core/`'s nouns/verbs rule. **[O → adopt]**
4. **States the anti-goal.** A confident generic agent actively harms a hire in a regulated firm. Sharper than anything in the pack. **[O → adopt as design principle]**
5. **Adds a time dimension.** The pack is a day-one artifact; onboarding is a 90-day process. Recognizing that is correct even if the specific curriculum is ungrounded. **[O → adopt shape, discard content]**

### D2. Where it usefully adds structure

- Source tiering (needs per-fact application + URLs)
- Explicit state files — closes a real gap in `core/`
- Eval checkpoints — closes a second real gap in `core/`
- Fixed assessment format — checkable
- Prioritized research queue — becomes the validation backlog
- `knowledge/internal/` as a designed seam rather than a retrofit

### D3. Where it overreaches

- **Fact density without source density.** ~40 specific claims, 0 URLs, 0 per-fact dates.
- **Numeric precision without calibration.** Scoring bars, hour estimates, day-numbered milestones.
- **Outcome promises.** 3–6 months → 30 days; day-90 peer onboarding.
- **Architecture inference about Hazel**, against an explicit pack boundary.
- **Regulatory detail** stated with a certainty its sourcing cannot support.

### D4. Where it introduces risk

| Risk | Mechanism | Severity |
|---|---|---|
| Hire repeats wrong regulatory/coverage detail | §5A stated Tier A, unverified, taught as day-one material | **Critical** |
| Agent invents an approver | §10.5 requires naming approvers with no org data | **Critical** |
| Unclassified internal data captured into files | §9 capture loop, no gate, no policy | **Critical** |
| Hire repeats "no training on customer data" as a control | §5C marketing claim presented as commitment | High |
| Stale financials asserted as current | §5B hardcoded volatile values | High |
| Runtime web results bypass the tier system | §4 web search with no retrieval-tier rule | High |
| Industry failure modes read as Altruist-specific | §6 Layer 2 framing | Medium |
| Manager/stakeholder names sit in an unpoliced file | §2 profile capture, no storage policy | Medium |
| Assessment scores treated as meaningful | §11 uncalibrated bars | Medium |

### D5. Where it assumes internal access or operational certainty it has not justified

- **Stakeholder role-play** (§4, §8) — playing "compliance partner" or "staff engineer" requires internal norms the pack marks unknown. As written, the agent improvises internal culture and the hire cannot tell simulation from information.
- **Meeting prep for real calendar meetings** (§7 Week 4) — presumes calendar access (not granted) and knowledge of internal meeting norms (unknown).
- **"Trace an end-to-end workflow and name where it breaks"** (§1 Day 14) — break points in *Altruist's* systems are internal. Only defensible as an industry-generic exercise, explicitly labeled.
- **"Which regulator cares about which system, and who has to approve a change"** (§5A) — approval chains are listed in the old plan's own known-unknowns (§5E) and then relied on anyway. Internal contradiction.
- **Week-3 role branches** (§7) — presumes role-specific ramps; pack template 12 is empty.

### D6. Salvageable if rewritten

| Old plan item | Rewrite condition |
|---|---|
| Fact base §5 | Split by verification state: pack-corroborated / URL-cited-and-dated / **quarantined pending validation**. Nothing enters the agent's answerable set from the third bucket |
| Enforcement §10 | Rename to policy; delete rule 5; move the enforceable residue into access limits + a validator |
| Failure modes §6 L2 | Relabel "Industry primer — general custody/brokerage operations. Not claims about Altruist systems or incidents" |
| Curriculum §7 | Keep the clock; replace content with pack-supported material; gate role branches on the internal templates being filled |
| Stakeholder role-play | Restrict to a single generic-industry persona with a persistent simulation banner, or defer past V1 |
| Assessment §11 | Keep the fixed format; delete numeric bars until real data exists |
| Research queue §12 | Becomes `knowledge/validation-backlog.md`, the source of truth for what is still quarantined |
| Tier system §5 | Map onto `core/` tags; add mandatory per-fact URL + retrieval date; add a rule for live-retrieved content |

---

## E. HarperOS foundation analysis by layer

`core/` fill order is fixed: **knowledge → skills → tools → feedback → enforcement**. Assessed per layer.

### E1. Knowledge — *what the agent knows (nouns)*

**Exists [V/I]:** `core/knowledge/CLAUDE.md` (12-section template, identical to `dedicated-knowledge/assets/CLAUDE-template.md`); the `dedicated-knowledge` skill with its extraction schema (12 categories), 13-point scored quality checklist, and discovery questions. The knowledge pack supplies real content for a large part of it.

**Section-by-section mapping of the pack onto `core/`'s template [I]:**

| `core/` CLAUDE.md § | Fit for an onboarding agent | Source |
|---|---|---|
| 1 What this company does | Direct fit | Pack §Company overview **[V]** |
| 2 Vocabulary | **Highest value.** Direct fit | Pack §6 glossary + `core/` "single highest-value section" **[V]** |
| 3 People and authority | **Empty by necessity** — must ship as `[MISSING]` with routing slots | Pack §7, §10 templates **[M]** |
| 4 Products and services | Fits as *public product surface*; pattern not catalog | Pack §2 **[V]** |
| 5 Customers and segments | RIA segmentation — public framing only | Pack §Company overview; old plan's Breakaway/Established/Enterprise is **[O]** |
| 6 The process this agent owns | Scope/triggers/handoffs of the onboarding conversation. Steps go to skills | `core/` nouns-vs-verbs rule **[I]** |
| 7 Decision rules | **Repurposed**: routing and refusal rules, not business rules | **[M]** |
| 8 Sources of truth | **Repurposed and critical**: when public info conflicts with what the hire heard internally, *internal wins and the agent stops asserting* | **[M]** |
| 9 Output standards | Answer shape: short, structured, beginner-friendly + a verbatim worked example of a good refusal | Pack §Guardrails **[V]**, example **[M]** |
| 10 Hard constraints | Direct fit — pack's must-not-pretend list is already absolute | Pack §Agent behavior guidance **[V]** |
| 11 Escalation | Fits, but pack's categories must become checkable triggers | Pack §Escalation rules **[V]** + **[M]** |
| 12 Open questions | Direct fit — the six templates + old plan §5E | Pack §7–12 **[V]** |

**Weak or missing:**
- No source registry; no fact is re-verifiable. **[M]**
- No staleness policy that executes. **[M]**
- §3, §7, §8 unfilled — and §8 is the layer's sharpest hidden gap.
- The pack's 12-file structure has not been reconciled with the one-CLAUDE.md rule.

**Reusable from `new-agent.md`:** tier vocabulary (remapped), `knowledge/internal/` seam, open-questions list, glossary ambition, culture content **absent — restore from pack**.

**Ignore/downgrade/rewrite:** all of §5B and §5C dated specifics → quarantine pending URL verification; §5D "internalize" instruction → delete; regulatory block §5A → quarantine at highest priority; Hazel architecture inference → delete.

### E2. Skills — *what the agent does (verbs)*

**Exists [I]:** `core/skills/_TEMPLATE.md` — Owns / Triggered by / Knowledge required / Steps (Do, Done when, If it fails) / Stop conditions / Output / Known gaps. Rule: *facts live in knowledge, not here.*

The pack supplies exactly one procedure (the 7-step `/onboard` flow). It is a good candidate but is written as narrative, not as trigger + done-criteria + failure branch.

**Weak or missing:**
- **No `answer-or-refuse` skill** — the single most important verb this agent has, and neither document renders it as a procedure with a done-condition. **[M]**
- No stop conditions anywhere. `core/`: *"'when unsure' is not a stop condition."* **[M]**
- No session-zero / returning-user handling (empty state, day-45 restart). **[M]**

**Reusable from `new-agent.md`:** the three-part unknown-answer response (becomes the `answer-or-refuse` skill body — highest-value transplant in this audit); mode naming; `explain` and `trace` as skill files; question-generator (safe — it produces questions, not answers).

**Ignore/downgrade/rewrite:** `stakeholder-roleplay` → defer past V1; `meeting-prep` → defer (assumes calendar + internal norms); `assess` → keep the format, drop the bars; `curriculum` → keep the clock, gate the content.

### E3. Tools — *what the agent can touch*

**Exists [I]:** `core/tools/access-policy.md` — Granted / **Explicitly withheld** / worst-case column ("If you can't fill it in, don't grant the access yet") / read-before-write / least privilege / irreversible needs a human / external needs a human / credential ownership and revocation.

**Weak or missing:** **the layer is entirely unfilled for this agent.** The knowledge pack is silent on tools. `new-agent.md` grants web search and file read/write in a single line with no worst-case analysis and roadmaps Slack and calendar — the exact over-granting the policy exists to prevent. **[M]**

**Reusable from `new-agent.md`:** the *reasoning* for web search (Altruist ships fast; a frozen fact base rots) is sound and should survive into the policy's "why it's needed" column.

**Rewrite:** the "Explicitly withheld" table is where the real value sits here and neither document has one. Withholding internal systems, send capability, and write access outside `state/` is **available enforcement on day one at zero engineering cost** — the strongest control in the entire design (`core/`: absence of access is the strongest kind).

### E4. Feedback — *how corrections flow back*

**Exists [I]:** `core/feedback/corrections.md` — two loops (within-run validation; across-run human correction), a correction log with a mandatory "Fixed in" column, four root-cause categories (missing knowledge / wrong rule / bad step / out of scope), weekly review, repeat-detection, and ownership by the *process owner*, not the builder.

**Weak or missing:**
- Neither document has a correction log. **[M]**
- **The owner question is unanswerable today** because the operator model is undefined. A new hire cannot own the correction loop for facts they cannot verify — they are the least-equipped person in the building to do it. Someone internal must own it. **[M]**

**Reusable from `new-agent.md`:** `gap-log.md` with dated entries and scheduled retests — but note it tracks *the hire's* gaps, not *the agent's* errors. These are different loops and the old plan conflates them. Keep both, separately.

### E5. Enforcement — *what the agent structurally cannot do*

**Exists [I]:** `core/enforcement/gates.md` (four kinds: absence of access, validation, approval gates, audit trail), `rules.json` (worked example from the fictional Meridian Abrasives client — explicitly to be replaced), `validate.py` (required/forbidden/threshold checks; **fails closed** on unevaluable rules; exit 0/1).

**Weak or missing — this is the layer with the deepest structural gap [I]:**

`validate.py` validates **a file before it is sent**. An onboarding agent's output is **conversational**, with no pre-send artifact. The shipped enforcement mechanism does not map onto this agent's output shape, and **neither document notices**. Left unaddressed, this agent ships with prose guardrails only — i.e. requests.

**Reusable from `new-agent.md`:** almost nothing *as enforcement*. §10.1 and §10.3 are good policy; §10.5 must be deleted.

**The fix — three enforcement mechanisms that actually run [I/M]:**

1. **Absence of access** (available immediately, strongest, free): no internal systems, no send capability, write access limited to `state/`. Fill the "Explicitly withheld" table and this is real on day one.
2. **Knowledge-base linting** — repoint `validate.py` from agent output to the **knowledge files at build time**. This is a genuine and immediate use of the shipped validator:
   - `required`: every knowledge file carries `Source:` and `Last verified:` lines
   - `forbidden`: quarantined-fact markers appearing in a shipped file
   - `forbidden`: banned assertion patterns (`your manager is`, `the internal wiki`, `you should ask <name>`, tool names outside an allowlist)
   - `forbidden`: `[MISSING]`/`[ASSUMED]` tags absent from files whose §3 is unfilled
   A build-time gate on the knowledge layer is worth more than a runtime gate on chat, because **this agent's failure mode is knowledge-borne, not phrasing-borne.**
3. **Approval gate**: any write to `knowledge/internal/` requires a named human. In V1 the simpler control is to **not build the path at all**.

*Honest limitation:* regex cannot reliably detect "an untagged specific number." Rules 1 and 3 above are robustly checkable; the banned-pattern list is a floor, not a ceiling. Say so in the gate table rather than overclaiming — `core/`: *"Don't let a passing validator become a reason to stop reading the output."*

### E6. Two layers `core/` does not have [O/M]

`state/` and `evals/` are real gaps in `core/` for any longitudinal, teaching, or multi-session agent. `new-agent.md` identified both. They should be added as **explicitly declared extensions**, documented as such — not folded in silently, or the next deployment inherits an undocumented divergence from the master scaffold.

---

## F. Gaps, holes, and risks

Consolidated. Each carries a trust label and the layer that owns it.

**F1. Factual overreach — `new-agent.md` §5** *(knowledge)* **[O]**
~40 specific claims, 0 URLs, 0 per-fact dates. Highest-consequence subset: regulatory posture, entity structure, funding, named enterprise clients, Hazel pricing and dates.
*Why it matters:* this agent's output is repeated aloud by a new hire in a regulated firm. Errors do not stay inside the chat.

**F2. Missing source discipline — both documents** *(knowledge)* **[M]**
Neither can be re-verified. The pack has one closing paragraph; the old plan has a bulk list at §15. Tiering without resolvable sources is worse than no tiering — it manufactures unearned confidence.

**F3. Live retrieval bypasses the tier system** *(tools + knowledge)* **[O]**
Web search is granted with no rule for classifying retrieved content. The tier discipline covers the static fact base and silently exempts everything arriving at runtime.

**F4. Role-boundary gaps** *(knowledge §10 / policy)* **[M]**
Undeclared: employment/HR advice, compensation, immigration/visa, legal, medical/benefits, "is my manager being reasonable", performance concerns, anything about colleagues. A first-days assistant will be asked several of these in week one. The pack covers compensation and policy; the rest is absent from both documents.

**F5. Weak escalation design** *(knowledge §11)* **[V→M]**
Pack lists topic categories; `core/` demands checkable triggers with a routing target. With the org chart empty, routing targets do not exist — so the design must escalate to a **role slot** (`[MISSING: HR contact — see 13_people_and_contacts]`) and say plainly that it does not know who fills it. Neither document does this.

**F6. Missing state logic** *(state)* **[O/M]**
No definition of: where state lives, who can read it, retention, what happens on empty state, or on a returning user mid-curriculum. `new-agent.md` names the files but not their lifecycle.

**F7. PII in state** *(tools + policy)* **[M]**
§2 captures manager and stakeholder names. Legitimate to capture, unmanaged to store. Employee-relationship data in an unpoliced file inside a regulated firm, with the confidentiality policy template empty.

**F8. Missing evaluation logic** *(evals)* **[O/M]**
Checkpoints are named; model answers are not written; the bars are invented. And there is **no evaluation of the agent itself** — only of the hire. The higher-value eval is: *given 20 questions, how often does it correctly refuse rather than answer?* Neither document proposes it.

**F9. Missing enforcement logic** *(enforcement)* **[M]**
Covered in E5. The shipped mechanism does not fit the output shape; the old plan's "enforcement" is prose.

**F10. Workflow gaps** *(skills)* **[M]**
No session-zero, no returning-user path, no conflict path (hire says something contradicting a public fact), no "user asks the same blocked question three times" path, no wind-down when the curriculum ends.

**F11. Undefined operator model** *(all layers)* **[M]**
Hire-deployed, HR-deployed, or manager-deployed? Determines tools, state, PII, correction ownership, and whether the internal templates ever get filled. **This is the single unanswered question that most constrains the build.**

**F12. Unresolved architecture** *(all layers)* **[M]**
Three folder structures, no reconciliation. Resolved in H.

**F13. Where the old plan sounds smart but produces an unsafe agent**

| Sounds smart | Actually produces |
|---|---|
| "Name who would need to approve" (§10.5) | An invented approver, stated with authority, in a compliance context |
| "Entity structure — must know on day one" (§5A) | A hire confidently repeating unverified regulatory structure in a meeting |
| "Custodial data correctness is the moat — internalize it week one" (§5D) | A labeled inference converted into a stated conviction |
| "Trace the workflow and name where it breaks" (§1, §8) | Industry-generic failure modes mistaken for knowledge of Altruist's systems |
| "Stakeholder role-play: compliance partner" (§8) | Improvised internal culture the hire cannot distinguish from information |
| "Hire writes internal learnings into knowledge/internal/" (§9) | Unclassified internal data captured with no authority or gate |
| "Day 30 ≥ 4.0, no axis below 3" (§11) | A precise-looking readiness signal with nothing calibrating it |
| "No training on customer data" (§5C) | A marketing statement repeated by an employee as a technical assurance |

---

## G. What to keep, rewrite, discard

### Keep as-is

| Item | Source | Label |
|---|---|---|
| Five-layer scaffold and fixed fill order | `core/` | **[I]** |
| Nouns-vs-verbs separation | `core/README.md` | **[I]** |
| Confidence tags (untagged / `[ASSUMED]` / `[MISSING]`) | `core/` | **[I]** |
| Decidability test | `dedicated-knowledge/SKILL.md` | **[I]** |
| 13-point quality checklist + adversarial pass | `core/` | **[I]** |
| "If it can be talked out of it, it isn't enforcement" | `core/enforcement/gates.md` | **[I]** |
| Access decided before connecting; worst-case column | `core/tools/` | **[I]** |
| Correction isn't finished until it's in the knowledge | `core/feedback/` | **[I]** |
| All verified public facts | Pack | **[V]** |
| Must-not-pretend-to-know list | Pack | **[V]** |
| Guardrails, incl. marketing-copy-is-positioning | Pack | **[V]** |
| Six internal templates as empty files | Pack | **[V]** |
| Kindness / Brilliance / Grit + culture content | Pack | **[V]** |
| Three-part unknown-answer response | `new-agent.md` §3 | **[O]** |
| Anti-goal (confident generic answers harm the hire) | `new-agent.md` §1 | **[O]** |
| One knowledge layer, forked skills per role | `new-agent.md` §2 | **[O]** |
| Named mode routing | `new-agent.md` §8 | **[O]** |
| Fixed assessment format (no praise for weak answers) | `new-agent.md` §10.3 | **[O]** |

### Rewrite

| Item | Rewrite into |
|---|---|
| Pack's 12-file knowledge structure | One `knowledge/CLAUDE.md` (operative, decidable) + reference files behind it; templates stay separate as `knowledge/internal/` |
| Pack's escalation categories | Checkable triggers with `[MISSING: role]` routing slots |
| Pack's `/onboard` narrative flow | `skills/onboard.md` in `_TEMPLATE.md` form: triggers, done-criteria, failure branches, stop conditions |
| Old plan tier system | Per-fact tags with mandatory URL + retrieval date; mapped onto `core/` tags; plus a rule for live-retrieved content |
| Old plan §5B/§5C fact blocks | `knowledge/quarantine.md` — present but **not answerable** until each fact carries a source. Promotion is a deliberate act |
| Old plan §5A regulatory block | Quarantine at highest priority; never taught before verification |
| Old plan §6 Layer 2 | `knowledge/industry-primer.md` with an explicit "not a claim about Altruist" header |
| Old plan §10 | `policy/behavioral-rules.md` (prose, honestly labeled) + real controls in `tools/` and `enforcement/` |
| Old plan §12 research queue | `knowledge/validation-backlog.md` — the promotion pipeline out of quarantine |
| Old plan curriculum | Keep the clock; content limited to verified material; role branches gated on internal templates being filled |
| `validate.py` usage | Repoint from agent output to **build-time knowledge-file linting** |

### Discard

| Item | Reason |
|---|---|
| Enforcement rule 5 (name the approver) | Mandates fabrication; conflicts with pack |
| §9 internal-knowledge capture loop | Unauthorized internal-data capture; no gate, no policy |
| §5D "internalize it week one" instruction | Converts labeled inference into taught conviction |
| Hazel architecture inference | Explicit pack boundary violation |
| §11 numeric scoring bars | Uncalibrated invention |
| §13 hour estimates | False precision |
| §1 3–6 months → 30 days claim | Unsourced both ends, unmeasurable |
| Day-90 "onboard the next hire" | Assumes unknown org practice |
| Calendar / Slack on the tool roadmap | No worst-case analysis; violates access policy |
| `stakeholder-roleplay` and `meeting-prep` in V1 | Both require internal norms marked unknown |
| Day 5 / 15 / 30 milestone numbers | Specificity inflation over "about 30 days" |

---

## H. Proposed target folder/file architecture

### H1. Principles

1. `core/` stays the **blank master**; the Altruist agent is a *deployment copy* (`README.md` step 1: *"Don't fill files in place here"*).
2. `core/`'s five layers are the top-level contract. `state/` and `evals/` are added as **declared extensions**.
3. **Reusable HarperOS logic vs Altruist-specific knowledge** separate at the top level.
4. **Verified public knowledge vs future internal knowledge** separate inside the knowledge layer, with a **quarantine tier** between them for the old plan's unverified specifics.
5. One operative `knowledge/CLAUDE.md`; reference files behind it. The decidability checklist is written against the template, and loose files bypass it.

### H2. Target structure

```
harperOS/
├─ core/                                    ← unchanged blank master
│  ├─ knowledge/ skills/ tools/ feedback/ enforcement/
│  └─ EXTENSIONS.md                         [M] documents state/ + evals/ as
│                                               sanctioned additions to the scaffold
│
├─ core-extensions/                         [M] reusable, client-agnostic
│  ├─ state/_TEMPLATE.md                        longitudinal agents
│  ├─ evals/_TEMPLATE.md
│  └─ knowledge/source-registry_TEMPLATE.md [M] URL + retrieval date + tier per fact
│
└─ deployments/
   └─ altruist-onboarding/                  ← the agent
      ├─ AGENT.md                           [M] identity, scope, mode routing,
      │                                         layer index. Facts live in knowledge
      ├─ knowledge/
      │  ├─ CLAUDE.md                       [V] operative layer, core's 12 sections
      │  ├─ public/
      │  │  ├─ 01-company-and-mission.md    [V] pack §Company overview
      │  │  ├─ 02-glossary.md               [V] pack §6 — highest-value file
      │  │  ├─ 03-product-surface.md        [V] pack §2, unnumbered claims only
      │  │  ├─ 04-customer-onboarding.md    [V] pack §3, "about 30 days"
      │  │  ├─ 05-culture-and-values.md     [V] Kindness/Brilliance/Grit
      │  │  ├─ 06-hazel-public.md           [V] capability only; no architecture,
      │  │  │                                   no dates, no pricing
      │  │  └─ 07-industry-primer.md        [O] general custody/brokerage ops.
      │  │                                      Header: NOT claims about Altruist
      │  ├─ quarantine.md                   [O] every unverified old-plan specific.
      │  │                                      Present, indexed, NOT answerable
      │  ├─ validation-backlog.md           [O] old plan §12, reordered by
      │  │                                      consequence. Promotion pipeline
      │  ├─ source-registry.md              [M] URL + retrieval date + tier per fact
      │  └─ internal/                       [V] the pack's six templates, empty
      │     ├─ 10-org-chart.TEMPLATE.md         Status: unknown externally
      │     ├─ 11-internal-tools.TEMPLATE.md
      │     ├─ 12-day-one-process.TEMPLATE.md
      │     ├─ 13-people-and-contacts.TEMPLATE.md
      │     ├─ 14-policies-compliance.TEMPLATE.md
      │     └─ 15-role-ramps.TEMPLATE.md
      ├─ skills/
      │  ├─ answer-or-refuse.md             [O] THE core verb. Three-part response
      │  ├─ onboard.md                      [V] pack's 7 steps, template form
      │  ├─ explain.md                      [O] teach then test
      │  ├─ glossary-lookup.md              [V]
      │  ├─ ask-better-questions.md         [O] produces questions, not answers
      │  └─ _deferred/                          role-play, meeting-prep, trace,
      │                                          curriculum — post-V1, gated
      ├─ policy/
      │  └─ behavioral-rules.md             [O] old plan §10 minus rule 5.
      │                                          Labeled: requests, not controls
      ├─ tools/
      │  └─ access-policy.md                [M] Granted + EXPLICITLY WITHHELD
      ├─ feedback/
      │  ├─ corrections.md                  [I] agent errors — core format
      │  └─ gap-log.md                      [O] hire's weak spots — separate loop
      ├─ state/
      │  ├─ profile.md                      [O] + retention/access header
      │  └─ progress.md                     [O]
      ├─ evals/
      │  ├─ refusal-suite.md                [M] 20 questions, expected refuse/answer.
      │  │                                      Evaluates the AGENT — highest value
      │  └─ checkpoints.md                  [O] format kept, bars removed
      └─ enforcement/
         ├─ gates.md                        [M] filled gate table
         ├─ rules.json                      [M] knowledge-file lint rules
         └─ validate.py                     [I] from core, repointed to build-time
```

### H3. Tag reconciliation (resolves the two competing systems)

`core/` tags express **verification state**. The old plan's tiers express **source class**. They are orthogonal — keep both, on every fact:

```
6,000+ advisors  [tier:A] [src:#altruist-home] [checked:2026-07-25]
Series F $152M   [tier:B] [QUARANTINE] [src:none] [checked:never]
Hazel model stack  [MISSING] — do not infer (pack §05 boundary)
Manager's name     [MISSING] — capture from user only; never assert
```

Rule: **no fact without a source id and a checked date is answerable.** That single rule converts the tier system from decoration into a control, and it is machine-checkable at build time.

### H4. What separates cleanly

| Reusable HarperOS core | Altruist-specific |
|---|---|
| Five layers + fill order | Every fact in `knowledge/public/` |
| Confidence tags, decidability test, checklist | The six internal templates |
| `_TEMPLATE.md` forms | Quarantine and validation backlog |
| `validate.py` | `rules.json` contents |
| `state/` + `evals/` templates | Curriculum, glossary, refusal suite |
| Three-part unknown-answer pattern | The specific routing slots |

The three-part unknown-answer pattern is the strongest candidate for promotion into `core/` itself — every public-knowledge-only agent needs it.

---

## I. Implementation plan by phase

### Phase 0 — Unblock (before any building)

| # | Action | Label |
|---|---|---|
| 0.1 | **Answer the operator question**: hire-deployed, HR-deployed, or manager-deployed | **[M]** |
| 0.2 | Decide whether internal templates will ever be filled, and by whom | **[M]** |
| 0.3 | Name the correction-loop owner — cannot be the new hire | **[M]** |
| 0.4 | Accept the target architecture (H2) and set up `deployments/altruist-onboarding/` | **[I]** |

*If 0.1 is unanswered, build Phase 1 anyway under the most restrictive assumption: hire-deployed, read-only, no internal capture, no PII beyond first name and role.*

### Phase 1 — Knowledge (highest value; `core/` mandates it first)

| # | Action | Priority | Label |
|---|---|---|---|
| 1.1 | Migrate all pack-verified facts into `knowledge/public/`, one source id + checked date each | **Critical** | **[V]** |
| 1.2 | Build `source-registry.md`; every fact resolves to a URL | **Critical** | **[M]** |
| 1.3 | Move **all** old-plan §5A regulatory, §5B, §5C specifics to `quarantine.md`, unanswerable | **Critical** | **[O]** |
| 1.4 | Write `CLAUDE.md` §10 (hard constraints) from the pack's must-not-pretend list, verbatim and absolute | **Critical** | **[V]** |
| 1.5 | Write `CLAUDE.md` §11 — checkable triggers with `[MISSING: role]` routing slots | **Critical** | **[V→M]** |
| 1.6 | Write `CLAUDE.md` §8 — internal beats public; on conflict the agent stops asserting | **High** | **[M]** |
| 1.7 | Build `02-glossary.md` (pack §6 terms + old plan's TAMP, sweep, fractional shares) | **High** | **[V]** |
| 1.8 | Create the six internal templates, empty, each headed `Status: unknown externally` | **High** | **[V]** |
| 1.9 | Restore culture/values content the old plan dropped | **Medium** | **[V]** |
| 1.10 | Write `07-industry-primer.md` from §6 L2/L3 with the "not about Altruist" header | **Medium** | **[O]** |
| 1.11 | Add role-boundary constraints: no HR, legal, compensation, immigration, medical, or colleague-related advice | **High** | **[M]** |
| 1.12 | Run the 13-point checklist + adversarial pass; **report the score honestly, weak or not** | **High** | **[I]** |

### Phase 2 — Skills

| # | Action | Priority | Label |
|---|---|---|---|
| 2.1 | `answer-or-refuse.md` — three-part response, `_TEMPLATE.md` form, stop conditions | **Critical** | **[O]** |
| 2.2 | `onboard.md` — pack's 7 steps with triggers, done-criteria, failure branches | **High** | **[V]** |
| 2.3 | Session-zero and returning-user paths | **High** | **[M]** |
| 2.4 | `glossary-lookup.md`, `explain.md` | **Medium** | **[V/O]** |
| 2.5 | `ask-better-questions.md` | **Medium** | **[O]** |
| 2.6 | Mode declaration rule in `AGENT.md` | **Medium** | **[O]** |
| 2.7 | Defer role-play, meeting-prep, trace, curriculum to `_deferred/` with gating conditions written down | **High** | **[O]** |

### Phase 3 — Tools

| # | Action | Priority | Label |
|---|---|---|---|
| 3.1 | Fill `access-policy.md` Granted table with the worst-case column completed | **Critical** | **[M]** |
| 3.2 | Fill **Explicitly withheld** — internal systems, send capability, write outside `state/`, Slack, calendar | **Critical** | **[M]** |
| 3.3 | Decide web search. If granted: mandatory tier assignment for retrieved content + "not in the verified base" disclosure | **High** | **[O]** |
| 3.4 | Credentials: owner, scope, revocation, logging | **Medium** | **[I]** |

### Phase 4 — Feedback

| # | Action | Priority | Label |
|---|---|---|---|
| 4.1 | Start `corrections.md` (agent errors, core format, "Fixed in" mandatory) | **High** | **[I]** |
| 4.2 | Start `gap-log.md` (hire's gaps) — keep the two loops separate | **Medium** | **[O]** |
| 4.3 | Weekly review cadence; assign the named owner from 0.3 | **High** | **[I]** |
| 4.4 | Wire `validation-backlog.md` into the loop: verified facts promote out of quarantine | **High** | **[O]** |

### Phase 5 — Enforcement (last, and separately — must hold when everything above is wrong)

| # | Action | Priority | Label |
|---|---|---|---|
| 5.1 | Fill the gate table in `gates.md` | **Critical** | **[M]** |
| 5.2 | Write `rules.json` as **knowledge-file lint rules**: `Source:` + `Last verified:` required; quarantine markers forbidden in shipped files; banned assertion patterns forbidden | **Critical** | **[M]** |
| 5.3 | Wire `validate.py` as a build-time gate over `knowledge/` | **Critical** | **[I]** |
| 5.4 | Record the regex limitation in `gates.md` — a pass is not a reason to stop reading | **High** | **[I]** |
| 5.5 | Approval gate for `knowledge/internal/` writes — or leave the path unbuilt in V1 | **Critical** | **[M]** |

### Phase 6 — Evals

| # | Action | Priority | Label |
|---|---|---|---|
| 6.1 | `refusal-suite.md` — 20 questions, expected refuse/answer, run before every release. **Evaluates the agent** | **Critical** | **[M]** |
| 6.2 | Adversarial set: questions engineered to bait an internal-knowledge answer | **High** | **[M]** |
| 6.3 | Hire-facing checkpoints — format only, no numeric bars | **Low** | **[O]** |

### Phase 7 — Post-V1, gated

Each item ships **only when its gate opens**:

| Item | Gate |
|---|---|
| Curriculum beyond week 1 | Verified role-specific content exists |
| Role branches | `15-role-ramps` filled by someone internal |
| Stakeholder role-play | Internal norms documented + persistent simulation banner |
| Meeting prep | Calendar access granted through a completed access policy |
| Internal-knowledge capture | Written data-classification policy + approval gate |
| Numeric assessment bars | Real scoring data from ≥5 hires |
| Quarantined facts promoted | URL + retrieval date + second-source confirmation each |

---

## J. Smallest strong V1

Following `core/`'s 30-minute doctrine — *narrow and finished beats broad and half-done.*

**Build exactly this:**

1. **`knowledge/CLAUDE.md`** with four sections filled properly:
   - **§2 Vocabulary** — the glossary. Highest-value section per `core/`, and 100% pack-supported.
   - **§10 Hard constraints** — the pack's must-not-pretend list, verbatim, absolute, plus the role-boundary additions (HR/legal/comp/immigration/medical/colleagues).
   - **§11 Escalation** — checkable triggers with `[MISSING: role]` slots.
   - **§12 Open questions** — the six internal templates, prioritized by consequence.
2. **`knowledge/public/`** — company/mission, product surface, onboarding arc, culture/values. Pack facts only. Every fact carries a source id and a checked date.
3. **`knowledge/quarantine.md`** — every old-plan specific, indexed and explicitly unanswerable.
4. **One skill: `skills/answer-or-refuse.md`** — the three-part response. This is the agent's defining verb; if it works, the agent is safe even when incomplete.
5. **Tools: read-only.** Withheld table filled. No web search in V1 — it introduces untiered content before the tier discipline is proven.
6. **One enforcement rule that actually runs** — `validate.py` over `knowledge/`, blocking on any file lacking `Source:` / `Last verified:`. One real rule is enough to prove the pattern.
7. **`feedback/corrections.md`** — started empty, owner named.
8. **`evals/refusal-suite.md`** — 20 questions. Ship only at 20/20 on the must-refuse subset.

**Explicitly NOT in V1:** curriculum, six modes, role-play, meeting prep, checkpoints, scoring bars, state files, internal capture, web search, tier-B/C facts, the entity table, regulatory posture.

**Definition of done — testable:**
- Refusal suite 20/20 on must-refuse items.
- Every answerable fact resolves to a URL and a checked date.
- `validate.py` exits 0 over `knowledge/`.
- Quality checklist scored and reported, including a weak score.
- A reader can tell, for any sentence in the knowledge base, whether it is verified, quarantined, or missing.

**Why this is strong rather than merely small:** a new hire's most dangerous input is a confident wrong answer about anything internal. V1 makes that structurally hard — the facts it can state are sourced, the facts it cannot are quarantined, the topics it must refuse are absolute, and refusal is the single procedure that has been engineered. Everything the old plan wanted to add sits on top of that without being load-bearing.

---

## K. Open questions requiring validation

Ordered by how much they block the build.

### K1. Blocking — cannot finish V1 without answers

1. **Who deploys and operates this agent** — hire, HR, or manager? Determines tools, state, PII, and correction ownership. **[M]**
2. **Will the six internal templates ever be filled, by whom, and under what classification?** If never, the curriculum, role branches, and role-play are permanently out of scope and should be deleted rather than deferred. **[M]**
3. **Who owns the correction loop?** `core/` requires the process owner, not the builder — and it cannot be the new hire. **[M]**
4. **Is `state/` permitted to hold employee-relationship data** (manager, stakeholders)? Under what retention? **[M]**
5. **Web search: yes or no in V1?** If yes, what tier does retrieved content carry, and what must the agent disclose? **[O]**

### K2. Fact validation — required before any quarantined item is taught

Ordered by consequence if wrong:

6. **Regulatory posture** — SEC/FINRA/OCC, 53 states, SIPC + Lloyd's excess, Customer Protection Rule segregation, Asset Protection Guarantee. Highest blast radius. **[O]**
7. **Four-entity structure and regulator mapping.** **[O]**
8. **Hazel dates, pricing, subscriber counts, and the "first AI platform to…" claim.** **[O]**
9. **Funding, valuation, AUM, market share, ranking claims.** All perishable. **[O]**
10. **Named enterprise clients and dollar figures.** Third-party names — verify or drop. **[O]**
11. **"No training on customer data"** — public statement or verifiable control? Changes how the agent is permitted to phrase it. **[O]**
12. **Founded 2018 / Jason Wenk / Culver City HQ** vs the pack's LA / SF / Dallas. **[O]**
13. **Day 5 / 15 / 30 onboarding milestones** vs the pack's "about 30 days." **[O]**
14. **Product specifics**: 30+ account types, 500+ models, segment names. **[O]**

### K3. Design questions

15. **Does the agent teach industry failure modes at all?** Useful for an engineer, and mislabelable as Altruist-specific. If yes, how is the boundary made unmistakable in the answer itself, not just the file header? **[O]**
16. **What happens when the hire tells the agent something internal?** Currently undefined. Recommended V1 answer: use it in-session, persist nothing, never promote it to knowledge. **[M]**
17. **Is refusal quality measured, and by whom?** The refusal suite needs a human judging expected-refuse correctness. **[M]**
18. **Does `core/` formally adopt `state/` and `evals/`,** or do they stay deployment-local? Affects every future longitudinal agent. **[I]**
19. **How does the agent behave once the internal templates are filled?** Does the same refusal skill route to internal content, or is a second skill needed? Design now — retrofitting refusal logic is how boundaries get eroded. **[M]**

---

## Closing judgment

`altruist_onboarding_agent_knowledge.md` is the trustworthy document. It is thinner because it stopped where the evidence stopped, and `core/`'s method rewards exactly that.

`new-agent.md` is the more useful document to *steal from* and the more dangerous document to *believe*. Its architecture instincts are good — tiering, mode routing, state, evals, and above all the three-part unknown-answer response, which is the single best idea in either file. Its facts are a liability: ~40 specific claims, no URLs, no per-fact dates, and three sections that would make the agent behave in ways the knowledge pack explicitly forbids.

The correct build is the knowledge pack's discipline, `core/`'s five layers, and roughly a third of the old plan — with the old plan's fact base quarantined until each item earns a source.

**Do not let the old plan's detail substitute for its evidence.** That confusion is the specific failure this agent exists to prevent in a new hire; it would be a poor outcome to build it into the agent itself.
