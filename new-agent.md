# Altruist New-Hire Onboarding Agent — Build Plan v1

**Context change from v0:** the user is no longer a candidate. They have been hired. The agent's job is not interview prep — it is to take a new employee from day 0 to *credible, contributing, and unafraid to open their mouth in a meeting* as fast as possible.

**Built the harperOS way:** knowledge → skills → tool access → feedback loop → enforcement. A prompt alone is not an agent.

---

## 1. Objective

Compress the ramp period for a new Altruist employee from the typical 3–6 months to roughly 30 days of confident participation and 60–90 days of independent contribution.

**Success criteria — measurable, not vibes:**

| Milestone | The new hire can… |
|---|---|
| Day 1 | Explain what Altruist does, who pays for it, and why, in 60 seconds |
| Day 5 | Use the vocabulary (RIA, ACAT, custody, TAMP, sweep, rebalance) without hedging |
| Day 14 | Trace an end-to-end workflow (advisor onboards a client → assets transfer → trades → billing) and name where it breaks |
| Day 30 | Sit in a cross-functional meeting, follow the argument, and ask a question that moves it forward |
| Day 60 | Scope their own work with correct risk framing (compliance, data correctness, client impact) |
| Day 90 | Onboard the *next* new hire on their domain |

The anti-goal: an agent that produces polished, confident, generic answers. That actively harms a new hire, because it teaches them to bluff inside a regulated firm.

---

## 2. Who it serves

Primary: a new engineer. But the same knowledge base serves ops, support, and product hires with a different skills layer on top — that reuse is the point, and it's the argument for building it as files rather than one prompt.

The agent's **first action in session one** is to capture and store:

- Role and team (engineering / ops / support / product / GTM)
- Seniority
- Stack and background (what they already know transfers)
- Manager and immediate stakeholders
- Start date — this drives the curriculum clock

Everything after that is calibrated to those five facts. Without them the agent is a generic FAQ bot.

---

## 3. Knowledge boundaries — the hard constraint

The agent is built **from public information only.** It has no access to internal docs, private roadmaps, customer data, internal architecture, incidents, or employee-only process.

This is a feature, not an apology. It is exactly what a harperOS deployment looks like on day one, before internal sources are connected. The design must make that connection trivial later: the moment Confluence / Notion / the internal wiki is plugged in, it drops into `knowledge/internal/` and the agent's answers get sharper without a rewrite.

**When a question needs internal knowledge, the agent must return three things — never a guess:**

1. What is publicly known
2. The assumption required to continue
3. **The exact question to ask internally, and who to ask**

Item 3 is the highest-value output in the whole system. It converts "I don't know" into a productive action and teaches the new hire the single most important professional habit in a regulated firm.

---

## 4. Architecture

```
altruist-onboarding-agent/
├─ AGENT.md                       ← identity, modes, routing, enforcement
├─ knowledge/
│  ├─ 00-facts.md                 ← tiered, dated, sourced company facts
│  ├─ 01-domain-primer.md         ← RIA / custody / brokerage from zero
│  ├─ 02-glossary.md              ← every acronym, plain English
│  ├─ 03-product-surface.md       ← per product: what, who uses it, what breaks
│  ├─ 04-hazel.md                 ← the AI platform, deep
│  ├─ 05-regulatory.md            ← SEC, FINRA, OCC, entity structure, why it matters daily
│  ├─ 06-competitive.md           ← Schwab, Fidelity, Pershing; Jump, Zocks
│  ├─ 07-workflows.md             ← end-to-end traces of the core advisor journeys
│  ├─ 08-failure-modes.md         ← what goes wrong and who gets hurt
│  ├─ 09-open-questions.md        ← the internal-only list, kept live
│  └─ internal/                   ← empty placeholder; where real docs land later
├─ skills/
│  ├─ curriculum.md               ← the day 1 / 30 / 60 / 90 path
│  ├─ explain.md                  ← teach a concept, then test retention
│  ├─ meeting-prep.md             ← talking points, risks, questions, decision criteria
│  ├─ stakeholder-roleplay.md     ← PM, compliance, support lead, staff eng, exec
│  ├─ trace-workflow.md           ← walk a business flow end to end
│  ├─ question-generator.md       ← what to ask your manager this week
│  └─ assess.md                   ← the scoring rubric
├─ state/
│  ├─ profile.md                  ← role, team, stack, start date, manager
│  ├─ progress.md                 ← curriculum position, competencies cleared
│  └─ gap-log.md                  ← dated weak spots, scheduled for retest
└─ evals/
   └─ checkpoints.md              ← day 7 / 30 / 60 assessments with model answers
```

**Tool access:** web search (Altruist ships fast — a frozen knowledge base is stale within weeks), file read/write for state. Later: internal doc sources, calendar, Slack.

---

## 5. Knowledge base — Altruist fact base v0

Every fact carries a **tier** and a **date**. The agent must surface both when a fact is load-bearing. This is the discipline that prevents confident fabrication.

- **Tier A** — Altruist's own site, press releases, regulatory filings
- **Tier B** — reputable trade press, credible secondary reporting
- **Tier C** — aggregators and third-party trackers; approximate, flag on use
- **Tier D** — inference by the agent; must be labelled as such, never stated as fact

### A. Identity and business model (Tier A)

Self-clearing digital custodian and wealth platform for independent RIAs, positioning itself as "AI-forward." Founded 2018 by Jason Wenk. HQ Culver City, CA. Serves 6,000+ advisors.

Vertically integrated: custody + front, middle, and back office in one platform, at a fraction of legacy cost. The bet is that owning the rails is what makes the software (and now the AI) good.

**Entity structure — a new hire must know this on day one:**

| Entity | Role |
|---|---|
| Altruist Corp | Technology |
| Altruist LLC | SEC-registered investment adviser |
| Altruist Financial LLC | Broker-dealer, FINRA/SIPC, clearing & custody |
| Altruist Advisors LLC | Advisory |

This split isn't legal trivia. It determines which regulator cares about which system, which disclosures attach to which screen, and who has to approve a change.

**Product surface (Tier A):** account opening (30+ account types), digital ACATs and bulk onboarding, commission-free fractional trading with smart order routing, portfolio reporting, fee billing, 25+ integrations (CRM, planning, reporting), custody, margin / SBLOC / fully-paid lending, high-yield cash via partner banks, tax management, 500+ model marketplace, personalized indexing, alternatives, options, co-branded client portal.

**Advisor segments:** Breakaway / Established / Enterprise. Three very different onboarding realities, service expectations, and failure costs. Any feature discussion should start with "which segment?"

**Regulatory posture (Tier A):** SEC, FINRA, OCC, 53 states and territories. SIPC plus excess coverage through Lloyd's. Client assets segregated under the Customer Protection Rule. Asset Protection Guarantee for unauthorized activity.

**Published onboarding arc:** join → onboard clients (day 5) → configure firm (day 15) → go live (day 30).

### B. Scale and trajectory (Tier B)

- Series F, April 2025: $152M led by GIC; Salesforce Ventures, Geodesic, Baillie Gifford, ICONIQ Growth participating. Valuation ~$1.9B. Total raised ~$602M.
- AUM tripled two consecutive years. 2025 T3 survey: market share jumped from 2.85% to 6.25%; All-Star in custody, portfolio management, trading/rebalancing, billing, cash management.
- Altruist Clearing (self-clearing) launched ~2024 — the step that made it a full-service custodian. SSG acquisition added 1,600+ advisors.
- As of Nov 2025: claims third-largest custodian by number of RIAs served, and the platform advisors most often switch to or add from Schwab.
- Enterprise wins: Ritholtz Wealth (~$6B), Bryn Mawr Trust Advisors (WSFS), Sowell Management, Gerber Kawasaki.

### C. Hazel — the strategic center of gravity (Tier B)

Any onboarding that treats Hazel as a side feature is wrong.

- Launched Sept 9, 2025, built on the acquisition of **Thyme**, a Y Combinator-backed meeting-intelligence startup.
- Core feature "Ask Hazel": answers from the firm's recorded conversations, emails, documents, CRM, plus market and regulatory information. Also meeting prep, real-time notes, recording/transcription/summary, drafted client emails in the advisor's voice, CRM task sync (Salesforce, Wealthbox, Redtail).
- **Nov 18, 2025:** first AI platform for wealth managers to unify *real-time custodial data* — accounts, households, holdings, balances, beneficiaries — with CRM, email, and notes. Firm-wide reporting on clients behind on RMDs, unrealized losses to harvest, etc.
- **Feb 10, 2026:** AI tax planning. Reads 1040s, paystubs, statements, notes, CRM and custodial data; applies tax logic; produces personalized strategies and scenario modeling in minutes.
- Sold standalone at hazel.ai, $60/seat/month or $600/year, and works for advisors who custody elsewhere.
- Stated commitment: encryption, enterprise-grade security, **no training on customer data.**
- March 2026 trade coverage: ~1,600 RIA firms subscribed in the four weeks after the tax agent release; analysts frame the edge as architectural rather than algorithmic — clean, permissioned custodial data underneath. Competitors named: Jump, Zocks.

### D. Strategic read (Tier D — inference, label it)

Hazel is both a product and a customer-acquisition wedge: sell the AI to advisors who custody at Schwab or Fidelity, prove the data-integration gap, convert them to custody. Which means **custodial data correctness is no longer just a compliance concern — it is the moat.** Bad data doesn't break a report; it poisons the flagship AI product and the sales motion behind it. That's the sentence a new engineer should internalize in week one.

### E. Known unknowns → `09-open-questions.md`

Internal architecture, service boundaries, deploy and on-call practice, real SLAs, incident history, roadmap, team topology, actual approval chains for compliance-touching changes, Hazel's model/eval stack. The agent never guesses at these — it generates the question to ask.

---

## 6. The three layers the agent must teach

Product pages don't make anyone credible. These do.

**Layer 1 — Who pays and why.** RIA vs broker-dealer. Fiduciary duty. Why an advisor leaves Schwab. What "breakaway" means. What a TAMP is and why a 500+ model marketplace undercuts it. How custodians actually make money: cash spread, securities lending, margin, platform fees.

**Layer 2 — What breaks, and who gets hurt.** This is where a new hire stops sounding like a visitor.

- ACAT transfers: partial transfers, rejects, cost-basis carryover arriving late or wrong
- Corporate actions: splits, mergers, spinoffs landing mid-rebalance
- Settlement and trade breaks under T+1
- Cash sweep reconciliation across multiple program banks; FDIC limits per depositor per bank
- Fee billing: a small calculation error replicated across an entire book, then invoiced
- RMD deadlines — a missed one is a client penalty
- Wash sales in automated tax-loss harvesting
- Reporting performance calculations that disagree with a client's statement

Each is an engineering failure with a named victim: an advisor's credibility, or an end client's money.

**Layer 3 — AI-specific risk.** Hazel reads tax documents and real balances and drafts client communications. So:

- What happens when it states a wrong balance to an advisor mid-meeting?
- Fiduciary liability for an AI-influenced recommendation
- Evaluation sets for a tax agent — how do you even know it's right?
- Retention, consent, and permissioning on meeting recordings
- Prompt injection via an uploaded client document
- Where the human approval gate sits, and why

Very few new hires arrive thinking about this. It is the fastest route to being taken seriously.

---

## 7. Curriculum

The agent drives this on a clock keyed to the start date, adapted by role.

**Day 1 — Orientation**
Capture profile. Deliver the 60-second company explanation and have the hire repeat it back in their own words. Glossary triage: the 15 terms they'll hear today.

**Week 1 — Domain fluency**
Who Altruist serves and why they switch. The entity structure and what each regulator cares about. Money flow end to end. Output: the hire can explain the business to a friend without notes.

**Week 2 — Product surface**
Each product: who uses it, what it replaces, what breaks. Trace two full workflows: (a) advisor onboards a household and transfers assets in, (b) quarter-end billing and reporting. Output: the hire can name three failure modes per workflow.

**Week 3 — Role-specific depth**
Branches by team. Engineering: idempotency, reconciliation, audit trails, backward compatibility, observability in a financial system. Ops/support: escalation, advisor-impact triage. Product: segment trade-offs. Plus Hazel and AI risk for everyone. Output: the hire can scope a small change with correct risk framing.

**Week 4 — Contribution and integration**
Meeting-prep drills for real meetings on their calendar. Stakeholder role-play: compliance partner, support lead, staff engineer. Question generation for their manager and skip-level. Day-30 checkpoint assessment.

**Days 30–90 — Compounding**
Weekly gap retests. On-demand explain/trace/meeting-prep. Day-60 checkpoint. Day-90: the hire writes the onboarding notes for their domain, which feed back into `knowledge/internal/`. The system gets smarter with each hire.

---

## 8. Modes

| Mode | Use |
|---|---|
| **Teach** | Explain a concept, then test retention with two questions |
| **Trace** | Walk a workflow end to end; hire must name the break points |
| **Meeting prep** | Talking points, risks, questions, decision criteria for a specific meeting |
| **Stakeholder role-play** | Agent plays PM, compliance, support lead, staff eng, or exec and pushes back |
| **Ask better questions** | Generate the questions the hire should be asking internally this week |
| **Checkpoint** | Scored assessment at day 7 / 30 / 60 |

The agent must **name the mode it is entering** and stay in it until told otherwise. Left unrouted, models drift into whatever mode the previous message resembled.

---

## 9. Feedback loop

Every session writes to state. This is the part that makes it an agent rather than a chatbot.

- A wrong or vague answer creates a dated entry in `gap-log.md` with topic and severity
- Gaps are retested unprompted 3 and 10 days later
- `progress.md` tracks curriculum position and competencies cleared
- Anything the hire learns internally that fills an open question gets written to `knowledge/internal/` — the knowledge compounds instead of evaporating when they close the tab

---

## 10. Enforcement

Rules that the agent cannot proceed while violating:

1. **No invented internal knowledge.** Ever. Missing information triggers the three-part response (public / assumption / question to ask).
2. **Tier and date load-bearing facts.** If a number drives a decision, its source tier and age must be visible.
3. **No praise for a weak answer.** Assessment format is fixed: what was strong → what was vague → what assumption was unsafe → which stakeholder or risk was missed → a stronger rewrite → one harder follow-up.
4. **Every technical discussion names the client impact.** Who is harmed if this is wrong — the advisor, or the end client?
5. **Flag compliance-touching decisions.** If a change touches disclosures, client money, PII, or trading, the agent says so and names who would need to approve.
6. **No buzzword answers.** Explain why a decision matters or don't make it.

---

## 11. Assessment rubric

Score 1–5 on five axes:

- Technical depth
- Domain awareness (RIA/custody context, not just software)
- Risk awareness (correctness, compliance, client harm)
- Honesty about unknowns
- Communication clarity

**Checkpoint bars:** Day 7 ≥ 3.0 average. Day 30 ≥ 4.0 average, no axis below 3. Day 60 ≥ 4.0 with no axis below 4.

The single highest-value behavior to train, and the one weighted most heavily:

> "I don't know — that's internal. Here's what's public, here's the assumption I'd need, and here's who I'd ask to confirm."

---

## 12. Research queue

Priority order, highest signal first:

1. Altruist **engineering blog** — architecture signals, stack, how they talk about correctness
2. **Careers page**, specifically the hire's own job description — names the real stack and team
3. **Help center / advisor guides** — the true operational surface, workflow by workflow
4. **Form CRS, fee schedule, security disclosures** — regulatory posture in their own words
5. **hazel.ai** product pages + the three Hazel announcements
6. **The Advisor Journey** podcast episode on Hazel (Gokul Ramanathan, Fernando San Martín) — closest public source to internal reasoning
7. Trade press — RIABiz, WealthManagement, InvestmentNews — for competitive framing

---

## 13. Build sequence

| # | Output | Est. |
|---|---|---|
| 1 | Pull sources 1–7; write `00-facts.md`, `02-glossary.md` | 3h |
| 2 | Write `01-domain-primer.md`, `07-workflows.md`, `08-failure-modes.md` | 4h |
| 3 | Write `04-hazel.md`, `05-regulatory.md`, `06-competitive.md` | 2h |
| 4 | Write `AGENT.md` — modes, routing, enforcement, state handling | 1.5h |
| 5 | Write `skills/` files and `assess.md` rubric | 2h |
| 6 | Write `evals/checkpoints.md` — day 7/30/60 with model answers | 1.5h |
| 7 | Dry run the full week-1 curriculum; log every gap and patch | 2h |

Roughly two focused days to a working v1.

---

## 14. Open decisions

1. **Which role and team** is the new hire joining? Engineering (which surface — clearing, data platform, Hazel/AI, integrations?), ops, support, product? This changes weeks 3–4 entirely.
2. **Runtime:** Claude Project, Claude Code with real files, or standalone? Files unlock the feedback loop and are the more defensible artifact; a Project is faster to stand up.
3. **Is this one hire or a repeatable onboarding system?** If repeatable, the knowledge layer is shared and only `skills/` and `state/` fork per role — which is the version worth building.
4. **Will internal docs ever be connected?** If yes, `knowledge/internal/` gets designed now, not retrofitted.

---

## 15. Sources

**Tier A:** altruist.com (product, security, disclosures, news), hazel.ai
**Tier B:** Business Wire releases (Hazel launch Sept 2025; custodial integration Nov 2025; AI tax planning Feb 2026; Series F Apr 2025), RIABiz (Mar 2026), WealthManagement.com, InvestmentNews, Private Banker International, fintech.global, The Advisor Journey podcast
**Tier C:** Tracxn company profile (headcount ~857 as of Feb 2026, older valuation datapoints)

Facts current as of July 2026. Altruist ships fast — refresh the fact base monthly.