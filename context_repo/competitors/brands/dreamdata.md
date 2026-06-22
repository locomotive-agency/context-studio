---
type: competitive-landscape
id: ctx.competitors.brands.dreamdata
title: Dreamdata
description: ''
scope_id: zoominfo
durability: persistent
criticality: hybrid
status: approved
provenance: competitor-wiki/wiki/competitors/dreamdata.md
source_type: source-document
source_path: competitor-wiki/wiki/competitors/dreamdata.md
tags:
- competitive-landscape
- competitors
---

---
type: competitor
brand: Dreamdata
slug: dreamdata
primary_url: https://dreamdata.io/
category: analytics
secondary_categories: [abm, intent-data, marketing-automation]
positioning_archetype: point-solution
competes_with_zi_pillars: [gtm_context_graph, universal_access]
competes_with_zi_products: [ZoomInfo Marketing, GTM Studio, GTM Context Graph, ZoomInfo Operations, WebSights]
icp_relevance: [marketing_demandgen, revops_gtm_eng]
pricing_model: hybrid_partial_public
has_free_tier: true
has_mcp_server: false
has_conversation_intelligence: false
has_abm_advertising: true
has_predictive_scoring: true
analyst_recognition: [#1 B2B Attribution vendor on G2]
research_depth: full
date_researched: 2026-05-08
flags: [vs_brand_missing, manual_review:funding_from_third_party_only, manual_review:starter_pricing_third_party, manual_review:industries_not_called_out, manual_review:employee_size_unavailable]
sources_count: 10
sub_products: [dreamdata--audience-hub, dreamdata--signals, dreamdata--b2b-attribution, dreamdata--customer-journeys, dreamdata--data-platform]
---

# Dreamdata

## Sub-products

- [[dreamdata--audience-hub|Dreamdata Audience Hub]] — competes with ZoomInfo Marketing
- [[dreamdata--signals|Dreamdata Signals]] — competes with Intent Data
- [[dreamdata--b2b-attribution|Dreamdata B2B Attribution]] — competes with ZoomInfo Marketing
- [[dreamdata--customer-journeys|Dreamdata Customer Journeys]] — competes with GTM Context Graph
- [[dreamdata--data-platform|Dreamdata Data Platform]] — competes with GTM Context Graph

## Summary

Dreamdata is a B2B revenue attribution and activation platform sold to B2B marketers, marketing ops, and agencies; it unifies data from CRM, marketing automation, ads, and website tracking into an account-based customer journey, then layers AI attribution, audience build/sync, and intent signals on top. Dreamdata directly overlaps ZoomInfo Marketing and the marketing-side of GTM Studio on audience activation, ABM measurement, and intent-driven prioritization, but consumes (rather than sells) third-party B2B contact data — listing ZoomInfo, Cognism, Lusha, Clearbit, Lead411, Apollo and others as data sources. They do not sell into Sales prospecting (no GTM Workspace analog), conversation intelligence (no Chorus analog), or website chat. No public Dreamdata-vs-ZoomInfo page surfaced; the closest first-party framing is on their ZoomInfo integration page.

## Company Snapshot

| Field | Value |
|---|---|
| Category | B2B revenue attribution & marketing analytics / B2B Customer Data Platform (Activation & Attribution) |
| Founded / HQ | HQ Copenhagen, Denmark (Kalvebod Brygge 39, 1560 Copenhagen); secondary office at 535 8th Avenue, 12th Floor, New York, NY 10018; CVR 39855224, copyright dated 2019–2026 (source: https://dreamdata.io/use-cases) |
| Funding / Ownership | Reported $55M raise in Nov 2025 (per demandgenreport.com SERP snippet); Latka entry reports $11.5M raised and $30M valuation in 2024 with $3M revenue / 120 customers — third-party only, not on Dreamdata's own pages — see flags |
| Employee size | _Not available — see flags._ |
| Primary buyer | B2B Marketers; Marketing Ops; Agencies (per https://dreamdata.io/for-marketers and the /use-cases solutions menu listing "For Marketers", "For Marketing Ops", "For Agencies") |

## Product Offerings

### Customer Journeys (B2B Customer Journey Map)

> **Wiki:** [[dreamdata--customer-journeys]]

- **What it does:** Out-of-the-box interactive customer journey timelines that show every touchpoint (known and anonymous) an account makes as it moves through the funnel.
- **Key features:**
  - Interactive customer journey timelines with every touch per account
  - Multi-stakeholder view — every contact (known and anonymous) involved in a deal
  - Identifies key personas driving deals via stakeholder activity analysis
  - Channel/source/campaign overlay to see how efforts combined to win the deal
  - Stage-duration analysis to identify bottlenecks
  - LinkedIn + G2 intent data integration as an official partner for anonymous account-level touches
- **Source URL:** https://dreamdata.io/use-cases/understand-customer-journey

### B2B Attribution (Performance / Revenue Attribution)

> **Wiki:** [[dreamdata--b2b-attribution]]

- **What it does:** Multi-touch B2B attribution that connects marketing and sales touchpoints to pipeline and revenue across long, multi-stakeholder buyer journeys.
- **Key features:**
  - 11 pre-built attribution models (First Touch, Linear, Last Touch, U-Shaped, W-Shaped, all four with Non-Direct variants, plus Data-Driven)
  - Custom attribution models that can be designed by the user
  - Attribution to pipeline stages (MQL, SQL, New Business)
  - Time-to-revenue metric (Dreamdata cites avg B2B journey of 272 days)
  - Account-based metrics rather than user/lead-only
  - Credit to offline touches
  - AI-powered report summaries (Advanced plan)
- **Source URL:** https://dreamdata.io/b2b-attribution

### Audience Hub

> **Wiki:** [[dreamdata--audience-hub]]

- **What it does:** Audience builder and activation layer that creates dynamic B2B audiences from unified GTM data and syncs them daily to LinkedIn, Google, Meta, and Microsoft Ads.
- **Key features:**
  - Unlimited filters across web visits, ad clicks, pipeline stages, intent signals, CRM properties, firmographics
  - Direct daily syncs to LinkedIn, Google, Meta, Microsoft Ads
  - Conversion syncs (offline conversions to ad platforms) — LinkedIn CAPI cited at 20% CPA reduction and 31% lift in attributed conversions
  - LinkedIn company match rates above 90% vs industry average 29-62%
  - Audience Reach Report — measures % of target accounts exposed
  - Webhooks for Zapier, Clay, or any webhook-enabled tool
- **Source URL:** https://dreamdata.io/audience-hub

### Signals (AI Buying Intent)

> **Wiki:** [[dreamdata--signals]]

- **What it does:** AI engine that scans all GTM data to identify hidden high-intent signals correlated with pipeline and revenue, then notifies sales and feeds activation workflows.
- **Key features:**
  - AI engine combining statistical machine learning + generative AI (powered by Google Gemini)
  - Custom Engagement Score — user-defined which signals matter
  - Slack/Teams notifications when high-intent accounts are detected
  - CRM Syncs to HubSpot/Salesforce — creates SDR follow-up tasks, enrolls accounts in sales sequences
  - Chrome Extension to surface signals on CRM, websites, or LinkedIn profiles
  - Identifies up to 80% of anonymous website visitors via proprietary IP-to-company resolution
- **Source URL:** https://dreamdata.io/signals

### Data Platform (B2B Customer Data Platform)

> **Wiki:** [[dreamdata--data-platform]]

- **What it does:** Automated B2B CDP that collects, models, and unifies data from across the GTM tech stack into a clean, account-based 360° customer journey ready for AI activation.
- **Key features:**
  - Automated data collection via proprietary tracking script + GTM stack integrations
  - Unified, account-based data model with deduplication, standardisation, automated UTM mapping
  - Cookie & cookie-less tracking
  - Data Hub for centralized control over what enters reporting/activation
  - Direct warehouse access — BigQuery, Snowflake, Redshift, Azure Storage, AWS S3
  - SOC 2 Type II certified; GDPR compliant; Google Cloud–based (EU data centres by default)
- **Source URL:** https://dreamdata.io/data-platform

## Pricing

| Tier | Price | What's included | Source |
|---|---|---|---|
| Free | $0/month | B2B Web Analytics, Cookie & Cookie-less Tracking, Engagement Scoring, Company Identification, Audience Builder, Slack/Teams Notifications, Ad Spend Report, B2B Benchmarks. Limits: 2 months user history, 5 seats, 3 stage models, 2 notifications, 1 sync. Self-serve onboarding + Slack community + AI Chat support. | https://dreamdata.io/pricing |
| Activation & Attribution (Advanced) | Custom Pricing | All Dreamdata capabilities unlocked: AI activation, advanced attribution & optimization, custom limits/volumes, full onboarding, dedicated CSM + Technical Manager, solutions consulting, data science support. Advanced data controls: Event Builder, Custom UTM Mapping, Data Model Scheduler, Custom Data Sources, Multiple Business Units, SSO/SAML. | https://dreamdata.io/pricing |

Dreamdata's own pricing page lists only Free + "Custom Pricing" for the Advanced tier. Third-party sources (Spectacle, Vendr, Software Advice, prospeo, zenabm, heeet) cite an "Activation Starter" plan at ~$750/month and Professional contracts of $25K–$50K/year, but those numbers are NOT on Dreamdata's own pricing page — see flags.

## Target Audience & ICP

- **Industries called out:** _No specific verticals named on extracted pages — see flags._ Customer success stories surface across SaaS / fintech / HR-tech (Cognism, Moss, Oyster, Eftsure, Coverflex, Clio, Pixelz, Profound North) but no industry vertical is positioned in headline copy.
- **Company size called out:** Smaller teams (Free + implied Starter) and larger teams (Advanced — custom pricing). No SMB / mid-market / enterprise framing on the pricing page itself.
- **Persona / role focus:** B2B Marketers, Marketing Ops, Agencies (the three "Solutions" links in the site navigation). Sales is a downstream consumer of Signals notifications and CRM Syncs, not a primary buyer.
- **Use cases promoted:** Target the right accounts; understand the customer journey; identify and activate high-intent accounts; optimize ad spend; optimize content marketing; optimize field marketing; report on marketing's impact; allocate marketing budget; report on marketing spend (source: https://dreamdata.io/use-cases).

## Integrations & Ecosystem

- **CRMs:** HubSpot, Salesforce, Microsoft Dynamics, Pipedrive (source: https://dreamdata.io/integrations).
- **Sales engagement / outreach:** Outreach, Salesloft, Apollo.io, LinkedIn Sales Navigator, Reachdesk, Sendoso, Chilli Piper.
- **Data / enrichment:** 6sense, Albacross, Clearbit, Dealfront, Rollworks, Snitcher, Triblio, Demandbase, ZoomInfo, ZoomInfo Enrichment, Cognism, Lusha, Seamless.ai, Lead411, LeadIQ, Breeze Intelligence, BuiltWith, People Data Labs, Apollo.io Enrichment.
- **Other notable integrations:**
  - Marketing automation: HubSpot, Marketo, Pardot, Oracle Eloqua, Salesforce Marketing Cloud
  - Ad platforms: LinkedIn Ads, Google Ads, Google Search Console, Meta Ads, Bing Ads, Microsoft Ads, Twitter Ads, Capterra, G2, NextRoll, Reddit Lead Ads, Facebook Lead Ads, Google Lead Form Ads, TrustRadius
  - Tracking: analytics.js, Segment, Zapier, Drift, Sleeknote, Calendly Embedded, Google Tag Manager
  - Customer success: Intercom
  - BI: Looker Studio, Tableau, Looker, PowerBI, Metabase, Sisense, Google Connected Sheets
  - Reverse ETL: Hightouch, Census
  - Data warehouses: Snowflake, Google BigQuery, Microsoft Azure Storage, Amazon Redshift, AWS S3
  - Other: Stripe, Shopify, BigCommerce, Vanta, SafeBase, Walnut, Supademo, Consensus, Livestorm

## Differentiators (vs the broader category)

- B2B-purpose-built attribution: 11 pre-built attribution models tailored to long (avg 272-day), multi-stakeholder (avg 10-stakeholder) B2B journeys — explicitly positioned against B2C tooling like Google Analytics and CRM 'original source' fields (source: https://dreamdata.io/b2b-attribution).
- Open warehouse access: free customer access to modeled data in BigQuery (and Snowflake/Redshift/Azure Storage/S3) for custom queries, BI/ML, or reverse ETL — uncommon among point-attribution tools (source: https://dreamdata.io/data-platform).
- Industry-leading anonymous-visitor identification: up to 80% of anonymous website visitors identified via proprietary IP-to-company resolution, even when cookies are declined (source: https://dreamdata.io/signals).
- Audience match rates of 90%+ for LinkedIn company audiences vs. industry typical 29–62%, driven by unified GTM data feeding the audience build (source: https://dreamdata.io/audience-hub).
- Free plan with real B2B analytics (web analytics, company identification, engagement scoring, audience builder, Slack/Teams notifications) — usage-tier sales motion vs. enterprise-only competitors (source: https://dreamdata.io/pricing).
- AI Signals built on Google Gemini + statistical ML, scanning all GTM data (not just first-party site) to find behaviour patterns that correlate with pipeline (source: https://dreamdata.io/signals).

## Crossover With ZoomInfo

- **Direct overlap:** Dreamdata Audience Hub + Signals + Performance Attribution compete head-to-head with **ZoomInfo Marketing** (ABM, audience activation, marketing measurement) and adjacent to **GTM Studio** (marketer / RevOps audience build & play orchestration). Dreamdata builds dynamic audiences from unified GTM data, syncs to LinkedIn/Google/Meta/Microsoft Ads daily, surfaces AI-identified intent signals to Slack/Teams + HubSpot/Salesforce, and runs full attribution from anonymous touch through closed-won — the same workflow ZoomInfo Marketing / GTM Studio runs on the marketer side (source: https://dreamdata.io/audience-hub, https://dreamdata.io/pricing).
- **Adjacent overlap:** Dreamdata's Data Platform (B2B CDP with open warehouse access) is adjacent to ZoomInfo's **GTM Context Graph** in that both unify GTM data into an account-based model — but ZoomInfo's pillar adds the 500M-contact data foundation and Chorus conversation intelligence, while Dreamdata is BYO third-party data (and lists ZoomInfo as one such source). Cleaning/standardisation/UTM-mapping also overlaps **ZoomInfo Operations** on data quality, though Dreamdata explicitly does not maintain a contact/company database (source: https://dreamdata.io/data-platform, https://dreamdata.io/integrations).
- **No overlap:** Dreamdata does not sell a B2B contact/company database — they integrate ZoomInfo, Cognism, Lusha, Clearbit, Lead411, Seamless.ai, Apollo Enrichment, People Data Labs, etc. as data sources. They do not have a seller-prospecting workspace (no **GTM Workspace** / **ZoomInfo Sales** analog), no conversation intelligence (no **Chorus** analog), and no data-powered website chat (no **ZoomInfo Chat** analog) — though they integrate with Drift as a chat-tracking source (source: https://dreamdata.io/integrations, https://dreamdata.io/signals).
- **Their pitch against ZoomInfo (if found):** No public head-to-head Dreamdata-vs-ZoomInfo page surfaced in SERP results. The closest first-party framing is on their ZoomInfo integration page: _"With Dreamdata you gain free access to raw data from across your tech stack. Move away from only accessing siloed data displayed inside ZoomInfo and your other [tools]"_ (source: https://dreamdata.io/integration/zoominfo-integration, snippet from SERP). Notably, Dreamdata is also listed in ZoomInfo's own app marketplace (https://market.zoominfo.com/app/dreamdata), suggesting partnership rather than direct head-to-head positioning.

## Messaging & Positioning Notes

- **Top-line value prop (their words):** Dreamdata is a "B2B Activation & Attribution Platform" that provides "the most complete B2B customer journey map anywhere," empowering marketers to build and activate precise audiences, leverage AI signals, and measure what truly drives revenue (source: https://dreamdata.io/).
- **Recurring proof points:** #1 B2B Attribution vendor on G2; aggregated benchmarks across +66M sessions / +3.5M customer journeys; named customer outcomes — Cognism (5x more qualified opportunities with AI Signals), Moss (74% reduction in cost per lead via Audience Hub), Oyster (28% reduction in CAC), Eftsure (40% reduction in cost per lead via LinkedIn CAPI), and average LinkedIn CAPI customers seeing 20% CPA reduction + 31% lift in attributed conversions.
- **Tone / category framing:** Marketer-led, AI-driven, account-based; positions explicitly against B2C analytics (Google Analytics) and CRM 'original source' attribution as inadequate for B2B. Repeated framing: "AI is only as good as the data it's built on" — sells the data foundation as the prerequisite for activation.

## Flags & Limitations

- `vs_brand_missing` — no public Dreamdata-vs-ZoomInfo comparison page surfaced; closest first-party framing is the ZoomInfo integration page, and Dreamdata appears in ZoomInfo's own app marketplace (suggesting partnership).
- `manual_review:funding_from_third_party_only` — $55M Nov-2025 funding (demandgenreport.com SERP snippet) and $11.5M raised / $30M valuation in 2024 (getlatka SERP snippet) were not on extracted Dreamdata pages; reported with caveat.
- `manual_review:starter_pricing_third_party` — multiple third-party sources cite an "Activation Starter" plan at ~$750/month, but Dreamdata's own pricing page lists only Free + "Custom Pricing" for Advanced. Reported with caveat.
- `manual_review:industries_not_called_out` — no specific industry verticals named on extracted pages; ICP is industry-agnostic B2B (success-story customers span SaaS / fintech / HR-tech / legal-tech).
- `manual_review:employee_size_unavailable` — employee headcount not surfaced on extracted Dreamdata pages.

## Sources

| URL | Status | Used For |
|---|---|---|
| https://dreamdata.io/ | success | homepage, value prop, proof points |
| https://dreamdata.io/pricing | success | pricing tiers, plan features, ICP |
| https://dreamdata.io/b2b-attribution | success | B2B Attribution product, attribution models, differentiators |
| https://dreamdata.io/integrations | success | integrations (CRM, MAP, ads, BI, warehouse, enrichment) |
| https://dreamdata.io/for-marketers | success | ICP — Marketers, product feature recap |
| https://dreamdata.io/data-platform | success | Data Platform product, security/compliance, differentiators |
| https://dreamdata.io/use-cases/understand-customer-journey | success | Customer Journeys product |
| https://dreamdata.io/signals | success | Signals product, AI architecture, anonymous-ID differentiator |
| https://dreamdata.io/audience-hub | success | Audience Hub product, match rates, conversion syncs |
| https://dreamdata.io/use-cases | success | Use cases inventory, persona/solutions menu |
