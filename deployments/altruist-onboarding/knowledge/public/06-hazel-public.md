# Hazel — Public

> Capability descriptions only. **No dates, no pricing, no subscriber counts, no architecture, no primacy claims.** Every one of those failed verification and several are explicitly forbidden by the primary pack.

## What Hazel is

Altruist publicly markets Hazel as its AI platform, described as drawing on real-time custodial data plus CRM, email, and notes to support faster answers and more personalized advice. `[ALT-006]`

Public materials say Hazel emerged from the acquisition of Thyme, a meeting-intelligence tool. `[ALT-023]` *(P3 — attribute)*

Public materials say Hazel connects to CRM, email, calendar, and document systems. `[ALT-026]` *(P3)*

## Capabilities

Publicly described: `[ALT-024]` *(P3 — attribute the whole set)*

- **Ask Hazel** — natural-language Q&A over client emails, meetings, CRM notes, and documents.
- **Meeting intelligence** — record, transcribe, and summarize meetings; surface action items; push them to CRM or task systems.
- **Daily digest** — a prioritized view of upcoming meetings, important emails, and follow-ups.
- **Tax planning** — ingests tax returns, paystubs, statements, and custodian data to propose personalized strategies explained in plain language.

## The commercial relationship worth understanding

Public materials say Hazel is available both to firms that custody with Altruist and to firms that do not; when paired with Altruist it can use live account, holdings, and balance data. `[ALT-025]` *(P3)*

That is a genuinely useful thing for a new hire to hold: **Hazel and the custody platform are separable.** It explains why Hazel is discussed as its own product rather than a feature.

What the agent must **not** do is build a strategy narrative on top of it. The old draft infers that Hazel is a customer-acquisition wedge and that custodial data correctness is therefore the company's moat — an architecture-and-strategy inference the primary pack explicitly forbids, and which the draft then instructs the hire to internalize as conviction. Quarantined as `ALT-Q18`. If a hire asks "why does Altruist sell Hazel separately?", the answer is that the agent doesn't know the strategy and the people around them do.

## Security messaging — handle exactly as written

Hazel's public security messaging says client data is not used to train foundation models, that data is encrypted, that enterprise-grade security is central to its design, and that zero-data-retention arrangements with AI providers are used where applicable. `[ALT-028]`

**`ALT-028` is sensitive and its attribution is mandatory and non-negotiable:**

> This is Hazel's *published security messaging*. It is not a verified technical control. It must never be repeated to a client or prospect, never put in writing as an assurance, and never used to answer "is my data safe?".

Boundary `B-15` covers every request to confirm, guarantee, or pass this on. The primary pack's guardrail is the reason: treat public marketing copy as positioning, not proof of internal process. A new hire who repeats a security guarantee they cannot stand behind has created a real problem, and this is the single most likely way this agent could cause one.

## Not answerable

Launch dates and the "first to unify real-time custodial data" primacy claim (`ALT-Q14`), pricing (`ALT-Q15`), subscriber counts (`ALT-Q16`), the Y Combinator detail (`ALT-Q13`), competitor names (`ALT-Q19`), and anything at all about Hazel's model stack, prompts, evaluation methods, permissions, or internal architecture — forbidden outright by the primary pack and covered by boundary `B-12`.
