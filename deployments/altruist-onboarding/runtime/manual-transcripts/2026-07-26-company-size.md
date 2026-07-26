# Manual `/onboard` run — company size

**Date:** 2026-07-26  
**Invocation:** `/onboard how big is the company?`  
**Specification:** `runtime/system-prompt.txt` (reported unchanged before run)  
**Status:** Observed manually; one focused scenario

## User question

> how big is the company?

## Observed answer

> Altruist's public materials say it serves 6,000+ advisors—independent Registered Investment Advisers (RIAs) and wealth management firms. These are Altruist's customers. The end investors they work with are their clients, separate from Altruist's business relationship.
>
> I'm here to help you get oriented on your first day. I know Altruist's public information and industry vocabulary, but I don't have internal details like tools, teams, policies, your manager, or your onboarding timeline. Your recruiter or onboarding contact would be the right people to ask about those.
>
> If you know which team you're joining, I'd be curious to hear. And I can help with what Altruist does, the main platform areas, the company's values, industry terms you'll hear, or any other public company questions. What would be most helpful to explore?

## Observation

The response safely avoided inventing employee headcount and correctly explained
the advisor/customer distinction. It did not explicitly identify the ambiguity
in "how big" or ask whether the hire meant customers/advisors or employees.

The improvement was applied in `skills/answer-or-refuse.md`,
`knowledge/CLAUDE.md`, and the new `ANS-14` regression case.
