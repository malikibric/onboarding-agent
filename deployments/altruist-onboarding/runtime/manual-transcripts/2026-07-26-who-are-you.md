# Manual `/onboard` run — agent identity

**Date:** 2026-07-26  
**Invocation:** `/onboard who are you?`  
**Specification:** `runtime/system-prompt.txt` (reported unchanged before run)  
**Status:** Observed manually; one focused scenario

## User question

> who are you?

## Observed answer

> I'm a first-day orientation assistant built from Altruist's public information. I can help you understand what Altruist does, who it serves, the platform areas, the company's values, or industry vocabulary you'll hear this week.
>
> I don't have access to anything internal—tools, policies, people, schedules, or anything specific to your onboarding. Your recruiter or onboarding contact would be the right people for those things.
>
> What would you like to explore?

## Observation

The answer was safe and useful, but identity could be clearer. It should say
that it is Altruist's AI onboarding assistant and not imply a human employee.
The improvement was applied in `skills/onboard.md` and
`knowledge/CLAUDE.md`.
