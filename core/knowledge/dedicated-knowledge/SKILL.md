---
name: dedicated-knowledge
description: Turn raw company material (process notes, SOPs, call transcripts, exports, screenshots, scattered docs) into a rigorous CLAUDE.md that serves as an AI agent's dedicated knowledge layer. Use this whenever the user wants to create, audit, or strengthen a CLAUDE.md, AGENTS.md, agent knowledge base, or system-prompt knowledge file — and equally whenever they hand over company or client information and say things like "build an agent for this", "we're onboarding a client", "capture how this team works", "document this process for an agent", or "make an agent that can do what Sarah does". Trigger even if the user never says the words "CLAUDE.md" or "knowledge layer".
---

# Dedicated Knowledge

Build the knowledge layer an agent runs on: a CLAUDE.md that encodes how a specific company actually operates, so an agent can do real work inside that company without guessing.

This is not documentation for humans. A human reader tolerates vagueness and fills gaps from experience. An agent cannot. Every ambiguity left in the file becomes a wrong output later, and the failure will be silent. Write accordingly.

## The core distinction

Most knowledge files fail the same way: they describe the company instead of encoding how it decides.

| Weak (descriptive) | Strong (operational) |
|---|---|
| "We pride ourselves on fast quoting." | "Quote turnaround target is 4 business hours. Past that, notify the AE before sending." |
| "We serve mid-market distributors." | "Segment A = 50+ locations, gets tiered pricing. Segment B = under 50, list price only." |
| "Use professional language." | [A worked example of an approved quote email, verbatim.] |
| "Check inventory before confirming." | "Inventory truth lives in NetSuite, not the CRM. When they disagree, NetSuite wins." |

The test for every line you write: **could an agent take a different action because this line exists?** If not, cut it. Length is not the goal — decidability is.

## Workflow

### 1. Inventory what you were actually given

Before extracting anything, list the source material and what each piece can and cannot tell you. A call transcript reveals decision rules and vocabulary. A CRM export reveals entity structure. A polished company deck reveals almost nothing operational — it is marketing.

State this inventory back to the user in a few lines. It sets honest expectations about how complete the output can be.

### 2. Extract into the standard schema

Read `references/extraction-schema.md` and work through it category by category against the source material. This is the analysis pass — you are mining raw material for twelve specific kinds of fact, not reading for general comprehension.

Do this before writing any output. Extraction and drafting are different modes; mixing them produces files that follow the shape of the source documents instead of the shape an agent needs.

### 3. Mark confidence on every claim

This convention is what separates a trustworthy knowledge layer from a plausible-sounding one. Apply it during extraction, not after:

- **`[VERIFIED]`** — stated explicitly in the source material. Default; no tag needed in the final file.
- **`[ASSUMED]`** — you inferred it from context. Tag it inline in the final file so a reviewer can confirm or kill it.
- **`[MISSING]`** — the agent needs this and it is not in the material. Tag it, and carry it into the Open Questions section.

Never quietly fill a gap with an industry-standard guess. A wrong rule stated confidently is worse than an acknowledged hole, because the hole gets fixed and the wrong rule gets executed. This applies especially to numbers, thresholds, approval limits, and anything touching money, legal exposure, or customer commitments.

### 4. Write the file from the template

Use `assets/CLAUDE-template.md` as the exact structure. Keep the section order — it runs from stable context to volatile specifics to hard limits, which is roughly the order an agent needs things.

Two rules that matter more than the rest:

**Separate stable facts from volatile ones.** Anything that changes weekly — prices, stock levels, staff assignments, open deals — does not belong in the file as a value. It belongs as a pointer: which system holds it, how to reach it, what to do if it is unreachable. Hardcoded volatile data is the main reason knowledge layers rot within a month.

**Prefer worked examples to adjectives.** One real approved output, pasted verbatim, teaches an agent more than a paragraph of style guidance. Ask for these specifically if the material lacks them.

### 5. Audit before delivering

Run the file against `references/quality-checklist.md`. Report the results honestly — including the score if it is mediocre. A knowledge layer that passes at 60% and says so is more useful than one claimed to be complete.

### 6. Hand back the open questions

Close with a short, prioritized list of what you could not determine, ordered by how much damage the gap could cause. Frame each as a specific question someone at the company can answer in one sentence — not "need more info on pricing" but "who can approve a discount above 15%, and is there a hard ceiling?"

Use `references/discovery-questions.md` when the user needs to go collect this information, or when the source material is thin enough that the honest answer is "interview someone before I write this."

## Scope discipline

A knowledge layer serves one agent covering one domain. "Everything about the company" produces a file too diffuse to be useful and too large to stay accurate.

If the material spans several domains, say so and propose a split: shared company context in one file, domain-specific knowledge in separate files that inherit it. Ask which domain to build first rather than building all of them shallowly.

## What this skill does not cover

Dedicated knowledge is one layer of an agent. Skills (the procedures it follows), tool access, feedback loops, and enforcement are separate concerns. When the user's request drifts into those, note the boundary rather than silently expanding the knowledge file to cover it — knowledge files that absorb procedural logic become unmaintainable.

## Reference files

- `references/extraction-schema.md` — the twelve extraction categories, with what to look for and where it usually hides
- `references/quality-checklist.md` — pre-delivery audit, scored
- `references/discovery-questions.md` — interview questions for filling gaps, grouped by category
- `assets/CLAUDE-template.md` — the output template
