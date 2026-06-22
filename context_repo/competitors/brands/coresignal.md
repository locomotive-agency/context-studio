---
brand: Coresignal
slug: coresignal
primary_url: https://coresignal.com/
category: b2b-data
positioning_archetype: api-first
competes_with_zi_pillars:
- data
- universal_access
competes_with_zi_products:
- Data
- APIs & MCP
icp_relevance:
- developer_data_eng
- revops_gtm_eng
pricing_model: tiered_public
has_free_tier: true
has_mcp_server: false
has_conversation_intelligence: false
has_abm_advertising: false
has_predictive_scoring: false
analyst_recognition:
- Datarade top data provider 2023+2024
- EWDCI founding member
research_depth: partial
date_researched: 2026-05-07
flags:
- vs_brand_missing
- manual_review:hq_not_stated
- manual_review:funding_ownership_not_surfaced
- manual_review:integrations_thin
sources_count: 10
sub_products:
- coresignal--multisource-api
- coresignal--employee-firmographic-jobs
type: competitive-landscape
id: ctx.competitors.brands.coresignal
title: Coresignal
description: ''
scope_id: zoominfo
durability: persistent
criticality: hybrid
status: approved
provenance: competitor-wiki/wiki/competitors/coresignal.md
source_type: competitor
source_path: competitor-wiki/wiki/competitors/coresignal.md
tags:
- competitive-landscape
- competitors
resource: https://coresignal.com/
---

# Coresignal

## Sub-products

- [[coresignal--multisource-api|Coresignal Multi-Source API + Agentic Search]] — competes with APIs & MCP
- [[coresignal--employee-firmographic-jobs|Coresignal Employee + Company + Jobs Datasets]] — competes with Data (Pillar 1)

## Summary

Coresignal is an API-first B2B public-web-data provider selling company, employee, and jobs records to engineering, data, and product teams — explicitly positioned as the "data intelligence layer for AI agents" rather than a sales-intelligence UI. Its primary ICP overlap with ZoomInfo is the developer / agent-builder audience served by ZoomInfo's APIs & MCP layer, plus the underlying Data foundation pillar (75M+ company and 865M+ employee records). Coresignal does not ship a seller UI, marketer surface, ABM orchestration layer, dialer, or conversation intelligence — its product is raw data + Elasticsearch query DSL + webhooks, leaving the workflow to the customer. No Coresignal-vs-ZoomInfo page exists on coresignal.com.

## Company Snapshot

| Field | Value |
|---|---|
| Category | B2B public web data provider — APIs and flat-file datasets for company, employee, and jobs data; positions itself as a "data intelligence layer for AI agents" |
| Founded / HQ | Founded 2016. HQ not surfaced on reviewed pages — see flags. |
| Funding / Ownership | _Not available — see flags._ |
| Employee size | 70+ technology specialists (about-us copy); 80+ employees (about-us stats card) |
| Primary buyer | Engineering, data, and product teams at sales tech, HR tech, investment, and market-research companies; data-science / ML teams building AI agents and LLMs |

## Product Offerings

### Company Data API (Base / Clean / Multi-Source)

- **What it does:** REST API to filter, retrieve, and enrich firmographic profiles for ~75M+ companies, with three processing tiers from raw single-source records to AI-enriched multi-source profiles.
- **Key features:**
  - Three processing levels — Base (70+ fields), Clean (80+ fields), Multi-Source (500+ fields)
  - Average 176 ms API response time
  - Elasticsearch Query DSL for filter-based search
  - Bulk download up to 10,000 records per request
  - Response field selection to keep payloads light
  - Real-time updates and historical headcount data
  - JSON, JSONL, CSV (and Parquet on multi-source) output formats
- **Source URL:** https://coresignal.com/solutions/company-data-api/

### Employee Data API (Base / Clean / Multi-Source)

- **What it does:** REST API to filter, retrieve, and enrich professional/employee profiles, scaled across an 865M+ employee dataset with three processing tiers.
- **Key features:**
  - Three processing levels — Base (300+ fields), Clean (90+ fields), Multi-Source (300+ fields)
  - Search filters covering job title, location, seniority, decision-maker flag, skills, education
  - Webhooks notify on profile changes / newly created records
  - Elasticsearch Query DSL search
  - Bulk download and response field selection
  - Real-time updates with last-update timestamps on records
- **Source URL:** https://coresignal.com/solutions/employee-data-api

### Jobs Data API (Base / Multi-Source)

- **What it does:** REST API to search and retrieve deduplicated active and historical job postings (461M+) for HR tech, sales tech, and market research workflows.
- **Key features:**
  - Two processing levels — Base and Multi-Source (85+ fields)
  - 176 ms average response time
  - Bulk source up to 10,000 postings per request
  - Response field selection
  - Real-time refresh of the underlying dataset
  - Use-case framing for HR tech (job search), market research (skills demand), trend forecasting
- **Source URL:** https://coresignal.com/solutions/jobs-data-api

### Agentic Search API (New)

- **What it does:** Natural-language interface that returns structured B2B data (company, employee, jobs) in response to a prompt — pitched as a way to plug Coresignal data into AI agents and end-user dashboards.
- **Key features:**
  - Natural-language prompt → structured B2B data response
  - Pitched for AI agent / LLM-app builders
  - Surfaced as a new flagship offering on every reviewed page (top banner)
- **Source URL:** https://coresignal.com/

### Datasets (flat-file delivery)

- **What it does:** Bulk dataset delivery as JSON or CSV (refreshed monthly with daily/quarterly options on specific datasets) covering Companies (75M+), Employees (865M+), Jobs (461M+), plus combined full-dataset bundles.
- **Key features:**
  - Companies dataset: 75M+ records, monthly full refresh
  - Employees dataset: 865M+ continuously updated records
  - Jobs dataset: 461M+ postings with daily additions
  - Full datasets: 15+ web sources, premium support
  - Pricing starts at $1,000 (yearly contract, monthly payments)
  - Delivery via web link, push to customer cloud, or API retrieval
- **Source URL:** https://coresignal.com/pricing/

### Self-service dashboard / no-code search

- **What it does:** Web app that lets non-engineers describe the data they need in a prompt, generates a list of matching records, enriches it, and exports up to 10,000 records as JSONL.
- **Key features:**
  - Prompt-based list generation
  - Add data fields via UI to enrich the list
  - Export up to 10,000 enriched records (or 100-record preview)
  - Same underlying B2B database as the API
  - Self-service sign-up, no credit card required
- **Source URL:** https://coresignal.com/

### Historical Headcount API (Premium add-on)

- **What it does:** API to track headcount changes over time per company; gated to the Premium plan and discussed alongside Company / Employee APIs.
- **Key features:**
  - Premium-tier access only (Starter and Pro do not include it)
  - Returns monthly / quarterly headcount deltas
  - Used together with Company API for growth tracking and competitive monitoring
- **Source URL:** https://coresignal.com/pricing/

## Pricing

| Tier | Price | What's included | Source |
|---|---|---|---|
| Free (7-day trial) | $0 | 200 Collect credits, 400 Search credits; Employee, Company, Jobs endpoints; Elasticsearch Query DSL; credits valid 7 days; no credit card required. | https://coresignal.com/pricing/ |
| Starter | From $49/month ($0.196–$0.133 per record) | ≥250 Collect, 500 Search credits monthly; all three endpoints; technical support; documentation. | https://coresignal.com/pricing/ |
| Pro | From $800/month ($0.080–$0.050 per record) | ≥10,000 Collect, 20,000 Search credits monthly; dedicated account manager; all three endpoints. | https://coresignal.com/pricing/ |
| Premium | From $1,500/month ($0.030–$0.005 per record) | ≥50,000 Collect, 150,000 Search credits monthly; dedicated account manager; Historical Headcount API; Employee API webhooks. | https://coresignal.com/pricing/ |
| Datasets (flat files) | From $1,000 (yearly contract, monthly payments) | Companies, employees, or jobs datasets; 15+ web sources; daily/weekly/monthly refresh; premium support. | https://coresignal.com/pricing/ |
| Yearly discount | 20% off when paid yearly | All credits delivered upfront for any API plan paid yearly. | https://coresignal.com/pricing/ |

Pricing is fully public and credit-based. Per-record price drops sharply with plan tier. No seat-based or platform-fee component on the API plans.

## Target Audience & ICP

- **Industries called out:** Sales tech, HR tech / recruitment, Investment / VC / private equity, Market research, AI / ML / LLM builders, Marketing
- **Company size called out:** Not explicitly segmented by company size on reviewed pages — pricing tiers and self-service free trial suggest startups through enterprise via dataset contracts.
- **Persona / role focus:** Engineers / developers, Data scientists / ML engineers, Product teams building data-driven products, Sales operations / RevOps embedding data into pipelines, Recruitment / talent intelligence teams, Investment analysts (deal sourcing, monitoring)
- **Use cases promoted:**
  - Lead enrichment and prospecting
  - AI/LLM training and AI-agent grounding (data-for-AI)
  - Talent sourcing and talent analytics
  - Investment intelligence and deal sourcing
  - Competitive intelligence and market research
  - Trend forecasting (skills demand, hiring activity)
  - B2B intent-signal generation

## Integrations & Ecosystem

- **CRMs:** _Integration list not surfaced on reviewed pages._ No Salesforce, HubSpot, or MS Dynamics native app surfaced.
- **Sales engagement / outreach:** _Integration list not surfaced on reviewed pages._
- **Data / enrichment:** Databricks Marketplace listing for sample employee data (surfaced via SERP only).
- **Other notable integrations:** n8n (native node, launched March 2026 — the only named integration on docs.coresignal.com/integrations); webhooks for change notifications; cloud delivery (push to customer cloud bucket); Swagger UI for testing.

The integrations docs page lists ONLY n8n as a named integration — i.e. integration is the customer's job, not a managed app marketplace.

## Differentiators (vs the broader category)

- API-first / developer-first delivery — no UI seat product (source: https://coresignal.com/solutions/web-data-apis/).
- 176 ms average API response time (source: https://coresignal.com/solutions/company-data-api/).
- Three processing levels (Base / Clean / Multi-Source) on every dataset (source: https://coresignal.com/solutions/company-data-api/).
- Founding member of the Ethical Web Data Collection Initiative (EWDCI); transparent, public-only data sourcing as a compliance moat (source: https://coresignal.com/about-us/).
- Elasticsearch Query DSL exposed to customers — a power-user search interface unusual among B2B data vendors (source: https://coresignal.com/solutions/web-data-apis/).
- Public credit-based pricing starting at $0 free trial → $49 Starter; transparent per-record economics (source: https://coresignal.com/pricing/).

## Crossover With ZoomInfo

- **Direct overlap:**
  - **APIs & MCP ↔ Coresignal Company / Employee / Jobs APIs + Agentic Search API.** Both pitch developer-grade access to B2B data for AI agents and downstream product teams. Coresignal's homepage hero is "Data intelligence layer for AI agents" — the same agent-builder audience ZoomInfo's MCP server targets (source: https://coresignal.com/).
  - **Data foundation (companies, contacts, technographics) ↔ Coresignal Company Data API + Employee Data API + Datasets.** Coresignal pitches 75M+ company records with 500+ fields and 865M+ employee profiles, directly targeting the same firmographic + people-data layer ZoomInfo's Data pillar covers (source: https://coresignal.com/).
- **Adjacent overlap:**
  - **ZoomInfo Sales / GTM Workspace (seller front-end) ↔ Coresignal data-for-sales use-case page.** Coresignal frames the same outcomes (lead enrichment, intent signal generation, prospecting) but delivers via raw data feeds — customers must build the seller UX themselves (source: https://coresignal.com/use-cases/sales-data).
- **No overlap:**
  - Sales engagement, dialer, conversation intelligence (Chorus, AI agent layer-drafted outreach) — Coresignal sells data only.
  - ABM / orchestration / GTM Studio surface — no marketing automation, campaign orchestration, audience-as-a-service, or Salesforce/HubSpot enrichment app.
  - Verified business phone numbers and direct dials — Coresignal collects only publicly available, strictly business-related data; verified-phone / direct-dial coverage is not surfaced on any reviewed page.
  - Intent data / behavioral signals at the buyer level — Coresignal mentions "B2B intent data" but the pitch is hiring-signal-style derivative intent (e.g., a company is hiring engineers → buying signal), not consented buyer-behavior intent.
- **Their pitch against ZoomInfo (if found):** _No public comparison page surfaced in SERP results._ Coresignal's footer lists Crustdata, Bright Data, People Data Labs, and Mixrank as its named competitors; it does not publish a Coresignal-vs-ZoomInfo page.

## Messaging & Positioning Notes

- **Top-line value prop (their words):** "Data intelligence layer for AI agents — fresh company, employee, and jobs records in real time."
- **Recurring proof points:**
  - 700+ customers globally; 9+ years in market; 4.5B+ data records; 176 ms API response time
  - Founding member of the Ethical Web Data Collection Initiative (EWDCI), 2023
  - Named top data provider by Datarade (2023 and 2024)
  - Customer testimonial: "+25% in net new pipeline in 2 months, +40% after 6 months"
- **Tone / category framing:** "Public web data provider" / "B2B data API" / "data intelligence layer for AI agents" — explicitly positions away from sales-intelligence UI category and toward developer / data infrastructure category.

## Flags & Limitations

- `vs_brand_missing` — Coresignal does NOT publish a Coresignal-vs-ZoomInfo page.
- `manual_review:hq_not_stated@https://coresignal.com/about-us/` — about-us page does not state HQ on reviewed text.
- `manual_review:funding_ownership_not_surfaced` — funding history / ownership structure not on any reviewed page.
- `manual_review:integrations_thin@https://docs.coresignal.com/integrations` — official integrations docs page lists only n8n.

## Sources

| URL | Status | Used For |
|---|---|---|
| https://coresignal.com/ | success | homepage; value prop; product summary; proof points |
| https://coresignal.com/pricing/ | success | pricing tiers; datasets pricing; FAQ |
| https://coresignal.com/solutions/web-data-apis/ | success | API portfolio overview; differentiators; pricing snippet |
| https://coresignal.com/solutions/company-data-api/ | success | Company API features; processing levels; ICP per-industry |
| https://docs.coresignal.com/integrations | success | integrations (n8n only); thin-content flag |
| https://coresignal.com/about-us/ | success | company snapshot; EWDCI; press mentions; story |
| https://coresignal.com/use-cases/data-for-ai | success | AI / agent ICP framing; sales-intelligence (AI SDR) use cases |
| https://coresignal.com/use-cases/sales-data | success | sales ICP; lead enrichment; intent signal framing |
| https://coresignal.com/solutions/employee-data-api | success | Employee API features; processing levels; webhooks |
| https://coresignal.com/solutions/jobs-data-api | success | Jobs API features; processing levels |
