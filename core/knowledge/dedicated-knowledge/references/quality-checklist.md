# Quality Checklist

Run before delivering. Score honestly and report the result, including a weak one — a knowledge layer known to be 60% complete is safer to deploy than one assumed to be finished.

## Blocking checks

Fail any of these and the file is not ready, regardless of how good the rest looks.

- [ ] **No invented specifics.** Every number, threshold, name, and rule traces to source material or carries `[ASSUMED]` / `[MISSING]`. Spot-check the three most consequential numbers in the file against the source.
- [ ] **Hard constraints present and absolute.** Section 10 exists, is non-empty, and contains no hedging language.
- [ ] **Escalation triggers are checkable.** No entry in section 11 depends on the agent's subjective confidence.
- [ ] **Sources of truth resolved.** Where two systems could hold the same fact, the file says which wins.
- [ ] **No volatile data hardcoded.** Prices, stock, staffing, and open items appear as pointers to systems, not as values.

## Decidability

- [ ] **Every line changes something.** Read the file line by line asking whether an agent could act differently because of it. Cut what fails.
- [ ] **Soft language converted.** No "usually", "typically", "as appropriate", "use judgment" left standing unless deliberately marked as a judgment call with an escalation path.
- [ ] **Worked examples present** for each artifact type the agent produces — real ones, not composed illustrations.
- [ ] **Vocabulary is thorough.** Scan the rest of the file for any term a competent outsider would not know. Each should appear in section 2.

## Structure

- [ ] **One domain.** The file covers a single agent's scope, not the whole company.
- [ ] **Process steps have triggers and done-criteria**, not just actions.
- [ ] **Open questions are specific and assigned** — answerable in one sentence by a named role.
- [ ] **Header metadata filled in** — date and source material, so a reader knows what this was built from and how stale it is.

## Adversarial pass

The most useful ten minutes. Take the agent's point of view and attack the file:

1. **Pick the three most expensive mistakes** the agent could make in this domain. For each, find the line that prevents it. If there is no such line, that is the highest-priority gap in the file.
2. **Find one instruction you could follow to the letter and still produce something the company would reject.** Fix the ambiguity that allows it.
3. **Ask what a new hire would need on day one** that is not in the file. That is usually the unwritten knowledge nobody thought to state.

## Scoring

Count the checkboxes passed out of 13 — the adversarial pass produces findings, not score points. Report as a fraction with the specific failures named:

> "10 of 13. Missing: approval thresholds above 15% discount, no worked example for the reorder confirmation, and the inventory source-of-truth conflict between NetSuite and the CRM is unresolved. The threshold gap is the one I would fix before this goes live."

Never round up a score into "looks good" language. The point of the number is that it forces the specifics into the open.
