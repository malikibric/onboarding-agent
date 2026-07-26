# Extraction Schema

Twelve categories to mine from source material. Work through them in order. For each, capture what you find, tag confidence, and note what is missing.

Most source material is disorganized — a single call transcript may contain vocabulary, decision rules, and escalation paths scattered across forty minutes. Read for these categories specifically rather than reading front to back.

---

## 1. Identity and business model

What the company sells, to whom, and how it makes money. Enough that an agent understands the stakes of its work — an agent that does not know the company sells to distributors rather than consumers will write the wrong email.

Keep to a short paragraph. This section is context, not content.

**Where it hides:** website, first two minutes of any call, email signatures.

## 2. Vocabulary

Internal terms, abbreviations, product codes, system nicknames, role shorthand. Every term where the company's meaning differs from the general one.

This is the single highest-value section and almost always the most neglected. An agent that does not know "the board" means the weekly ops dashboard rather than the board of directors will produce confidently wrong work. Companies are blind to their own jargon, so extract aggressively: any noun used without explanation in internal material is a candidate.

Format as a flat glossary. Include the wrong-but-plausible reading where it is genuinely confusable.

**Where it hides:** everywhere, but especially in casual internal chat, ticket titles, and spreadsheet column headers.

## 3. People and authority

Named individuals, roles, and — critically — who decides what. Approval thresholds. Who to route which type of question to. Who must be copied on what.

Names and assignments are volatile. Where possible, encode the role and the rule ("discounts above 15% need sales leadership approval") and point to the system that holds current names, rather than hardcoding a person.

**Where it hides:** org charts if you are lucky, otherwise approval flows described verbally in calls.

## 4. Products and services

The catalog, its structure, and the logic underneath it — how things are grouped, coded, bundled, substituted. Not a full product list dump. An agent needs the *pattern* well enough to navigate the catalog in the tool, not a stale copy of the catalog.

**Where it hides:** price lists, order forms, the CRM's field structure.

## 5. Customers and segments

How the company divides its customers and what changes as a result. Segments only matter if they drive different behaviour — different pricing, different terms, different tone, different SLA. If the segmentation changes nothing operationally, skip it.

**Where it hides:** CRM field values, discount policies, sales team territory descriptions.

## 6. The process this agent owns

Step by step, with three things per step that are usually left out:
- **Trigger** — what causes this step to start
- **Done criteria** — how you know the step is complete and correct
- **Handoff** — who or what receives the output

Get the real process, not the official one. If a transcript describes people routinely skipping a documented step, the real process is the one to encode — and the discrepancy is worth flagging to the user.

**Where it hides:** screen recordings, "walk me through your day" transcripts, the gap between an SOP and how anyone actually behaves.

## 7. Decision rules

Every if/then in the operation. Thresholds, conditions, branch points. This is what turns a description into something executable.

Convert soft statements into hard ones wherever the material supports it, and tag `[ASSUMED]` when you had to pick the boundary yourself. "We usually give the bigger accounts a break on shipping" becomes a candidate rule with an explicit unknown: what counts as bigger, and how much of a break.

**Where it hides:** phrases like "it depends", "usually", "unless", "we'd normally". Every one of these is an unwritten rule.

## 8. Sources of truth

For each category of fact, which system holds the authoritative version — and what happens when two systems disagree.

Nearly every company has at least one contradiction here, and nearly every agent failure in production traces back to reading the wrong system. Ask about it directly if the material does not say.

**Where it hides:** rarely documented. Usually only surfaces when you ask "where would you look to check that?"

## 9. Output standards

What good work looks like, expressed as examples rather than adjectives. Collect real approved artifacts — a sent quote, a published summary, a filed report — and include them verbatim in the file.

Where a format is rigid (invoice numbering, file naming, subject line conventions), state the rule exactly. Where it is a matter of judgment, the example does the teaching.

**Where it hides:** sent-mail folders, shared drives, whatever the team quietly treats as the template.

## 10. Hard constraints

Things the agent must never do. Regulatory limits, contractual terms, commitments it cannot make, data it cannot expose, claims it cannot state.

Write these as absolutes with no interpretive room. This section is the one place where blunt prohibition beats nuance — it is the last line of defence when everything else in the file has been ambiguous.

**Where it hides:** compliance policies, legal review comments, and the horror stories people tell about the last time something went wrong.

## 11. Escalation

When the agent should stop and involve a human. Define it by condition rather than by feeling: value thresholds, unrecognised entities, conflicting data, anything irreversible, anything touching an external commitment.

An escalation rule that says "escalate when unsure" is not a rule. Give it a trigger.

**Where it hides:** must usually be constructed from decision rules and hard constraints rather than found directly.

## 12. Gaps

The running register of `[MISSING]` items. Maintain it throughout extraction rather than assembling it at the end — gaps are easiest to notice at the moment you go looking for something and it is not there.

Prioritize by consequence, not by how hard they are to fill. A missing approval threshold on a six-figure decision outranks a missing glossary entry.
