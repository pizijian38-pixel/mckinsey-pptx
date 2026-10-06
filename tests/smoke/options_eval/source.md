# CRM platform options for Harbor Bank (proposal outline)

Challenge: replace the 15-year-old CRM before the vendor ends support in 18 months, without disrupting 1,200 relationship managers.

## Option 1 — Buy a SaaS CRM (Vendor A)
- Why: vendor product covers 85% of requirements out of the box; upgrades included.
- How: 3 waves by region; vendor-certified integrator; retire the old CRM in month 15.
- Economics: licence $2.1M per year; implementation $4.5M; 5-year cost $15.0M.
- Advantages: fastest time to value (9 months to first wave); lowest delivery risk.
- Disadvantages: limited customisation of credit workflows; data residency needs a dedicated region.

## Option 2 — Extend the in-house platform
- Why: in-house team knows the bank's processes; reuses the existing data model.
- How: rebuild front end; modernise integration layer; 40 engineers for 18 months.
- Economics: build $9.0M; run cost $1.2M per year; 5-year cost $15.0M.
- Advantages: full control of credit workflows; no licence dependency.
- Disadvantages: 18 months before any release; key-person risk in a team of 40.

## Option 3 — Hybrid: SaaS core plus in-house credit module
- Why: buy the commodity sales functions, build only what differentiates the bank.
- How: SaaS for contact and pipeline management; in-house credit module on the SaaS platform API.
- Economics: licence $1.6M per year; implementation $5.5M; 5-year cost $13.5M.
- Advantages: lowest 5-year cost; keeps credit workflows in-house.
- Disadvantages: two teams to coordinate; API limits of the SaaS platform.

## Scorecard (1 = poor, 5 = excellent)
| Criterion | Weight | Option 1 | Option 2 | Option 3 |
|---|---|---|---|---|
| Time to value | 30% | 5 | 2 | 4 |
| 5-year cost | 25% | 3 | 3 | 4 |
| Fit with credit workflows | 20% | 2 | 5 | 4 |
| Delivery risk | 15% | 4 | 2 | 3 |
| Vendor dependency | 10% | 2 | 5 | 3 |

## Recommendation
Option 3 (Hybrid). Roadmap: months 0–6 SaaS core for one region; months 7–12 credit module and two more regions; months 13–18 retire the old CRM.
Risks: SaaS API limits (high) — mitigate with a proof of concept before contract signature; team coordination (medium) — one programme office and shared backlog; data residency (medium) — contract a dedicated region.
