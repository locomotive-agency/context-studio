---
brand: HG Insights
slug: hg-insights
primary_url: https://www.hginsights.com/
category: intent-data
secondary_categories:
- b2b-data
- market-intelligence
- abm
positioning_archetype: enterprise-platform
competes_with_zi_pillars:
- data
- gtm_context_graph
- universal_access
competes_with_zi_products:
- Data (Pillar 1)
- Intent Data
- ZoomInfo Marketing
- ZoomInfo Operations
- ZoomInfo Sales
- GTM Workspace
- APIs & MCP
icp_relevance:
- revops_gtm_eng
- marketing_demandgen
- sales_ae_sdr
- developer_agent_builder
pricing_model: enterprise_only
has_free_tier: false
has_mcp_server: true
has_conversation_intelligence: false
has_abm_advertising: true
has_predictive_scoring: true
analyst_recognition:
- Trusted by 90% of Fortune 500 Tech Companies
- SOC 2 Type II
research_depth: full
date_researched: 2026-05-08
flags:
- pricing_blocked
- manual_review:vs_brand_first_party_thin
- manual_review:trustradius_acquisition_context
- manual_review:recent_ownership_change
- manual_review:company_snapshot_thin
sources_count: 9
sub_products:
- hg-insights--rgi-platform
- hg-insights--rgi-fabric
- hg-insights--intent-driven-leads
- hg-insights--customer-voice
- hg-insights--market-analyzer
- hg-insights--sales-copilot
type: competitive-landscape
id: ctx.competitors.brands.hg-insights
title: HG Insights
description: ''
scope_id: zoominfo
durability: persistent
criticality: hybrid
status: approved
provenance: competitor-wiki/wiki/competitors/hg-insights.md
source_type: competitor
source_path: competitor-wiki/wiki/competitors/hg-insights.md
tags:
- competitive-landscape
- competitors
resource: https://www.hginsights.com/
---

# HG Insights

## Sub-products

- [[hg-insights--rgi-platform|HG RGI Platform]] — competes with GTM Workspace
- [[hg-insights--rgi-fabric|HG RGI Fabric]] — competes with Data (Pillar 1)
- [[hg-insights--intent-driven-leads|HG Intent-Driven Leads]] — competes with Intent Data
- [[hg-insights--customer-voice|HG Customer Voice (powered by TrustRadius)]] — competes with ZoomInfo Marketing
- [[hg-insights--market-analyzer|HG Market Analyzer]] — competes with ZoomInfo Marketing
- [[hg-insights--sales-copilot|HG Sales Copilot]] — competes with ZoomInfo Sales

## Summary

HG Insights sells "Revenue Growth Intelligence" — a technographics-, IT-spend-, and buyer-intent platform aimed at GTM, RevOps, marketing, and strategy leaders inside B2B technology companies (it claims 90% of the Fortune 500 tech segment). After acquiring TrustRadius in June 2025, HG layered verified 2nd-party buyer intent and a 12M-evaluator review community on top of its existing technographic + IT spend datasets, and now ships a productized RGI Platform with three AI copilots (Market Analyzer, Data Studio, Sales Copilot), an MCP server, and an RGI Agent Builder. That overlaps directly with ZoomInfo's Pillar 1 data foundation (technographics + intent), with ZoomInfo Operations (CRM/MDM enrichment), and increasingly with the GTM Workspace seller surface — though HG's contact dataset is positioned as "no extra license" enrichment inside Sales Copilot rather than a 500M-contact primary database. Third-party reviewers frame the choice as "account strategy (HG) vs rep activation (ZoomInfo)" rather than full substitution.

## Company Snapshot

| Field | Value |
|---|---|
| Category | Revenue Growth Intelligence — technographics + IT spend + buyer intent platform |
| Founded / HQ | _Not available — see flags._ |
| Funding / Ownership | Backed by Riverwood Capital (board member quoted in TrustRadius acquisition press release); acquired TrustRadius June 2025, which now operates as an independent subsidiary (source: https://hginsights.com/blog/hg-insights-acquires-trustradius/). |
| Employee size | _Not available — see flags._ |
| Primary buyer | GTM and RevOps leaders, marketing/ABM owners, sales and strategy leadership, data analysts; pitched at B2B technology companies. |

## Product Offerings

### Revenue Growth Intelligence (RGI) Platform

> **Wiki:** [[hg-insights--rgi-platform]]

- **What it does:** SaaS GTM platform that unifies HG's market, account, technographic, IT spend, and buyer intent data with first-party data, then activates it through AI copilots and agentic workflows.
- **Key features:**
  - Three AI copilots: Market Analyzer (TAM/SAM/SOM, ICP, whitespace, territory optimization), Data Studio (no-code propensity models, scoring, ABM, CRM enrichment), Sales Copilot (signal-based selling, AI sales plays, daily prioritization, competitive displacement)
  - Contact Intelligence with multi-provider waterfall enrichment and real-time company validation, included natively in Sales Copilot (credit-based, no separate third-party data subscription)
  - Platform MCP server connects HG intelligence to external AI tools like Claude, ChatGPT, and Cursor
  - Integrates with Salesforce, HubSpot, Marketo, Eloqua, Snowflake; pushes workflow actions into Outreach, Salesloft, Gong Engage
  - Buyer Intent module combines TrustRadius-sourced 2nd-party intent signals with account context for scoring and targeting
- **Source URL:** https://hginsights.com/product/rgi-platform

### Revenue Growth Intelligence (RGI) Fabric

> **Wiki:** [[hg-insights--rgi-fabric]]

- **What it does:** Underlying unified B2B data layer (firmographics, technographics, IT spend, buying centers, competitive, buyer intent) delivered via API, S3, and CRM connectors to power MDM/CRM enrichment and AI agents.
- **Key features:**
  - Technographics across 20,000+ products with behind-the-firewall detection, deployment intensity, maturity, and location data
  - IT spend forecasting across 140+ categories (hardware, software, services, communications) at account-level granularity
  - Layered buyer intent signals (problem/solution/product aware) including 2nd-party signals from TrustRadius
  - AI Maturity Index, Data Management Maturity, and AI Intent specialty datasets
  - Cloud Centricity / cloud adoption data covering 10M+ cloud companies
  - REST API (Company Match, Company Installs, Intent endpoints), S3 data exchange, Salesforce/HubSpot bi-directional integration, MCP server
  - RGI Agent Builder for developers to construct purpose-built AI agents on the Fabric
- **Source URL:** https://hginsights.com/product/rgi-fabric

### Intent-Driven Leads

> **Wiki:** [[hg-insights--intent-driven-leads]]

- **What it does:** Opt-in, ICP-qualified leads sourced from the TrustRadius buyer community, filtered by sales propensity and delivered to the customer's GTM stack.
- **Key features:**
  - Bottom-funnel intent context drawn from active TrustRadius reviewers and category researchers
  - ICP- and propensity-filtered to lift conversion and pipeline velocity
  - Engages buyers actively researching the customer's product, competitors, or category
  - Delivered into customer's marketing/sales systems for immediate nurturing or outreach
- **Source URL:** https://hginsights.com/product/packaging-and-pricing/

### Customer Voice (powered by TrustRadius)

> **Wiki:** [[hg-insights--customer-voice]]

- **What it does:** Customer advocacy and review-syndication product that turns verified TrustRadius reviews into web widgets, sales proof, and SEO/SEM content.
- **Key features:**
  - TrustQuotes and Site Widgets that embed verified review snippets on web/landing pages
  - Review sourcing campaigns with reviewer identity verification and human moderation
  - Reference management for advocate routing, calls, quotes, and case studies
  - Competitive takeout content built from peer reviews of competitor products
  - Voice-of-the-Customer widget for SEO performance
  - TrustQuotes for Salesforce integration (cited in HG's Terms of Service) syncing curated review content into Salesforce
- **Source URL:** https://hginsights.com/product/customer-voice

### Market Analyzer (copilot inside RGI Platform)

> **Wiki:** [[hg-insights--market-analyzer]]

- **What it does:** AI-driven conversational analytics for TAM/SAM/SOM sizing, ICP design, whitespace identification, and competitive analysis.
- **Key features:**
  - Conversational queries to size markets and explore segments
  - Whitespace mapping for expansion targeting
  - Competitive displacement and "where competitors are weak" analysis
  - Territory optimization inputs for RevOps
- **Source URL:** https://hginsights.com/product/rgi-platform

### Sales Copilot (inside RGI Platform)

> **Wiki:** [[hg-insights--sales-copilot]]

- **What it does:** Seller-facing module that turns buyer signals into prioritized accounts, account research, and outreach playbooks.
- **Key features:**
  - Daily prioritization workflows and signal-triggered alerts
  - AI-generated account briefs and competitive context
  - Activates contact reveals and outreach into Salesforce, Gong, Outreach, Salesloft, HubSpot
  - Custom playbooks and personalized outreach sequences
- **Source URL:** https://hginsights.com/solutions-use-role/sales/

## Pricing

_Pricing not publicly listed — see flags._

| Tier | Price | What's included | Source |
|---|---|---|---|
| All packages (RGI Platform, RGI Fabric, Intent-Driven Leads, Customer Voice) | Contact sales (gated; form behind cookie consent) | Modular packaging across the four product lines; flexible scope by data coverage, users, AI capabilities, and integrations | https://hginsights.com/product/packaging-and-pricing/ |
| Third-party benchmark (prospeo.io) | $23,498–$158,108/yr range; ~$75,389 median | Benchmark spread/median across deals (not vendor-published) | https://prospeo.io/s/hg-insights-vs-zoominfo |

## Target Audience & ICP

- **Industries called out:** B2B technology (primary; "Trusted by 90% of Fortune 500 Tech Companies"), enterprise SaaS, cloud and infrastructure vendors (source: https://hginsights.com/).
- **Company size called out:** Enterprise (primary), mid-market.
- **Persona / role focus:** GTM and RevOps leaders, marketing/ABM teams, sales leadership and AEs, strategy / corporate development, data analysts (AI agent infrastructure), executives and investors validating market opportunity (source: https://hginsights.com/).
- **Use cases promoted:**
  - TAM/SAM/SOM market sizing
  - ICP design and account prioritization
  - Territory design and quota planning
  - Competitive displacement / takeout campaigns
  - Whitespace and expansion analysis
  - ABM optimization and signal-based selling
  - CRM/MDM data enrichment with technographics + spend + intent
  - Customer advocacy / review syndication (Customer Voice)

## Integrations & Ecosystem

- **CRMs:** Salesforce (bi-directional, plus TrustQuotes for Salesforce), HubSpot (bi-directional). Microsoft Dynamics not surfaced on reviewed pages.
- **Sales engagement / outreach:** Outreach, Salesloft, Gong Engage (source: https://prospeo.io/s/hg-insights-vs-zoominfo).
- **Data / enrichment:** Snowflake, Amazon S3 (native data exchange), BigQuery, Marketo, Eloqua (source: https://hginsights.com/product/rgi-fabric).
- **Other notable integrations:** MCP server (HG MCP) for Claude, ChatGPT, Cursor, and other AI agents; REST API (Company Match, Company Installs, Intent endpoints); product analytics — Amplitude, Segment, Mixpanel; Chrome extension and iframe embeds for in-workflow insights; Intercom (push destination); Gong (revenue intelligence destination).

## Differentiators (vs the broader category)

- Technographics depth: 20,000+ products tracked with behind-the-firewall detection, deployment intensity, maturity, and location-level granularity (positioned as "best-in-class technographics") (source: https://hginsights.com/product/rgi-fabric).
- Bottom-up IT spend forecasting across 140+ categories with 12-month projections at account level — distinct from generic firmographic data (source: https://hginsights.com/product/rgi-fabric).
- TrustRadius acquisition (June 2025) layered verified 2nd-party buyer intent and a 12M+ annual B2B technology evaluator community on top of HG's technographic and spend datasets (source: https://hginsights.com/blog/hg-insights-acquires-trustradius/).
- MCP server natively exposes HG intelligence to Claude, ChatGPT, Cursor and other AI agents — positioned as "industry's first unified platform built on agentic infrastructure" (source: https://hginsights.com/product/rgi-platform).
- AI Maturity Index, Data Management Maturity, and AI Intent specialty datasets to identify where AI growth is accelerating in target accounts (source: https://hginsights.com/product/rgi-fabric).
- Customer Voice product (TrustRadius-powered review syndication and customer advocacy) — a category most pure-play data vendors do not offer (source: https://hginsights.com/product/customer-voice).

## Crossover With ZoomInfo

- **Direct overlap:**
  - **ZoomInfo Data foundation (Pillar 1) (technographics across 30K+ technologies; 500M contacts) ↔ HG RGI Fabric.** HG positions RGI Fabric as "unified firmographic, technographic, spend, contracts, and buyer intent" delivered via API/S3/CRM — same enrichment-layer use case ZoomInfo Operations and the ZoomInfo Data API serve (source: https://hginsights.com/product/rgi-fabric).
  - **ZoomInfo Marketing + Intent Data (intent + ABM) ↔ HG Buyer Intent + Intent-Driven Leads + ABM Optimization use case.** HG's layered buyer intent (problem/solution/product aware) plus TrustRadius 2nd-party intent and ICP-filtered intent leads compete head-to-head with ZoomInfo's intent topics and ABM motion (source: https://hginsights.com/blog/hg-insights-acquires-trustradius/).
  - **ZoomInfo Sales / GTM Workspace (Sales Copilot, signal-based selling) ↔ HG RGI Platform Sales Copilot + Contact Intelligence.** HG's Sales Copilot turns buyer signals into "tasks, emails, and call prompts" and now reveals verified emails and phone numbers natively (waterfall enrichment, real-time company validation) — a direct shot at ZoomInfo's contact-data + seller-execution surface (source: https://hginsights.com/product/rgi-platform).
  - **ZoomInfo APIs & MCP (mcp.zoominfo.com) ↔ HG MCP + REST API + RGI Agent Builder.** HG's Platform MCP enables Claude, ChatGPT, and Cursor to access account briefs, predictive scores, and intent signals; RGI Agent Builder lets developers build agents on the Fabric (source: https://hginsights.com/product/rgi-platform).
  - **ZoomInfo Operations (CRM data quality + enrichment) ↔ HG RGI Fabric data enrichment via Salesforce/HubSpot bi-directional integration + S3/Snowflake/BigQuery.** HG explicitly markets "Enrich your MDM/CRM with the most comprehensive, current, and granular market, account, spend, tech installs, and buyer datasets" — same job as ZoomInfo Operations (source: https://hginsights.com/).
- **Adjacent overlap:**
  - **ZoomInfo brand-trust/advocacy assets (TrustRadius Buyer's Choice, G2 awards, Forrester Wave) ↔ HG Customer Voice (TrustRadius-powered review syndication and advocacy).** HG sells advocacy/review syndication as a productized SKU; ZoomInfo benefits from TrustRadius reviews but does not sell a productized advocacy module. Notably, ZoomInfo's TrustRadius proof points now sit on a TrustRadius that is owned by HG Insights (source: https://hginsights.com/product/customer-voice).
  - **ZoomInfo GTM Studio (no-code audience building for marketers/RevOps) ↔ HG Data Studio.** Both target the marketer/RevOps audience-builder persona with no-code modeling, but HG's surface is anchored on technographic/spend signals while GTM Studio sits on the GTM Context Graph (source: https://hginsights.com/product/rgi-platform).
- **No overlap:**
  - **Chorus (conversation intelligence) and ZoomInfo Chat (data-powered website chat) have no HG analog.** HG triggers actions into Gong but does not record/transcribe calls or run web chat (source: https://hginsights.com/product/rgi-fabric).
  - **ZoomInfo's 500M-contact / 200M-email / 135M-phone-number contact database is materially deeper than HG's contact layer**, which is positioned as "native contact enrichment, no extra license" inside Sales Copilot rather than a primary product. The vs-page (prospeo.io) explicitly frames HG as "not a replacement for ZoomInfo" on contacts (source: https://prospeo.io/s/hg-insights-vs-zoominfo).
- **Their pitch against ZoomInfo (if found):** "Pick HG Insights if technographics, TAM sizing, whitespace, and market intelligence drive ABM/territory strategy... Pick ZoomInfo if reps need high-volume prospecting, direct dials, enrichment, and workflows in one place. In hg insights vs zoominfo, the split is account strategy vs rep activation: HG is strongest for technographics-led targeting, TAM, and whitespace; ZoomInfo is strongest for contact sourcing, enrichment, and day-to-day outbound workflows." This is a third-party (prospeo.io) framing — HG Insights does not publish a direct competitive page on hginsights.com; the closest first-party resource (https://hginsights.com/resource/hg-insights-and-zoominfo-for-account-intent-and-gtm-intelligence/) was surfaced in SERP but not extracted (source: https://prospeo.io/s/hg-insights-vs-zoominfo).

## Messaging & Positioning Notes

- **Top-line value prop (their words):** AI-powered Revenue Growth Intelligence — "unify market, account, buyer, IT spend, competitor, intent, and customer insights to build precise GTM strategies and achieve efficient execution with AI-assisted workflows" — moving customers "from market analysis to pipeline achievement" (source: https://hginsights.com/).
- **Recurring proof points:** "Trusted by 90% of Fortune 500 Tech Companies"; customer logos and quotes from Hyland Software, HiBob, Equinox, NiCE, Thomson Reuters, NetApp; outcome metrics — 45% increase in sales quota achievement, 30% increase in marketing pipeline, 49% increase in revenue from target accounts, 10x rise in lead-to-opportunity conversions; technographics scale per third-party benchmark (13.2M+ companies, 236 countries, 20K+ products, 90% accuracy); SOC 2 Type II certification; 12M+ annual B2B tech evaluators added via TrustRadius acquisition (sources: https://hginsights.com/, https://hginsights.com/solutions-use-role/sales/, https://hginsights.com/blog/hg-insights-acquires-trustradius/).
- **Tone / category framing:** "Revenue Growth Intelligence" — a category HG positions itself as creating; framed as "the industry's first unified platform built on agentic infrastructure" pairing market intelligence with AI copilots and agents.

## Flags & Limitations

- `pricing_blocked@https://hginsights.com/product/packaging-and-pricing/` — packaging/pricing page is a contact-sales form gated behind cookie consent; no public pricing tiers published.
- `manual_review:vs_brand_first_party_thin` — HG's first-party HG-vs-ZoomInfo resource (https://hginsights.com/resource/hg-insights-and-zoominfo-for-account-intent-and-gtm-intelligence/) was surfaced in SERP but not extracted in this pass; primary vs-pitch evidence used here is from prospeo.io (third-party).
- `manual_review:trustradius_acquisition_context` — HG's June 2025 TrustRadius acquisition reshaped the dossier; HG is now also an indirect competitor to ZoomInfo's TrustRadius-derived advocacy proof points (TrustRadius Buyer's Choice etc. now reside under an HG-owned subsidiary).
- `manual_review:recent_ownership_change` — TrustRadius is an HG Insights subsidiary as of June 2025; relevant for any wiki page that references TrustRadius separately.
- `manual_review:company_snapshot_thin` — Founded date, HQ, and employee size were not surfaced on the reviewed pages; no `/about` or company-overview URL was extracted.

## Sources

| URL | Status | Used For |
|---|---|---|
| https://hginsights.com/ | success | Homepage / value prop / proof points / use case grid |
| https://hginsights.com/product/packaging-and-pricing/ | success | Pricing (gated) / Intent-Driven Leads / Customer Voice descriptions |
| https://hginsights.com/solutions-use-role/sales/ | success | Sales ICP / use cases / customer outcome metrics / sales engagement integrations |
| https://hginsights.com/blog/hg-insights-acquires-trustradius/ | success | Funding/ownership / TrustRadius acquisition context / messaging |
| https://prospeo.io/s/hg-insights-vs-zoominfo | success | vs-ZoomInfo pitch / pricing benchmarks / integration list / decision framing |
| https://hginsights.com/gtm-data-insights/hg-insights-data-fabric/ | success | Data Fabric depth — technographics, firmographics, hierarchies |
| https://hginsights.com/product/rgi-fabric | success | RGI Fabric product page — datasets, integrations, MCP, API endpoints |
| https://hginsights.com/product/rgi-platform | success | RGI Platform product page — copilots, Contact Intelligence, MCP |
| https://hginsights.com/product/customer-voice | success | Customer Voice product page — TrustQuotes, advocacy, review syndication |
