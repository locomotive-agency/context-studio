---
brand: Salesforge
slug: salesforge
primary_url: https://www.salesforge.ai/
category: sales-ai-agents
positioning_archetype: ai-agent
competes_with_zi_pillars:
- data
- universal_access
competes_with_zi_products:
- GTM Workspace
icp_relevance:
- founder_solo
- sales_ae_sdr
- revops_gtm_eng
pricing_model: tiered_public
has_free_tier: false
has_mcp_server: true
has_conversation_intelligence: false
has_abm_advertising: false
has_predictive_scoring: false
analyst_recognition: []
research_depth: partial
date_researched: 2026-05-07
flags:
- vs_brand_missing
- manual_review:company_snapshot_thin
- manual_review:agent_frank_purchase_gated
sources_count: 10
sub_products:
- salesforge--cold-outreach
- salesforge--infrastructure
type: competitive-landscape
id: ctx.competitors.brands.salesforge
title: Salesforge
description: ''
scope_id: zoominfo
durability: persistent
criticality: hybrid
status: approved
provenance: competitor-wiki/wiki/competitors/salesforge.md
source_type: competitor
source_path: competitor-wiki/wiki/competitors/salesforge.md
tags:
- competitive-landscape
- competitors
resource: https://www.salesforge.ai/
---

# Salesforge

## Sub-products

- [[salesforge--cold-outreach|Salesforge Cold Outreach]] — competes with GTM Workspace
- [[salesforge--infrastructure|Salesforge Infrastructure]] — competes with GTM Workspace

## Summary

Salesforge is an AI-SDR / cold-outreach execution platform sold horizontally to founders, sales teams, growth/GTM engineers, and lead-gen agencies — it bundles multi-channel email + LinkedIn sequencing, an autonomous AI SDR (Agent Frank), and a vertically-integrated infrastructure stack (Mailforge, Warmforge, Leadsforge, Infraforge/Primeforge/Megaforge) under one login. Direct overlap with ZoomInfo runs through GTM Workspace (Agent Frank vs ZoomInfo's AI-drafted seller surface), the Data foundation (Leadsforge's 500M+ contact engine), and APIs/MCP (Salesforge ships an MCP server for Claude). Salesforge has no equivalent to the GTM Context Graph, Chorus, ZoomInfo Operations, or ABM/intent reasoning, and explicitly markets away from Fortune 500 / six-figure-deal buyers — the third-party prospeo.io comparison frames it as "a scooter vs a semi truck." Salesforge sells in spaces ZoomInfo does not (email infrastructure provisioning and warm-up).

## Company Snapshot

| Field | Value |
|---|---|
| Category | AI SDR / multi-channel cold outreach platform (email + LinkedIn execution) |
| Founded / HQ | _Not available — see flags._ |
| Funding / Ownership | _Not available — see flags._ CEO is Frank Sondors (per SERP People-Also-Ask citation pulled from www.salesforge.ai/author/frank-bacon). |
| Employee size | _Not available — see flags._ Homepage states "Trusted by 10,000+ Businesses." |
| Primary buyer | Founders, sales leaders, growth/GTM engineers, and lead-gen agencies. Agent Frank page calls out "decision-makers at startups, SMBs, or mid-market companies" as the buying ICP (source: https://www.salesforge.ai/agent/frank). |

## Product Offerings

### Salesforge (multi-channel outreach platform)

- **What it does:** The "sales execution" command center — runs combined email + LinkedIn cold-outreach sequences, with unlimited mailboxes, unlimited LinkedIn senders, an AI personalization layer, and Primebox for unified reply management.
- **Key features:**
  - Unlimited mailboxes and unlimited LinkedIn senders (no seat-based pricing)
  - Conditional multi-channel sequences (email + LinkedIn in one workflow)
  - Primebox unified inbox — consolidates email + LinkedIn replies with sentiment analysis
  - AI-generated personalization per lead (Personalization Credits)
  - Smart mailbox rotation, dynamic IPs, ESP matching
  - Unlimited Premium Warm Up via Warmforge included on every plan
  - Multi-language sequences in 20+ languages (Growth plan)
  - Salesforge API and MCP server (connects to Claude / AI assistants)
- **Source URL:** https://www.salesforge.ai/, https://www.salesforge.ai/pricing

### Agent Frank (AI SDR)

- **What it does:** An autonomous AI sales-development agent that runs end-to-end outbound — finds prospects, enriches/verifies data, writes personalized email + LinkedIn outreach, follows up, and books meetings, with Auto-Pilot or Co-Pilot supervision modes.
- **Key features:**
  - Auto-Pilot (no supervision) and Co-Pilot (review-before-send) modes
  - 24/7 automated prospecting against a 500M+ contacts search engine
  - Three configurable goals: click-out, send meeting link, receive meeting link
  - 9 tonalities and 20+ languages, with a configurable Knowledge Base trained on the customer's product
  - Personalization sources include prospect website, blog posts, and LinkedIn posts
  - Pulls infrastructure from Mailforge / Infraforge / Megaforge and warm-up from Warmforge — no external dependencies
  - Dedicated Account Manager and shared Slack channel during onboarding
  - Demo-gated purchase ("Agent Frank is only available after a demo")
- **Source URL:** https://www.salesforge.ai/agent/frank

### Mailforge

- **What it does:** Distributed/shared cold-email infrastructure — bulk-creates domains and mailboxes with automated DKIM/DMARC/SPF setup. Sister product on mailforge.ai.
- **Key features:**
  - Bulk domain + mailbox provisioning (hundreds/thousands)
  - Automated DNS / auth-record setup
  - Shared infrastructure tier — cheaper, suited to teams scaling fast
  - Native integration with Salesforge for direct sending
  - Pricing starts at "$3 or less" per mailbox per SERP snippet (source: https://www.mailforge.ai/)
- **Source URL:** https://www.salesforge.ai/stack, https://www.salesforge.ai/integrations/mailforge

### Warmforge

- **What it does:** Email-deliverability / warm-up engine — runs warm-up using a private pool of healthy Google Workspace and Microsoft 365 mailboxes (no external SMTPs), monitors domain/inbox health, and runs inbox-placement tests.
- **Key features:**
  - Premium internal warm-up pool (excludes external SMTP vendors)
  - Inbox-placement testing and reputation scoring
  - Domain and mailbox health monitoring with alerts
  - Included free and unlimited on every Salesforge plan
  - Sister product on warmforge.ai with its own standalone marketing
- **Source URL:** https://www.salesforge.ai/stack, https://www.salesforge.ai/integrations/warmforge

### Leadsforge

- **What it does:** Chat-based AI lead-search engine — users describe their ICP in natural language and the engine builds enriched lead lists from a 500M+ contacts dataset, with waterfall enrichment and lookalike / competitor-follower extraction.
- **Key features:**
  - Natural-language chat interface for list-building
  - 500M+ contacts; waterfall enrichment across multiple data sources
  - Lookalike audiences and competitor-follower extraction
  - Intent-signal qualification before outreach
  - Direct push into Salesforge sequences or CSV export
  - Pre-launch / early-access stage per the prospeo.io vs page; 100 free credits on signup
- **Source URL:** https://www.salesforge.ai/stack, https://prospeo.io/s/leadsforge-vs-zoominfo

### Infraforge / Primeforge / Megaforge (infrastructure tiers)

- **What it does:** Three infrastructure options sold within The Forge Stack — Primeforge (Google Workspace + MS365 with US IPs), Infraforge (private dedicated infrastructure with multi-IP, SSL, domain masking), and Megaforge (Agent Frank-specific premium multi-ESP infrastructure).
- **Key features:**
  - Primeforge — Google Workspace & MS365 mailboxes for ESP matching
  - Infraforge — private infrastructure with multi-IP provisioning, pre-warmed mailboxes, SSL, domain masking; from $33/mo for 10 mailboxes (annual)
  - Megaforge — premium multi-ESP infrastructure built specifically for Agent Frank; auto-distributes sending across Gmail/Outlook/Mailforge/Infraforge; from $69/mo for 20 mailboxes
  - Whitelabel reseller programs for Salesforge and Infraforge
- **Source URL:** https://www.salesforge.ai/agent/frank, https://www.salesforge.ai/stack

### Primebox

- **What it does:** Unified reply manager — consolidates all email and LinkedIn replies (across all connected mailboxes/accounts) into one view with AI sentiment analysis and AI-drafted replies.
- **Key features:**
  - Multi-channel reply consolidation (email + LinkedIn)
  - Sentiment analysis tagging on every thread
  - AI-drafted replies (Primebox AI on Growth plan)
  - Captures replies even when prospect responds from a different address
  - Mobile apps on iOS and Android
  - Included free with every Salesforge subscription
- **Source URL:** https://www.salesforge.ai/, https://www.salesforge.ai/pricing

## Pricing

| Tier | Price | What's included | Source |
|---|---|---|---|
| Pro Plan (Salesforge — Human Path) | $40/mo billed annually (entry) | 1,000 active contacts, 5,000 emails/mo, 100 validation credits, 100 personalization credits, 100 social action credits, 1 LinkedIn sender, unlimited mailboxes, unlimited Warmup, 1 user, Primebox, sentiment analysis, smart mailbox rotation, dynamic IPs | https://www.salesforge.ai/pricing |
| Growth Plan (Salesforge — Human Path) | $80/mo billed annually (annual = 2 months free vs monthly) | 10,000 active contacts, 50,000 emails/mo, 1,000 validation credits, 1,000 personalization credits, 300 social action credits, unlimited LinkedIn senders, unlimited users, multi-language sequences, A/B testing, personal onboarding, advanced settings, priority support, Salesforge API, Primebox AI, ESP matching, full integrations. Add-on credit packs (e.g. 200K active contacts $96/mo, 200K personalization credits $130/mo). | https://www.salesforge.ai/pricing |
| Agent Frank (AI Path) | $499/mo billed quarterly OR ~$416/mo billed annually; 2,000+ contacts/mo = $0.25 per contact | Up to 1,000 active contacts (entry), 24/7 automated prospecting, Auto-Pilot & Co-Pilot, fully customizable agent, 500M+ contacts search engine, 20+ languages, dedicated account manager, shared Slack. Email infra (Mailforge / Infraforge / Megaforge) is an add-on. **Purchase gated behind a mandatory demo.** | https://www.salesforge.ai/pricing, https://www.salesforge.ai/agent/frank |
| Forge Expert Double Session (consulting add-on) | $500 for two 1:1 sessions | Two 1:1 outreach-strategy consulting sessions with a Salesforge expert | https://www.salesforge.ai/pricing |
| Infrastructure add-ons | Infraforge from $33/mo (10 mailboxes, annual); Megaforge from $69/mo (20 mailboxes); Mailforge "starting at $3 or less" per mailbox | Email infrastructure tiers — billed separately ("You need to have a separate subscription for each product.") | https://www.salesforge.ai/agent/frank, https://www.mailforge.ai/ |

Pricing is fully public — no gating on Salesforge plans or Agent Frank pricing. Pricing model is hybrid: flat seat-less subscription PLUS usage-based credit packs (active contacts, emails, personalization, validation, social actions); explicitly contrasted with seat-based pricing on the homepage ("Forget about seat-based pricing").

## Target Audience & ICP

- **Industries called out:** No vertical industry calls — Salesforge positions horizontally across any B2B outbound use case. Customer logos visible on homepage: AKOOL (creative AI), ChannelCrawler (YouTube data), UniteSync (music royalty audit), VidLab7, Net New Solutions, Lean Sales Systems, BetterContact, LinkedDNA, Vacord Screen Printing — primarily SMB / lead-gen agency / niche-data SaaS (source: https://www.salesforge.ai/).
- **Company size called out:** Solopreneurs (Pro plan), SMB, mid-market, agencies / outbound service firms, founders running their own outbound.
- **Persona / role focus:** Sales teams (AEs, SDRs replacing manual outbound), founders/solopreneurs, growth teams and GTM engineers, lead-gen agencies, Forge Expert partner agencies.
- **Use cases promoted:**
  - Multi-channel cold outbound (email + LinkedIn) at scale without seat-based cost
  - Replacing/augmenting human SDR teams with an AI SDR (Agent Frank)
  - Managing email infrastructure (domains, mailboxes, deliverability) end-to-end in one stack
  - Agency client outreach — running multiple ICP campaigns across separate workspaces
  - Whitelabel reselling cold-email infrastructure (Salesforge Whitelabel, Infraforge Whitelabel)

## Integrations & Ecosystem

- **CRMs:** Salesforce, HubSpot, Pipedrive, Attio, folk, Breakcold, GoHighLevel (source: https://www.salesforge.ai/integrations).
- **Sales engagement / outreach:** Sendspark (video), RB2B (visitor identification), Weezly (AI video).
- **Data / enrichment:** Clay, Bitscale, Persana AI, Databar.ai, Leadsforge (own product), OutboundSync.
- **Other notable integrations:** Email infrastructure — Mailforge, Primeforge, Infraforge, Microsoft 365, Google Workspace, custom SMTP. Deliverability — Warmforge (own product, included). Communication — Slack. Automation — Make, Zapier, Webhooks. AI assistants — Salesforge MCP server (connects to Claude and other assistants). API — Salesforge API (Growth plan) and Infraforge API. Salesforge claims integrations with "1000+ different apps and products."

## Differentiators (vs the broader category)

- Unlimited mailboxes and unlimited LinkedIn senders included on the Growth plan — explicitly anti-seat-pricing: "We're the only platform to offer unlimited mailboxes & LinkedIn senders" (source: https://www.salesforge.ai/).
- Vertically integrated outbound stack ("The Forge Stack") covering infrastructure, warmup, data, execution, and AI SDR under one login. Positioned as "Apple-like" vs the "Android-like" patchwork of point tools (source: https://www.salesforge.ai/stack).
- Premium Warmforge warm-up pool excludes external SMTP vendors and uses only healthy Google Workspace + MS365 mailboxes — pitched as a deliverability-quality differentiator (source: https://www.salesforge.ai/).
- Agent Frank sold as a fully autonomous AI SDR with dedicated account manager and shared Slack channel; pricing ($499/mo quarterly or ~$416/mo annual) positioned as cheaper than a human SDR (source: https://www.salesforge.ai/agent/frank).
- Multi-language sequences in 20+ languages out of the box on the Growth plan and Agent Frank (source: https://www.salesforge.ai/pricing, https://www.salesforge.ai/agent/frank).
- MCP server lets buyers operate Salesforge from Claude or other AI assistants — create contacts, launch sequences, manage outreach from chat (source: https://www.salesforge.ai/integrations).

## Crossover With ZoomInfo

This is the load-bearing section. Compare the competitor against the brand's positioning in `CONTEXT.md`.

- **Direct overlap:**
  - **GTM Workspace** ↔ Salesforge platform + Agent Frank. Salesforge bundles prospecting, AI personalization, multi-channel sequencing, reply management (Primebox), and meeting booking into one seller surface — the same workflow GTM Workspace packages. Agent Frank's autonomous prospect-to-meeting loop maps directly to ZoomInfo's AI-drafted outreach inside GTM Workspace (source: https://www.salesforge.ai/agent/frank).
  - **Data foundation (500M contacts, 200M+ emails, 135M+ verified phones)** ↔ Leadsforge. Leadsforge claims a 500M+ contacts search engine with waterfall enrichment — the same B2B contact-data lane the Data foundation occupies. The prospeo.io vs page explicitly frames it as "LeadsForge vs ZoomInfo" while concluding LeadsForge wins on price/UX and ZoomInfo wins on data depth and intent (source: https://prospeo.io/s/leadsforge-vs-zoominfo).
  - **APIs & MCP** ↔ Salesforge MCP server + Salesforge API. Salesforge ships an MCP server that lets Claude and other AI assistants drive contacts and sequences — direct overlap with mcp.zoominfo.com/mcp (source: https://www.salesforge.ai/integrations).
- **Adjacent overlap:**
  - **GTM Studio** ↔ Leadsforge chat interface. Leadsforge's natural-language ICP chat is conceptually adjacent to GTM Studio's natural-language audience builder — but Leadsforge sits at the prospecting layer for outbound execution, not at the campaign-orchestration layer GTM Studio occupies (source: https://www.salesforge.ai/stack, https://prospeo.io/s/leadsforge-vs-zoominfo).
  - **ZoomInfo Marketing (ABM, audience orchestration)** ↔ Salesforge solutions/growth (Growth team + GTM Engineer playbook). Salesforge markets to growth teams and GTM engineers ("infrastructure, automation, and control to build, test, and scale LinkedIn + email outreach systems"). This touches ZoomInfo Marketing's audience and demand-gen workflows from the execution side, but Salesforge does not run paid ABM display, intent-driven website targeting, or audience activation across ad platforms (source: https://www.salesforge.ai/solutions/growth).
- **No overlap:**
  - **GTM Context Graph** — Salesforge has no equivalent first-party CRM/conversation/behavior fusion layer, no Chorus/Workbounce-equivalent, and no Bombora-grade intent integration. Reviewed pages mention "intent signals" only at the lead-list level (Leadsforge); the prospeo.io vs page calls out "Intent data: Basic signals" for LeadsForge vs "Bombora + GTM workflows" for ZoomInfo (source: https://prospeo.io/s/leadsforge-vs-zoominfo).
  - **ZoomInfo Operations** — no CRM data hygiene, lead-to-account matching, or revenue routing in any reviewed product page (source: https://www.salesforge.ai/stack).
  - **Chorus** — no conversation-intelligence / call-recording / coaching surface in the Forge Stack (source: https://www.salesforge.ai/stack).
  - **ZoomInfo Chat** — no website-chat or visitor-identification surface beyond a third-party RB2B integration (source: https://www.salesforge.ai/integrations).
  - **Salesforge sells in spaces ZoomInfo does not** — email infrastructure provisioning (Mailforge/Infraforge/Primeforge) and warm-up (Warmforge). ZoomInfo does not sell domain provisioning, mailbox creation, DKIM/DMARC/SPF setup, or warmup pools (source: https://www.salesforge.ai/stack).
- **Their pitch against ZoomInfo (if found):** No Salesforge-authored vs/ZoomInfo page surfaced in SERP. The third-party prospeo.io comparison frames LeadsForge (the Salesforge data product) as "a scooter vs a semi truck": "LeadsForge wins on accessibility, price, and UX simplicity. ZoomInfo wins on data depth, intent signals, integrations, and workflow breadth." It also notes mutual customers can use both — LeadsForge is on the ZoomInfo App Marketplace and can enrich GTM Studio Audiences via a LeadsForge license, with API/MCP partnership letting LeadsForge pull ZoomInfo intelligence into its own interface (source: https://prospeo.io/s/leadsforge-vs-zoominfo). Flag: `vs_brand_missing`.

## Messaging & Positioning Notes

- **Top-line value prop (their words):** "Forge Pipeline With Unlimited LinkedIn, Email & AI SDR Outreach" — launch outreach with unlimited mailboxes & LinkedIn senders, or let Agent Frank (AI SDR) handle it. The category framing is "all-in-one cold outreach platform that combines AI, human workflows, and world-class infrastructure" (source: https://www.salesforge.ai/).
- **Recurring proof points:** "Trusted by 10,000+ Businesses" (homepage); 4.6 G2 rating (homepage), 4.9 cited on Agent Frank page; AKOOL — 214K+ prospects with 16%+ positive reply rate; ChannelCrawler — 85.71% positive reply rate (with Salesforge + Infraforge + Warmforge); UniteSync — 85.26% positive reply rate, $2.86 CAC; VAI Consulting — Agent Frank booked 3 calls in a week.
- **Tone / category framing:** Positions itself as a unified outbound stack ("Apple-like vs Android-like"), explicitly category-rejecting fragmented tooling. Uses "cold outreach platform" / "AI SDR" / "sales execution" as primary category descriptors — does NOT call itself a sales-intelligence or GTM platform. Explicitly de-targets enterprise: Agent Frank's "Not-so-good fit" list calls out "You primarily target Fortune 500 companies" and "Your average deal size is consistently in the six to seven-figure range."

## Flags & Limitations

- `vs_brand_missing` — no Salesforge-authored vs-ZoomInfo page surfaced in SERP. The prospeo.io "LeadsForge vs ZoomInfo" page is third-party and only covers the data-product subset of the Forge Stack.
- `manual_review:company_snapshot_thin` — founded date, HQ, headcount, and funding/ownership are not surfaced on any extracted page; CEO name (Frank Sondors) confirmed via SERP People-Also-Ask citation, not via an extracted page.
- `manual_review:agent_frank_purchase_gated` — Agent Frank pricing is publicly listed but purchase requires a sales demo (not self-serve checkout).

## Sources

| URL | Status | Used For |
|---|---|---|
| https://www.salesforge.ai/ | success | Homepage / positioning / proof points / unlimited senders claim |
| https://www.salesforge.ai/pricing | success | Pricing tiers (Pro, Growth, Agent Frank, add-ons) |
| https://www.salesforge.ai/agent/frank | success | Agent Frank product depth + ICP fit/not-fit lists + infra add-ons |
| https://www.salesforge.ai/stack | success | The Forge Stack — full product ecosystem (5 layers) |
| https://www.salesforge.ai/solutions/sales | success | Sales-team ICP and use-case framing |
| https://www.salesforge.ai/solutions/agencies | success | Agency ICP — negative-space crossover with ZoomInfo |
| https://www.salesforge.ai/solutions/growth | success | Growth/GTM-engineer ICP framing |
| https://www.salesforge.ai/integrations | success | CRM / sales engagement / data / MCP / API integrations |
| https://www.salesforge.ai/case-study/vai-consulting | success | Proof point — VAI Consulting / Agent Frank case |
| https://prospeo.io/s/leadsforge-vs-zoominfo | success | Vs-brand framing (third-party) — LeadsForge vs ZoomInfo |
