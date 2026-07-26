# Altruist onboarding agent knowledge pack

## Purpose
This file is a project-ready knowledge seed for building a Claude-based onboarding agent for a brand-new hire interacting with an Altruist-focused assistant. The goal is to organize what can be known from public information, identify what cannot be known externally, and structure the missing pieces so internal teams can fill them in safely.

## Task interpretation
The requested agent should:
- act as a first-days onboarding assistant for a new hire,
- rely on public company information where possible,
- clearly separate verified external facts from unknown internal details,
- support a `/onboard` flow for day-one guidance,
- operate with safe guardrails and avoid pretending to know internal tools, people, or policies.

## Verified public facts

### Company overview
- Altruist describes itself as a wealth platform and AI-forward custodian built for independent advisors / RIAs.
- Its public platform messaging centers on account opening, trading, portfolio management, billing, reporting, and custody in one place.
- The company says its mission is to make independent financial advice better, more affordable, and more accessible to everyone.

### Customer and product context
- Altruist publicly says it serves 6,000+ advisors.
- Public product pages describe features including account creation, transfers/ACATs, billing, reporting, integrations, client portal access, custody, model marketplace, high-yield cash, and trading.
- Altruist says firms can use 25+ integrations across CRM, financial planning, and custodial AI workflows.
- Altruist publicly markets Hazel as its AI platform, describing it as drawing on real-time custodial data plus CRM, email, and notes to support faster answers and more personalized advice.

### Onboarding and operating model
- Altruist publicly states that many firms are up and running in about 30 days.
- Public onboarding messaging says clients receive a dedicated onboarding manager.
- A public timeline describes: joining Altruist and setting firm preferences, onboarding clients, configuring portfolios/fees/integrations, and going live.
- Public pages emphasize digital onboarding, transfers/ACATs, and support during setup.

### Company values and culture
- Altruist careers messaging highlights three core values: Kindness, Brilliance, and Grit.
- Careers messaging also emphasizes purpose, growth, equity/compensation, health benefits from day one, work-life integration, and inclusivity.
- Publicly listed office locations include Los Angeles, San Francisco, and Dallas.

## What the agent likely needs to know
The onboarding agent should be prepared to help a new hire with these publicly supported topics:

1. What Altruist is.
2. Who Altruist serves.
3. What the platform does at a high level.
4. The company mission and core values.
5. High-level explanation of public product areas.
6. Publicly described customer onboarding journey.
7. Public language around Hazel and AI capabilities.
8. Public office and culture information from the careers site.
9. What information is not knowable externally and must be escalated.

## Recommended knowledge structure 

### 1) `01_company_overview.md`
Use for mission, positioning, who Altruist serves, and top-level platform summary.

Suggested contents:
- Mission
- Customer segment: independent advisors / RIAs
- Platform summary
- Core differentiators claimed publicly
- Short glossary: custodian, RIA, ACAT, model marketplace, rebalancing

### 2) `02_products_and_platform.md`
Use for product-area explanations a new hire may ask about.

Suggested sections:
- Account opening
- Transfers / ACATs
- Trading
- Portfolio management
- Billing
- Reporting
- Custody
- Client portal
- Integrations
- Hazel AI
- High-yield cash
- Model marketplace

### 3) `03_customer_onboarding_public.md`
Use for public onboarding journey only.

Suggested sections:
- Publicly described 30-day journey
- Dedicated onboarding manager
- House account and firm preferences
- Client onboarding
- Portfolio and fee configuration
- Integration setup
- Go-live milestone

### 4) `04_culture_and_values.md`
Use for mission, values, careers messaging, and work culture clues.

Suggested sections:
- Mission
- Kindness / Brilliance / Grit
- Growth mindset
- Inclusivity
- Benefits publicly mentioned
- Office locations

### 5) `05_ai_and_hazel_public.md`
Use for public AI capability descriptions only.

Suggested sections:
- What Hazel is claimed to do
- Publicly stated data sources Hazel can use
- Example benefits from public marketing language
- Boundaries: do not infer internal model stack, evaluation methods, prompt architecture, or permissions

### 6) `06_glossary.md`
Use for quick explanations of financial-platform terms likely unfamiliar to a new hire.

Suggested terms:
- RIA
- Custodian
- Self-clearing brokerage
- ACAT
- Rebalancing
- Fractional shares
- Fee billing
- SIPC
- FDIC
- Model marketplace

## Clearly missing internal files
These should exist as empty or template files because an external researcher cannot fill them reliably.

### 7) `10_internal_org_chart_TEMPLATE.md`
Purpose: key teams, leadership, reporting lines, important stakeholders.

Template:
- Executive team
- Department leads
- Team names
- Reporting structure
- New hire's manager
- Cross-functional partners
- Slack / email groups

Status: unknown externally.

### 8) `11_internal_tools_TEMPLATE.md`
Purpose: systems the new hire must access.

Template:
- HRIS
- Identity / SSO
- Device setup
- Email / calendar
- Chat / messaging
- Ticketing
- Documentation wiki
- CRM
- Engineering tools
- Support tools
- Analytics tools
- Internal AI tools
- Access request process

Status: unknown externally.

### 9) `12_day_one_process_TEMPLATE.md`
Purpose: exact first-day checklist.

Template:
- Laptop/device pickup or shipping
- Account activation steps
- Security training
- Benefits enrollment steps
- Intro meetings
- Required forms
- Role-specific setup
- End-of-day check

Status: unknown externally.

### 10) `13_people_and_contacts_TEMPLATE.md`
Purpose: who the agent should refer the new hire to.

Template:
- Hiring manager
- Buddy / mentor
- HR contact
- IT support
- Payroll / benefits contact
- Security contact
- Facilities / office contact

Status: unknown externally.

### 11) `14_policies_and_compliance_TEMPLATE.md`
Purpose: internal policy lookup.

Template:
- Code of conduct
- Information security policy
- Acceptable use policy
- Confidentiality policy
- Customer data handling
- Compliance escalation rules
- Remote work / office policy
- Time off policy

Status: unknown externally.

### 12) `15_role_specific_ramps_TEMPLATE.md`
Purpose: onboarding paths by function.

Template:
- Engineering ramp
- Operations ramp
- Support ramp
- Sales ramp
- Product ramp
- Compliance ramp
- Role-specific 30/60/90 day plan

Status: unknown externally.

## Agent behavior guidance

### Role
The agent is a first-days onboarding assistant for new hires. It should help them understand the company, its mission, major products, public language, and day-one orientation basics, while being explicit about what it does not know.

### What it can answer well
- High-level company overview
- Mission and values
- Public product positioning
- Public onboarding/customer workflow descriptions
- Public AI/Hazel descriptions
- Basic glossary questions about industry terms

### What it must not pretend to know
- Internal tools or URLs
- Names of managers or teammates
- Security procedures
- Internal policies or employee handbook details
- Exact first-week meeting schedule
- Private architecture, prompts, permissions, or customer data flows
- Compensation, benefits details beyond public careers copy

### Escalation rules
The agent should say it does not have verified internal information and route the user to the appropriate internal source when asked about:
- access setup,
- payroll or benefits specifics,
- security/compliance instructions,
- team structure,
- role-specific expectations,
- manager-specific priorities,
- legal/policy questions.

## Recommended `/onboard` day-one flow

### Goal
Walk a new hire through a calm, useful day-one conversation.

### Suggested steps
1. Welcome the new hire and explain what the assistant can help with.
2. Ask their team or role if that context is available.
3. Give a concise overview of Altruist: mission, who it serves, and what the platform does.
4. Explain the public core values.
5. Offer a short glossary of key platform terms.
6. Ask what they need next: company overview, product overview, values, glossary, or internal-setup questions.
7. If they ask an internal question, acknowledge the gap and point them to the correct internal template/source.

### Example opening
"Welcome to Altruist. I can help you understand what the company does, who it serves, the main platform areas, and the public culture and values. For internal tools, people, policies, or team-specific processes, I’ll clearly tell you what still needs to be filled in by your team."

## Guardrails for the Claude agent
- Always separate public facts from unknown internal information.
- Never fabricate internal processes, tools, employee names, org structures, or policies.
- Prefer short, structured answers for new hires.
- Use beginner-friendly explanations for finance/custody terms.
- When uncertain, say what source category would be needed.
- Do not provide compliance, legal, or operational instructions unless explicitly present in verified internal files.
- Treat public marketing copy as positioning, not proof of internal process details.

## Public-source notes
This knowledge pack is based on public Altruist website and careers information, including public descriptions of the company mission, platform capabilities, Hazel AI, onboarding claims, customer support claims, and careers values.

## Short note on missing confidence areas
The biggest external blind spots are internal employee onboarding workflows, internal software stack, reporting relationships, support ownership, compliance procedures, and role-specific first-week expectations. Those gaps should be intentionally represented as templates rather than guessed content.
