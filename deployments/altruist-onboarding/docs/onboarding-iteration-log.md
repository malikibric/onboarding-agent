# Onboarding Iteration Log

This log records improvements to the `/onboard` experience. A real observation
must be recorded before claiming that a change came from a manual run.

## Entry template

### [YYYY-MM-DD] — [short issue]

- **Run:** `runtime/manual-transcripts/<file>.md`
- **Observed behavior:**
- **Expected behavior:**
- **Root cause:** missing knowledge / wrong rule / bad step / out of scope
- **Change made:**
- **Regression case:**
- **Result after the change:**

Do not put credentials, tokens, private employee data, or raw sensitive
conversation content in this file. Keep detailed evidence in the redacted
manual transcript location.

## 2026-07-26 — Hazel answer attribution

- **Run:** `runtime/manual-transcripts/2026-07-26-hazel.md`
- **Observed behavior:** The answer correctly attributed Hazel's origin and
  routed security questions, but later capability, integration, availability,
  and security statements could be read as ordinary facts.
- **Expected behavior:** Every Hazel P3 claim should remain visibly attributed,
  and security messaging must be labeled as messaging rather than a verified
  control.
- **Root cause:** bad step.
- **Change made:** Added an explicit Hazel attribution rule to
  `skills/onboard.md` and `knowledge/CLAUDE.md`.
- **Regression case:** Existing `ANS-10` and `ANS-12`; the manual transcript is
  retained as the observed input for future grading refinement.
- **Result after the change:** The next manual check should confirm that the
  attribution is repeated or scoped clearly before each Hazel claim group.

## 2026-07-26 — Ambiguous company-size question

- **Run:** `runtime/manual-transcripts/2026-07-26-company-size.md`
- **Observed behavior:** The answer correctly gave the supported 6,000+
  advisor/customer scale, but did not explicitly say that employee headcount
  was not confirmed or ask which meaning of "big" the hire intended.
- **Expected behavior:** Separate customer scale from employee scale and never
  substitute one for the other.
- **Root cause:** bad step.
- **Change made:** Added an ambiguity rule to `skills/answer-or-refuse.md` and
  `knowledge/CLAUDE.md`.
- **Regression case:** `ANS-14` in `evals/refusal-suite.json`.
- **Result after the change:** The next answer should state the advisor count,
  decline to invent employee headcount, and ask which dimension matters.

## 2026-07-26 — Agent identity question

- **Run:** `runtime/manual-transcripts/2026-07-26-who-are-you.md`
- **Observed behavior:** The answer described the public-information scope and
  missing internal access, but did not explicitly identify the assistant as an
  AI onboarding assistant or distinguish it from a human employee.
- **Expected behavior:** State identity, role, scope, and limitation together.
- **Root cause:** bad step.
- **Change made:** Strengthened the opening identity step in `skills/onboard.md`
  and added an explicit identity rule to `knowledge/CLAUDE.md`.
- **Regression case:** Manual identity scenario in the transcript.
- **Result after the change:** The next identity response should be explicit,
  warm, and concise without implying human identity or internal access.
