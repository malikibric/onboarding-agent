# Glossary — Industry Vocabulary

> **Provenance note, important.** These are *general financial-industry* definitions, written for a beginner. They are **not** claims about Altruist and are not drawn from Altruist source material. Where a term connects to something Altruist publicly says, the fact id is cited and that citation is the sourced part.
>
> `core/` calls vocabulary the single highest-value section of a knowledge layer. It is also the safest, because industry terms are public knowledge rather than internal fact — which is exactly why this file can be rich while the rest of the knowledge base is thin.

Definitions are deliberately plain. A new hire should be able to use the word in a sentence after reading one line.

---

## The core four

**RIA — Registered Investment Adviser**
A firm (or person) registered to give investment advice and legally required to act in the client's best interest. RIAs are Altruist's customers. `[ALT-013]`

**Custodian**
The institution that actually holds client assets — the securities and cash — and keeps the official record of them. A custodian safeguards and settles; it does not advise. Altruist describes itself as a custodian. `[ALT-001]`

> **The confusion to avoid:** *custodian ≠ advisor.* The advisor decides what the client should own. The custodian holds it and processes the transactions. Mixing these up is the most common new-hire error and produces sentences that misstate what the company does.

**Broker-dealer**
A firm licensed to buy and sell securities, either for customers or for itself. Altruist's public materials describe it as a FINRA-registered broker-dealer. `[ALT-027]` — attribute this, and send any follow-up on what it means to Compliance.

**Fiduciary duty**
The legal obligation to act in the client's best interest, ahead of your own. It's the standard RIAs are held to, and it is the reason so much of this industry is about documentation and defensibility.

---

## Moving money and accounts

**ACAT — Automated Customer Account Transfer**
The standard process for moving an account's holdings from one brokerage or custodian to another. When an advisor brings a client to a new custodian, an ACAT is usually how the assets arrive. Public materials describe transfers/ACATs as part of the platform. `[ALT-004]`

**Partial vs full transfer**
A full transfer moves the whole account. A partial moves only some positions — and partials are where operational trouble tends to live, because the two sides must agree on exactly what moved.

**Cost basis**
What the client originally paid for a holding. It determines the taxable gain when sold, and it has to travel correctly with a transferred account or the tax reporting downstream is wrong.

**Settlement**
The gap between agreeing a trade and actually exchanging cash for securities. Trades are not final at the moment they execute.

**Sweep**
Automatically moving uninvested cash into an interest-bearing destination — typically a bank program — rather than leaving it idle.

**Household**
A group of related accounts (a couple, a family, connected trusts) managed and reported on together. Advisors think in households, not single accounts.

---

## Investing mechanics

**Rebalancing**
Bringing a portfolio back to its intended allocation after market movement has pushed it off target. Public materials describe automated, rules-based rebalancing. `[ALT-016]`

**Model / model portfolio**
A predefined target allocation that an advisor applies across many client accounts at once, instead of hand-building each portfolio. Public materials describe a model marketplace. `[ALT-004]`

**Fractional shares**
Buying part of a share. It lets small accounts hold a full target allocation instead of being distorted by expensive single shares. Public materials describe commission-free fractional trading in stocks and ETFs. `[ALT-015]`

**UMA — Unified Managed Account**
One account holding several strategies or models side by side, managed as a whole. `[ALT-017]`

**Direct / personalized indexing**
Owning an index's underlying holdings directly rather than through a fund, so individual positions can be screened out or tax-managed. Public materials describe personalized indexing including screens and exclusions. `[ALT-017]`

**Tax-loss harvesting**
Selling a position at a loss to offset gains elsewhere, then maintaining exposure. Public materials describe daily scanning for it. `[ALT-018]`

> **Boundary:** the agent explains what these features *are*. It never advises on whether to use one, for whom, or with what tax effect. That is boundary `B-11`.

**Wash sale**
A tax rule that disallows a loss if a substantially identical security is repurchased inside a set window around the sale. It is the reason automated harvesting has to be careful. *(General industry rule, stated as vocabulary. Not tax advice.)*

**TAMP — Turnkey Asset Management Program**
An outsourced provider that runs portfolio management for an advisor. Relevant because model marketplaces cover some of the same need in-platform.

---

## Firm operations

**Fee billing**
Calculating and collecting the advisor's fee, usually a percentage of assets, usually quarterly, across a whole book of clients. Public materials describe billing tools in the platform. `[ALT-004]`

**Performance reporting**
Showing clients what their portfolio actually did over a period. `[ALT-004]`

**Breakaway advisor**
An advisor leaving a large wirehouse or bank to start or join an independent RIA. A meaningful source of new business for custodians.

**Client portal**
The web and mobile experience the end investor logs into. Public materials describe viewing accounts, tracking performance, moving cash, and accessing statements. `[ALT-021]`

---

## Protections

**SIPC — Securities Investor Protection Corporation**
Covers the return of securities and cash if a member brokerage fails. It does **not** protect against investment losses. Altruist's public materials describe SIPC protection. `[ALT-027]`

**FDIC**
Deposit insurance for bank accounts, with per-depositor per-bank limits. Distinct from SIPC — different institutions, different risks.

> **Boundary:** define the terms; never state what any protection covers in a specific case, and never state coverage amounts. Coverage specifics from the old draft failed verification (`ALT-Q05`, `ALT-Q06`). Route to Compliance — boundary `B-15`.

---

## Altruist-specific

**Hazel**
Altruist's AI platform for wealth management. `[ALT-006]` `[ALT-023]` See `06-hazel-public.md`.

**Self-clearing**
Handling the back-office settlement and clearing of trades in-house rather than paying another firm to do it. Public materials describe Altruist as combining self-clearing brokerage and custody. `[ALT-029]` — attribute.
