---
brand: Surfe
slug: surfe
primary_url: https://www.surfe.com/
category: b2b-data
secondary_categories:
- sales-engagement
positioning_archetype: point-solution
competes_with_zi_pillars:
- data
- universal_access
competes_with_zi_products:
- Data (Pillar 1)
- ZoomInfo Sales
- GTM Workspace
- ZoomInfo Operations
- APIs & MCP
icp_relevance:
- sales_ae_sdr
- revops_gtm_eng
pricing_model: tiered_public
has_free_tier: true
has_mcp_server: false
has_conversation_intelligence: false
has_abm_advertising: false
has_predictive_scoring: false
analyst_recognition:
- G2 Momentum Leader
- G2 Top 100 Fastest Growing
- G2 Top 100 Rising European Startups
- G2 LeadCapture Leader
- G2 Mid-Market High Performer
research_depth: full
date_researched: 2026-05-08
flags:
- thin_content_market_signals
- manual_review:founding_year_unknown
- manual_review:funding_unknown
sources_count: 10
sub_products:
- surfe--chrome-extension
- surfe--email-finder
- surfe--company-search
- surfe--api
- surfe--market-signals
type: competitive-landscape
id: ctx.competitors.brands.surfe
title: Surfe
description: ''
scope_id: zoominfo
durability: persistent
criticality: hybrid
status: approved
provenance: competitor-wiki/wiki/competitors/surfe.md
source_type: competitor
source_path: competitor-wiki/wiki/competitors/surfe.md
tags:
- competitive-landscape
- competitors
resource: https://www.surfe.com/
---

# Surfe

## Sub-products

- [[surfe--chrome-extension|Surfe Chrome Extension]] — competes with GTM Workspace
- [[surfe--email-finder|Surfe Email Finder / Waterfall Enrichment]] — competes with Data (Pillar 1)
- [[surfe--company-search|Surfe Company Search]] — competes with ZoomInfo Sales
- [[surfe--api|Surfe API]] — competes with APIs & MCP
- [[surfe--market-signals|Surfe Market Signals]] — competes with Intent Data

## Summary

Surfe is a Paris-based, LinkedIn-native B2B prospecting and CRM-enrichment tool sold primarily to SDRs/BDRs, AEs, Sales Ops, and Sales/Team Leads who live inside the LinkedIn timeline and a CRM (Salesforce, HubSpot, Pipedrive, or Copper). Its core surface is a Chrome extension that adds LinkedIn contacts to the CRM in one click, auto-enriches them via a "Waterfall Enrichment" cascade across 15+ underlying data providers (advertised 93% find rate, ZeroBounce-verified emails), and pushes them into Salesloft / Outreach / HubSpot Sequences cadences without leaving LinkedIn. Surfe overlaps directly with ZoomInfo's Pillar 1 Data foundation (verified emails / mobile numbers / contacts and companies) and the GTM Workspace seller-execution surface — and aggressively contests ZoomInfo's data-depth claim with two head-to-head benchmark blog posts (source: https://www.surfe.com/blog/surfe-vs-zoominfo-5k-comparison/) — while explicitly conceding ABM, intent-driven account orchestration, and US-centric GTM scale to ZoomInfo. Pricing is publicly listed seat-based at Free / $49 / $89 per user per month with credits only consumed on successful matches.

## Company Snapshot

| Field | Value |
|---|---|
| Category | LinkedIn-native B2B prospecting and CRM enrichment (Chrome extension + waterfall-enrichment app) |
| Founded / HQ | HQ at 52 rue de la Chaussée d'Antin, 75009 Paris, France; founding year not stated on reviewed pages — see flags |
| Funding / Ownership | _Not available — see flags._ |
| Employee size | Not disclosed on reviewed pages; serves 40,000+ users |
| Primary buyer | Sales Teams, SDRs & BDRs, Sales Ops, C-levels, Team Leads (per role pages linked from homepage and pricing page footer) |

## Product Offerings

### Surfe Chrome Extension (CRM-on-LinkedIn)

> **Wiki:** [[surfe--chrome-extension]]

- **What it does:** Chrome extension that brings the user's CRM into LinkedIn (and other "business socials") so reps can add contacts, enrich data, log activity, and trigger sequences without leaving the social timeline.
- **Key features:**
  - 1-click add of LinkedIn contacts/companies into Salesforce, HubSpot, Pipedrive, or Copper
  - Automatic Waterfall Enrichment of contacts on add (verified email + mobile)
  - Bulk export and enrichment of LinkedIn / Sales Navigator lead lists into the CRM in one click
  - Job change alerts that flag when a contact moves roles or companies and update the CRM record
  - In-extension access to HubSpot Sequences, Salesloft cadences, Outreach cadences, plus Gmail and Aircall for native email/call
  - Set-up advertised at 30 seconds with no credit card required
- **Source URL:** https://www.surfe.com/chrome-extension/

### Email Finder / Waterfall Enrichment

> **Wiki:** [[surfe--email-finder]]

- **What it does:** Multi-source contact-enrichment engine that combines 15+ underlying data providers and ZeroBounce verification to source verified professional emails and mobile numbers.
- **Key features:**
  - Advertised 93% find rate on email and triple-verified data quality
  - Waterfall cascade across 15+ providers — escalates to next provider only if the prior one returns no valid match
  - Credits only deducted on successful matches (not on failed lookups)
  - ZeroBounce validation applied to every email; catchall addresses filtered out
  - Database of 500M B2B contact profiles and 350M company profiles
  - Available via in-app UI, Chrome extension on business socials, CSV upload, or API
- **Source URL:** https://www.surfe.com/email-finder/

### Company Search / Lead List Builder

> **Wiki:** [[surfe--company-search]]

- **What it does:** ICP-finder app for building target-company and target-prospect lists with advanced filters and account look-alikes, with one-click export to CRM.
- **Key features:**
  - 350M+ company profiles, refreshed daily
  - Filters across technographic data, industry, revenue, head-office location, employee count, plus keyword refinement
  - People search by company, job title, seniority, location, and more (Pro plan: 10,000 results/day)
  - Account Lookalikes — input a company or list and surface similar companies (330M+ data points analyzed daily)
  - Automatic CRM-dedup check during list building to avoid duplicates and flag accounts already owned by a teammate
  - Pre-built playbook lists (e.g. "European Pharmaceutical companies with +200 employees", "Heads of IT in Technology Companies")
- **Source URL:** https://www.surfe.com/company-search/

### Surfe API / Enrichment API

> **Wiki:** [[surfe--api]]

- **What it does:** Programmatic enrichment API that lets engineering teams pipe Surfe's waterfall enrichment directly into their own sales/marketing systems.
- **Key features:**
  - Email and mobile enrichment endpoints powered by the same 15+ provider waterfall
  - Webhooks for event-driven workflows
  - n8n integration listed alongside API docs and GitHub examples
  - Documented at developers.surfe.com with public Terms and Conditions for API use
- **Source URL:** https://www.surfe.com/

### Market Signals

> **Wiki:** [[surfe--market-signals]]

- **What it does:** Community-driven marketplace of B2B prospecting lists organized as "playbooks" — users browse curated lists of companies to prospect (e.g. Top Pharmaceutical Companies in Switzerland).
- **Key features:**
  - Community-built ready-to-sell prospecting lists (categories: Most Viewed, Fresh Insights, Tech Installs, Market Expansion)
  - Lists are tagged with intent data, growth trends, and similar attributes
  - Free to browse from the homepage; integrates back into Surfe's prospecting flow
- **Source URL:** https://www.surfe.com/ (dedicated page https://www.surfe.com/market-signals/ failed extraction — see flags)

## Pricing

| Tier | Price | What's included | Source |
|---|---|---|---|
| Free | $0/user/month | 240 email-finder credits/year, 60 mobile-phone-finder credits/year, unlimited email validation; Company & People Search 100 results/week; B2B contact details finder; CRM/GSheets integration; 1-click Add to CRM (limited to 1 contact/day); Salesloft / Outreach / Lemlist integrations; native email & call from social profiles | https://www.surfe.com/pricing/ |
| Essential | $49/user/month ($39 annual) | 1,800 email credits/year, 600 mobile credits/year, unlimited email validation; Company & People Search 100 results/week; B2B contact details finder; full 1-click Add to CRM/GSheets (no daily cap); Salesloft / Outreach / Lemlist integrations; bulk export from Surfe app to CRM | https://www.surfe.com/pricing/ |
| Pro ("Most popular") | $89/user/month ($79 annual) | 12,000 email credits/year, 1,200 mobile credits/year, unlimited email validation; Company & People Search 10,000 results/day; everything in Essential plus Account Lookalikes and Prospect List Builder; 14-day free trial | https://www.surfe.com/pricing/ |

Three publicly-listed seat-based tiers (Free / Essential / Pro) priced per user per month with ~25% annual discount. Credits are deducted only on successful matches. No Enterprise tier on the public pricing page; Surfe's own vs-ZoomInfo blog cites 50-user Essential at $17,400/year and Pro at $31,860/year, with a $15,000 add-on for 600,000 extra emails (source: https://www.surfe.com/blog/surfe-vs-zoominfo/).

## Target Audience & ICP

- **Industries called out:** Industry-agnostic; named customer logos include Google / Google Cloud, AWS / Amazon, Uber, Bolt, Personio, Spendesk, Softbank, Sennder, Pigment, Mirakl, Sastrify, Rokt, PlayPlay, Opendoor, AB Tasty, Partoo
- **Company size called out:** Marketed across SMB, mid-market, and enterprise; pricing tiers tilt toward SMB / mid-market self-serve adoption (G2 badges shown include "Mid-Market High Performer")
- **Persona / role focus:** Sales Teams, SDRs & BDRs, Sales Ops, C-levels, Team Leads (dedicated role landing pages linked from main nav)
- **Use cases promoted:**
  - LinkedIn-native prospecting (add contacts to CRM from LinkedIn profiles in one click)
  - Bulk enrichment of LinkedIn / Sales Navigator lead lists into CRM
  - Email and mobile-number finding via waterfall enrichment
  - ICP / account-lookalike prospect list building
  - Job-change-alert-driven CRM hygiene and re-engagement
  - Cadence enrollment from LinkedIn into Salesloft, Outreach, HubSpot Sequences, Lemlist

## Integrations & Ecosystem

- **CRMs:** HubSpot (native), Salesforce (native; AppExchange listing), Pipedrive (native), Copper (native), Livespace
- **Sales engagement / outreach:** Salesloft (native), Outreach (native), HubSpot Sequences, Lemlist, Aircall (native dialer for in-extension calling), Gmail (native email send)
- **Data / enrichment:** Apollo.io, Cognism, Datagma, Hunter.io, Kaspr, LeadIQ, ZeroBounce (email verification), plus 15+ underlying contact databases combined via Waterfall Enrichment
- **Other notable integrations:** Google Sheets (native), n8n (workflow automation), Webhooks, public REST API + GitHub examples (developers.surfe.com)

## Differentiators (vs the broader category)

- LinkedIn-native CRM sync: 1-click add of LinkedIn contacts/companies into Salesforce/HubSpot/Pipedrive/Copper from inside the social timeline, with auto-enrichment on add (source: https://www.surfe.com/crm-integration/)
- Waterfall Enrichment across 15+ providers in a single subscription, dynamically escalating until a match is returned, with ZeroBounce verification on every email (source: https://www.surfe.com/email-finder/)
- Credits are only consumed on successful matches — failed lookups do not burn credits, an explicit pricing differentiator vs. legacy credit-based vendors (source: https://www.surfe.com/pricing/)
- Advertised 93% email find rate and triple-verified data quality, with publicly published industry/geographic find-rate dashboards (source: https://www.surfe.com/email-finder/)
- Job Change Alerts as a dedicated workflow — notifies reps and updates CRM contact records automatically when a prospect moves company or role (source: https://www.surfe.com/chrome-extension/)
- Public, transparent seat-based pricing with self-serve Free / Essential / Pro tiers and 14-day Pro trial — no enterprise gating to access core features (source: https://www.surfe.com/pricing/)

## Crossover With ZoomInfo

- **Direct overlap:**
  - **Data (Pillar 1)** (verified emails / mobile numbers / contact + company records) overlaps directly with Surfe **Email Finder + Waterfall Enrichment** (15+ providers, 500M contacts, 350M companies). Surfe contests ZoomInfo's data-depth pillar with a benchmark claim of 87–89% email find rate and 90% accuracy vs. ZoomInfo's 65% US / 35% global (source: https://www.surfe.com/blog/surfe-vs-zoominfo/) and an updated 5,000-contact test claiming 89.42% Surfe vs. 52.32% ZoomInfo on email (source: https://www.surfe.com/blog/surfe-vs-zoominfo-5k-comparison/).
  - **ZoomInfo Sales / GTM Workspace** (seller front-end for prospecting and outreach) overlaps with **Surfe Chrome Extension + Company Search + cadence integrations** (Salesloft, Outreach, HubSpot Sequences). Surfe positions itself as the day-to-day prospecting surface that "keeps reps moving inside the tools they already use" (source: https://www.surfe.com/company-search/).
  - **APIs & MCP** (Data API, Enrichment API) overlap with **Surfe Enrichment API + Webhooks + n8n** at developers.surfe.com — same data-pipe-to-customer-system use case (source: https://www.surfe.com/).
- **Adjacent overlap:**
  - **ZoomInfo Operations** (CRM data quality, routing) is touched but not replaced by Surfe's **Job Change Alerts + automatic CRM contact updates** — a single-feature crossover, not a full data-quality / routing platform (source: https://www.surfe.com/chrome-extension/).
  - **Intent Data** (Scoops, intent signals) is partly mirrored by **Surfe Market Signals + filters for funding stage / tech stack / headcount growth + Lookalikes / Sales Recommendations**, but Surfe explicitly concedes ZoomInfo's intent suite is "more geared toward operations teams running programmatic ABM" (source: https://www.surfe.com/blog/surfe-vs-zoominfo/).
- **No overlap:**
  - Conversation intelligence (Chorus) — no call-recording / deal-coaching surface on Surfe.
  - ABM platform / programmatic ad orchestration (ZoomInfo Marketing / GTM Studio) — Surfe does not market an ABM product and concedes ZoomInfo "may be a better fit" for that buyer (source: https://www.surfe.com/blog/surfe-vs-zoominfo/).
  - Website chat (ZoomInfo Chat) — no chatbot surface on Surfe.
  - Native LinkedIn-as-prospecting-surface — flipped: Surfe sells this as its primary GTM and explicitly claims "ZoomInfo does not currently support direct LinkedIn-to-CRM syncing" (source: https://www.surfe.com/blog/surfe-vs-zoominfo/).
- **Their pitch against ZoomInfo (if found):** "Surfe verified 89.42% of emails versus ZoomInfo's 52.32%: a 37-point gap equating to roughly 370 more verified contacts per 1,000 prospects … ZoomInfo does not currently support direct LinkedIn-to-CRM syncing … Surfe is the only ZoomInfo alternative that delivers across the board: 93%+ verified accuracy, strong global data, workflow-native prospecting." Surfe also frames ZoomInfo as a "legacy giant" with US-centric strength and weaker EMEA/APAC/LATAM coverage, while positioning itself as global-balanced and LinkedIn-workflow-native (source: https://www.surfe.com/blog/surfe-vs-zoominfo-5k-comparison/).

## Messaging & Positioning Notes

- **Top-line value prop (their words):** "High-quality data that powers high-converting pipeline" — capture, sync, and enrich contacts from LinkedIn (and other business socials) into your CRM in one click, powered by 15+ provider Waterfall Enrichment (source: https://www.surfe.com/).
- **Recurring proof points:** 40,000+ users; 1M+ enrichments per month; logos including Google, AWS/Amazon, Uber, Bolt, Personio, Spendesk, Softbank, Sennder, Pigment; Bolt "3X more outbound leads", Partoo "142% increase in demos", AWS "90% find rate", Google "80% of new contacts sourced via Surfe"; ISO27001 certified, GDPR compliant, SOC 2 Type II (cited in vs-ZoomInfo blog); G2 Momentum Leader, Top 100 Fastest Growing, Top 100 Rising European Startups, G2 LeadCapture Leader / Mid-Market High Performer.
- **Tone / category framing:** Surfe deliberately rejects "data provider" / "sales intelligence" framing and instead positions itself as a "connected revenue workspace" / "purpose-built sales platform" that brings the CRM to where selling happens (LinkedIn). The vs-ZoomInfo article contrasts the two head-on: "ZoomInfo brings scale and breadth … Surfe is built for salespeople in the trenches."

## Flags & Limitations

- `thin_content@https://www.surfe.com/market-signals/` — Jina extraction failed (HTTPS read timeout, 30s); fallback returned only 140 words. Market Signals product features inferred from homepage and SERP snippets only.
- `manual_review:founding_year_unknown` — founders Romain Ginestou and David Maurice Chevalier and a 2020 founding date appear in a third-party SERP snippet (startupintros.com) but are not stated on any extracted Surfe-owned page, so excluded from the snapshot per the no-fabrication rule.
- `manual_review:funding_unknown` — no funding amount or investor list disclosed on any reviewed Surfe page; not included in snapshot.

## Sources

| URL | Status | Used For |
|---|---|---|
| https://www.surfe.com/ | success | homepage, products (Surfe API, Market Signals), messaging, integrations |
| https://www.surfe.com/pricing/ | success | pricing tiers, ICP signal (self-serve seat-based) |
| https://www.surfe.com/crm-integration/ | success | products (Chrome Extension overlap), differentiators (LinkedIn-native CRM sync) |
| https://www.surfe.com/blog/surfe-vs-zoominfo/ | success | crossover_with_brand, vs_brand_pitch (find rates, integrations comparison, pricing comparison) |
| https://www.surfe.com/market-signals/ | error | products (Market Signals) — extraction failed; see flags |
| https://www.surfe.com/blog/surfe-vs-zoominfo-5k-comparison/ | success | crossover_with_brand, vs_brand_pitch (5K methodology, regional/segment/role breakdowns) |
| https://www.surfe.com/email-finder/ | success | products (Waterfall Enrichment), differentiators (93% find rate, 15+ providers) |
| https://www.surfe.com/company-search/ | success | products (Lead List Builder, Account Lookalikes), ICP playbooks |
| https://www.surfe.com/chrome-extension/ | success | products (Chrome Extension feature set, Job Change Alerts) |
| https://www.surfe.com/integrations/ | success | integrations ecosystem (CRMs, sales engagement, enrichment partners) |
