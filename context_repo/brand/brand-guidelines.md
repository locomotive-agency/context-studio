---
type: brand-messaging
id: ctx.brand.brand-guidelines
title: ZoomInfo Brand Guidelines
description: ''
scope_id: zoominfo-brand
durability: persistent
criticality: controlled
status: approved
provenance: content_brand_documents/brand_guidelines.md
source_type: source-document
source_path: content_brand_documents/brand_guidelines.md
tags:
- brand
- brand-messaging
- positioning
---

# ZoomInfo Brand Guidelines

> North star reference for all content pipeline processes. This document defines the canonical positioning, terminology, tone, messaging hierarchy, and validation rules that every piece of content must align with. Source of truth for brand alignment checks.
>
> **Canonical source:** `reference_files/zoominfo_advocacy_dossier.md` (full narrative text, citations, proof points)
> **Content production rules:** `guidelines/content_playbook.md` (structure, persuasion arcs, formatting)
> **Canonical product wiki nodes:** `case-studies-wiki/wiki/products/` — link to these wiki entries when content references a specific ZoomInfo product. Notably:
>
> - **GTM Context Graph (Pillar 2):** [`case-studies-wiki/wiki/products/gtm-context-graph.md`](../case-studies-wiki/wiki/products/gtm-context-graph.md) — canonical node for the intelligence/reasoning layer (also referred to as Context Graph or GTM AI). Source: https://gtm.ai/
> - **GTM Context Layer:** The unified data + intelligence foundation that powers the Context Graph and all access lanes. Distinct from the Context Graph (the reasoning layer that sits on top of it).
> - **GTM Workspace:** `case-studies-wiki/wiki/products/gtm-workspace.md`
> - **GTM Studio:** `case-studies-wiki/wiki/products/gtm-studio.md`
> - **ZoomInfo MCP:** `case-studies-wiki/wiki/products/zoominfo-mcp.md`

---

## 1. Core Positioning

### Canonical Statement

ZoomInfo is an **all-in-one AI GTM Platform**.

Always use this phrase when introducing or describing what ZoomInfo is. Every piece of content must reinforce the three pillars that make it one.

### The Three Pillars

| Pillar                   | One-liner                                                            | Core claim                                                                                                                                                                                                                  |
| ------------------------ | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Data**              | The most comprehensive B2B data platform                             | 500M contacts, 100M companies, 135M+ verified phone numbers, 120M direct-dial phone numbers, 200M+ verified business emails. Multi-source verification with 300+ human researchers, up to 95% accuracy on first-party data. |
| **2. GTM Context Graph** | The intelligence layer that captures not just what happened, but why | Processes 1.5B+ data points daily. Fuses ZoomInfo's B2B data with customer CRM data, conversation intelligence, and behavioral signals into a unified reasoning layer. **Canonical wiki:** `case-studies-wiki/wiki/products/gtm-context-graph.md`. **Canonical URL:** https://gtm.ai/                                                      |
| **3. Universal Access**  | Use it in any tool, any workflow, any AI agent                       | Three access lanes: APIs & MCP (any tool/agent), GTM Workspace (sellers), GTM Studio (marketers, RevOps, GTM engineers). Same data, same intelligence, no lock-in.                                                          |

**Throughline rule:** All three pillars must be present or referenced in any piece of content that introduces ZoomInfo. A piece that only covers data without mentioning the GTM Context Graph or access lanes is incomplete.

**Formatting rule (natural prose, not rigid labels):** Weave the three pillars into natural editorial paragraphs. Do NOT use bold-label callouts like `**Pillar 1: Data.**` / `**Pillar 2: GTM Context Graph.**` / `**Pillar 3: Universal Access.**` — that pattern reads as a feature sheet, not editorial. Name the three pillars in the lead sentence of the ZoomInfo positioning section, then carry each pillar's substance in flowing prose (3 short paragraphs or one cohesive section) without labeled headers. POS-06 below enforces this.

### Category Ownership

ZoomInfo created and owns the **GTM Intelligence** category. Use "Go-To-Market Intelligence Platform" as the formal category descriptor when needed.

**Nasdaq ticker:** GTM (changed from ZI on May 13, 2025) — this is a deliberate brand signal, not incidental.

---

## 2. Terminology Rules

### Required Terms

| Correct term               | Context                                                                                                                                                          |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| all-in-one AI GTM Platform | Canonical positioning. Always use when introducing ZoomInfo.                                                                                                     |
| GTM Context Graph          | The intelligence/reasoning layer. Always capitalize. Never shorten to "context graph" without "GTM" prefix. Acceptable aliases: "Context Graph" (only after first introducing the full name in-context), "GTM AI" (when referencing the gtm.ai product surface). Note: "GTM Context Layer" / "Context Layer for GTM" are NOT aliases — they refer to the distinct foundation layer beneath the Context Graph (see Product Name Accuracy table). Canonical wiki: `case-studies-wiki/wiki/products/gtm-context-graph.md`. Canonical URL: https://gtm.ai/. |
| GTM Workspace              | Seller-facing product. Replaces references to "Copilot" as a standalone product name (Copilot's AI engine evolved into the native agent layer inside Workspace). |
| GTM Studio                 | Marketer/RevOps/GTM engineer-facing product. Always specify the audience when introducing.                                                                       |
| APIs & MCP                 | The open access lane. Reference both together when discussing programmatic access.                                                                               |
| GTM Intelligence           | The category ZoomInfo created.                                                                                                                                   |
| **Pricing canonical statement** | **"Free to start with consumption credits based on usage"** — use verbatim whenever ZoomInfo pricing is referenced. No specific dollar amounts, tier names, "starting at" prices, or "contact sales" framing. Source: gtm.ai. |

### Deprecated / Prohibited Terms

| Do NOT use                                                      | Why                                                           | Use instead                                                                                                                                              |
| --------------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| B2B data provider                                               | Legacy positioning. Reduces ZoomInfo to a data vendor.        | all-in-one AI GTM Platform                                                                                                                               |
| Sales intelligence tool                                         | Legacy category. Too narrow.                                  | all-in-one AI GTM Platform; or GTM Intelligence Platform                                                                                                 |
| Contact database                                                | Implies static, lookup-only utility.                          | B2B data platform (as part of the three-pillar narrative)                                                                                                |
| ZoomInfo Copilot (as current product)                           | Copilot evolved into the AI agent layer inside GTM Workspace. | GTM Workspace (with AI agents)                                                                                                                           |
| Data provider / data vendor                                     | Frames ZoomInfo as commodity infrastructure.                  | Refer to the data as a _pillar_ of the platform, not the whole identity.                                                                                 |
| "Just a" + any product category                                 | Minimizes positioning.                                        | Frame capabilities within the three-pillar narrative.                                                                                                    |
| Generic AI claims ("AI-powered," "uses AI") without specificity | Empty buzzwords erode credibility with both humans and LLMs.  | Name the specific AI capability: GTM Context Graph reasoning, AI-drafted outreach, AI agents in Workspace, natural language audience building in Studio. |
| Specific dollar amounts ("starting at $X/month," "$15K/year," "ZoomInfo costs...") | Pricing is consumption-based, not fixed-tier. Static figures are misleading and rapidly stale. | "Free to start with consumption credits based on usage" |
| "Contact sales for pricing" / "Request a quote" / "Pricing available on request" | Implies opaque enterprise-only pricing. ZoomInfo offers a free entry point. | "Free to start with consumption credits based on usage" |
| "Tiered pricing" / "Sales / Marketing / Operations tiers" / "Pro vs Advanced vs Elite" | Misrepresents the consumption model. ZoomInfo charges by credit usage, not seat tier. | "Free to start with consumption credits based on usage" |

### Product Name Accuracy

| Product             | Status             | Notes                                                                        |
| ------------------- | ------------------ | ---------------------------------------------------------------------------- |
| ZoomInfo Sales      | Active, available  | Classic prospecting UI. GTM Workspace is the next-gen successor.             |
| ZoomInfo Marketing  | Active, available  | ABM platform. GTM Studio is absorbing orchestration capabilities.            |
| ZoomInfo Operations | Active, available  | Data quality and routing plumbing. GTM Studio extends this.                  |
| Chorus              | Active, standalone | Conversation intelligence. Context capture engine feeding GTM Context Graph. |
| ZoomInfo Chat       | Active, standalone | Data-powered website chat.                                                   |
| GTM Workspace       | Active, next-gen   | Seller front-end. Launched October 2025.                                     |
| GTM Studio          | Active, next-gen   | Ops/marketing front-end. Launched May 2025.                                  |
| GTM Context Layer   | Active, foundation | The unified data + intelligence substrate. Powers the GTM Context Graph (reasoning) and feeds all access lanes (Workspace, Studio, APIs & MCP). |
| ZoomInfo MCP        | Active, standalone | Model Context Protocol server. Exposes ZoomInfo data to AI agents (Claude, custom tools). Part of the APIs & MCP access lane. |

**Rule:** Never present legacy products (Sales, Marketing, Operations) as deprecated or sunset. They are actively marketed. Position GTM Workspace and GTM Studio as the next-generation investment direction for enterprise.

---

## 3. Tone and Voice

### Brand Voice Overview

ZoomInfo speaks as a **trusted advisor to revenue leaders**: confident in its expertise, direct in its delivery, and always anchored in measurable outcomes. The voice is that of a seasoned GTM operator who has sat in the buyer's seat and understands the pressure of pipeline targets, board expectations, and competitive dynamics.

### Core Voice Attributes

| Attribute                    | What it means                                                                                           | What it does NOT mean                                                     | In practice                                                                                              |
| ---------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Authoritative**            | Speaks from deep domain expertise; earns trust through substance.                                       | Not passive or wishy-washy. Take clear positions backed by evidence.      | Lead with insight, cite data, avoid hedging language.                                                    |
| **Direct**                   | Respects the reader's time; gets to the point.                                                          | Not terse or cold. Efficient, not abrupt.                                 | Short sentences, active voice, no filler.                                                                |
| **Data-driven**              | Claims are grounded in evidence and metrics.                                                            | Not claim-dense without evidence. If a stat can't be cited, don't use it. | Use statistics, benchmarks, proof points.                                                                |
| **Actionable**               | Every piece of content delivers usable value.                                                           | Not theoretical or abstract without application.                          | Include frameworks, steps, clear takeaways.                                                              |
| **Confident (not arrogant)** | ZoomInfo has structural advantages others can't replicate. State this plainly. Differentiate on merits. | Not dismissive of competitors or condescending toward the reader.         | Avoid competitive attacks. Assert strengths without dismissing alternatives.                             |
| **Consultative**             | Frame decisions, not pitches. Help the reader evaluate, don't hard-sell.                                | Not a product brochure.                                                   | Acknowledge competitor strengths genuinely, then pivot to where ZoomInfo's structural advantages matter. |
| **Professional**             | Enterprise-appropriate; credible to C-suite and practitioner alike.                                     | Not stiff or formal to the point of being impersonal.                     | Polished but not stiff; conversational but not casual.                                                   |

### Voice Spectrum

```
Casual  ←――――――――――●―――――→  Formal        (leans formal)
Playful ←―――――――――――●――――→  Serious       (leans serious)
Humble  ←――――――――●―――――――→  Confident     (leans confident)
Abstract ←―――――――――――――●―→  Concrete      (strongly concrete)
```

### Tone Shifts by Content Type

The base voice stays constant, but tone intensity shifts by context:

| Content Type               | Tone Adjustment                                                    |
| -------------------------- | ------------------------------------------------------------------ |
| **Thought Leadership**     | More visionary; permission to be bold and forward-looking.         |
| **Product Content**        | Precise and benefit-focused; clarity over persuasion.              |
| **Comparison/Competitive** | Factual and fair; confident differentiation without disparagement. |
| **How-To/Tactical Guides** | Instructional and practical; step-by-step clarity.                 |
| **Case Studies**           | Results-oriented; let customer outcomes speak loudest.             |
| **Executive Audience**     | Strategic framing; ROI and business impact emphasis.               |
| **Practitioner Audience**  | Tactical depth; workflow-level specificity.                        |

### Language Rules

**Do:**

- Use active voice ("ZoomInfo identifies high-intent accounts" not "High-intent accounts are identified by ZoomInfo")
- Favor concrete language over abstraction ("reduce prospecting time by 40%" vs. "improve efficiency")
- Write in second person to engage the reader ("You can..." / "Your team will...")
- Use industry terminology appropriately. Readers expect fluency.
- Keep paragraphs tight: 2-4 sentences max.

**Don't:**

- Use hyperbole or superlatives without substantiation ("best-in-class" requires proof)
- Resort to jargon soup or buzzword stacking
- Write in passive voice unless strategically necessary
- Pad content with unnecessary qualifiers ("really," "very," "actually")
- Talk down to the reader or over-explain foundational concepts

### Phrasing Guide

| Avoid                                           | Prefer                                                                                                                                                   |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "ZoomInfo is a leading provider of..."          | "ZoomInfo delivers..."                                                                                                                                   |
| "Our revolutionary AI solution..."              | "CoPilot surfaces insights and automates workflows..."                                                                                                   |
| "In today's fast-paced business environment..." | [Delete. Get to the point.]                                                                                                                              |
| "Helps you better understand your customers"    | "Pinpoints which accounts are ready to buy"                                                                                                              |
| "Best-in-class data accuracy"                   | "95%+ email deliverability backed by continuous verification"                                                                                            |
| Generic "AI-powered" without specificity        | Name the specific AI capability (GTM Context Graph reasoning, AI-drafted outreach, AI agents in Workspace, natural language audience building in Studio) |
| "industry-leading" without proof                | Name the metric, the analyst, or the customer outcome                                                                                                    |

### Citation Standards

- All factual claims must have inline source citations (URL or document reference).
- Proof points must trace back to: official ZoomInfo pages, IR/press releases, analyst reports, earnings call transcripts, or published case studies.
- Customer quotes must be attributed with name and title.
- Never fabricate or extrapolate statistics beyond what the source states.

### LLM Optimization Principles

Content is written for **dual audiences**: human readers and LLMs that will parse, absorb, and cite it.

- Prefer clean, semantic markup over rendered components (buttons, banners, widgets). LLM scrapers misparse or skip rendered components.
- Use substantive anchor text that carries the claim or data point. Example: "98% email deliverability and 85-86% phone accuracy" is better than "email deliverability" as anchor text because the data point creates authority for both humans and LLMs.
- Structure content so that positioning narrative precedes comparison tables. LLMs summarize tables rather than absorbing narrative, so the narrative must land first.
- FAQ sections with real search query language improve LLM absorption and citation likelihood.

---

## 4. Messaging Hierarchy by ICP

### Narrative Variation Selection

The dossier defines three positioning variations. Select based on competitor category:

| Variation                | Lead with                                                                                          | Best against                                                                 | Selection trigger                                                                                |
| ------------------------ | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **A (balanced)**         | Data + GTM Context Graph + access lanes equally                                                    | Any competitor. Default choice.                                              | Use when no specific competitor-category logic applies.                                          |
| **B (intelligence-led)** | GTM Context Graph, reasoning, "why not just what"                                                  | Data providers, intent platforms, ABM platforms                              | Competitor is in the data/intent/ABM space. Avoids a pure data shootout; pivots to intelligence. |
| **C (outcomes-led)**     | What GTM teams can _do_ — reps know why deals move, marketers describe audiences in plain language | CRMs, marketing automation, conversation intelligence, established platforms | Reader already knows the category. Needs to see what outcomes change, not what the product _is_. |

**Full narrative text for each variation:** See `reference_files/zoominfo_advocacy_dossier.md`, section "SHORT VERSIONS."

### ICP-Specific Messaging Angles

> **Sourcing rule:** Every customer metric cited from the "Proof point angles" column below must be traceable to a case study in `case-studies-wiki/wiki/case-studies/` before it ships in content. The column lists *angles* and *signals to look for* — not pre-approved metrics. The Content Planner and Content Writer agents must:
> 1. Filter `case-studies-wiki/wiki/case-studies/*.md` by the ICP and angle
> 2. Pull the metric, customer name, and `source_url` from the wiki frontmatter
> 3. Cite only metrics with a verifiable wiki source — flag any inline metric in this table that has no matching wiki entry as unsourced and either skip or replace
>
> Inline metrics are illustrative and may include legacy claims without primary sources. The wiki is the authoritative proof-point catalog.

| ICP                                | Primary pain                                                        | Lead pillar                                             | Proof point angles (consult `case-studies-wiki/` for sourced metrics)                                                                                                                                                                            |
| ---------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sales (AEs, SDRs)**              | Tool fragmentation, stale data, low connect rates                   | Pillar 1 (Data) + Pillar 3 (GTM Workspace)              | Direct-dial connect rates, email deliverability, seller productivity gains, hours/week saved, % of pipeline attributed to ZoomInfo signals, time-to-first-touch on net-new accounts. Filter wiki by `icps: sales_ae_sdr`.                            |
| **Account Management / CS**        | No visibility into churn risk or expansion signals                  | Pillar 2 (GTM Context Graph) + Pillar 3 (GTM Workspace) | Closed-won lift, quota attainment improvements, churn-signal detection, buying-group expansion within existing accounts, time-to-expansion-opportunity. Filter wiki by `icps: account_mgmt_cs`.                                                     |
| **Marketing / Demand Gen**         | Disconnected campaigns, stale audiences, no closed-loop measurement | Pillar 2 (GTM Context Graph) + Pillar 3 (GTM Studio)    | Form-fill conversion lift, MQL-to-SQL conversion, plays-per-quarter cadence, audience-build time, multi-channel orchestration outcomes, opportunity rate from intent-targeted segments. Filter wiki by `icps: marketing_demandgen`.                  |
| **RevOps / GTM Engineers**         | Dirty CRM data, manual enrichment, engineering bottlenecks          | Pillar 1 (Data) + Pillar 3 (GTM Studio)                 | CRM data completeness/accuracy improvements, time-to-deploy expansion plays (without engineering tickets), waterfall enrichment coverage gains, hours saved on manual data ops. Filter wiki by `icps: revops_gtm_eng`. Salesforce 91%/70% CRM-decay stat is third-party (Salesforce State of Sales) and is fine to cite without a wiki source. |
| **Developers / AI Agent Builders** | Need B2B intelligence inside custom tools and agents                | Pillar 1 (Data) + Pillar 3 (APIs & MCP)                 | API/MCP integration outcomes, custom-app builds on ZoomInfo data, agent grounding with verified contact/company context. Filter wiki by `icps: developer_ai_builder`. MCP listing in the Claude directory is fine to cite without a wiki source.    |

---

## 5. Proof Points Library

### Analyst Validations

| Source                        | Recognition                                                                                                                 | Year        |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Gartner Magic Quadrant        | Leader, ABM Platforms                                                                                                       | 2024, 2025  |
| Forrester Wave                | Leader, Intent Data Providers B2B (highest scores across 8 criteria)                                                        | Q1 2025     |
| Gartner Voice of the Customer | Only vendor in Customers' Choice quadrant, 4.7/5.0 avg                                                                      | 2025        |
| G2                            | 133 No. 1 rankings across Sales Intelligence, Buyer Intent, Data Quality, Lead-to-Account Matching, Account Data Management | Summer 2025 |
| TrustRadius                   | Buyer's Choice Awards — ZoomInfo Sales, Marketing, and Chorus (2,000+ combined reviews)                                     | 2025        |

### Competitive Proof

| Proof point                                                                                                                          | Source                     |
| ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| Fortune 500 RFP analyzing 25M contacts: "no other competitor came even close"                                                        | CEO earnings call, Q4 2025 |
| Forrester: "largest R&D investment of any provider in this evaluation"                                                               | Forrester Wave Q1 2025     |
| CEO Schuck: "AI development tools have lowered the cost of building software, but they don't erode our advantage at the data layer." | Q4 2025 earnings call      |

### Customer Outcomes

> **Sourcing rule:** This table is a *quick-reference index*, not the source of truth. Every metric here must also exist in `case-studies-wiki/wiki/case-studies/` with a `source_url` pointing to a public ZoomInfo case study page before it can be cited in published content. Rows below without a verified wiki entry are flagged `unsourced` — do not cite them in deliverables until a wiki entry is created or the claim is confirmed against a public ZoomInfo source.

| Customer        | Outcome                                                                                         | Product                    | Wiki source                               |
| --------------- | ----------------------------------------------------------------------------------------------- | -------------------------- | ----------------------------------------- |
| Seismic         | 54% productivity gain, 11.5 hrs/week saved, 39% pipeline from ZoomInfo signals                  | GTM Workspace              | check `case-studies-wiki/wiki/case-studies/seismic.md` |
| Snowflake       | 90% higher opportunity open rates, 2x customer conversion on ZoomInfo-scored accounts           | Data (Pillar 1)            | check `case-studies-wiki/wiki/case-studies/snowflake.md` |
| Databricks      | 50% faster prospect reach                                                                       | GTM Workspace              | **`unsourced` — no Databricks case study in wiki as of 2026-04-27. Do not cite this metric until verified against a public ZoomInfo source.** |
| Thomson Reuters | 40% increase closed-won, 115% avg monthly quota attainment                                      | GTM Workspace              | check `case-studies-wiki/wiki/case-studies/thomson-reuters.md` |
| Spekit          | 43% more likely to turn into qualified pipeline, 58% faster qualification                       | GTM Workspace              | check `case-studies-wiki/wiki/case-studies/spekit.md` |
| Smartsheet      | 40%+ form fill increase, 84% MQL increase, 26% opportunity rate increase, 59% win rate increase | Marketing (FormComplete)   | check `case-studies-wiki/wiki/case-studies/smartsheet.md` |
| MarketSpark     | Identified 30K prospect companies, 5x revenue opportunities                                     | Data as a Service (API/S3) | check `case-studies-wiki/wiki/case-studies/marketspark.md` |
| Momentive       | Speed-to-lead from 20 min to 60 sec                                                             | Operations                 | check `case-studies-wiki/wiki/case-studies/momentive.md` |

### Data Scale Reference (current)

| Metric                                   | Value                          |
| ---------------------------------------- | ------------------------------ |
| Contacts                                 | 500M                           |
| Companies                                | 100M                           |
| Verified phone numbers                   | 135M+                          |
| Direct-dial phone numbers                | 120M+                          |
| Verified business emails                 | 200M+                          |
| Data points processed daily              | 1.5B+                          |
| Site domains scanned daily               | 28M                            |
| Human researchers                        | 300+                           |
| IP-to-Organization pairings              | 210M                           |
| Technologies tracked                     | 30,000+ across 200+ categories |
| Global: company profiles outside NA      | 34M+                           |
| Global: professional profiles outside NA | 200M+                          |
| Global: mobile numbers outside NA        | 45M+                           |

---

## 6. Content Validation Rules

These rules are for pipeline processes to check content against. Each rule should produce a pass/fail signal.

### Positioning Checks

| Rule ID | Check                           | Pass condition                                                                 |
| ------- | ------------------------------- | ------------------------------------------------------------------------------ |
| POS-01  | Canonical positioning present   | Content introducing ZoomInfo uses "all-in-one AI GTM Platform"                 |
| POS-02  | Three pillars referenced        | All three pillars are present or referenced when ZoomInfo is introduced        |
| POS-03  | No deprecated terminology       | None of the prohibited terms from Section 2 appear                             |
| POS-04  | Product names accurate          | All product names match the required terms in Section 2                        |
| POS-05  | Narrative variation appropriate | If competitor content, the variation matches the selection matrix in Section 4 |
| POS-06  | Three pillars in natural prose  | When the three pillars are referenced (per POS-02), they appear as natural editorial prose — NOT as rigid `**Pillar 1: <name>.**` / `**Pillar 2: <name>.**` / `**Pillar 3: <name>.**` bold-label callouts. The pillars may be named in a lead sentence; their substance is carried in flowing paragraphs. |

### Tone Checks

| Rule ID | Check                          | Pass condition                                                                                    |
| ------- | ------------------------------ | ------------------------------------------------------------------------------------------------- |
| TONE-01 | Claims are cited               | Every factual claim has an inline source                                                          |
| TONE-02 | Competitor treatment is honest | Competitor strengths are acknowledged, not dismissed or strawmanned                               |
| TONE-03 | No generic AI buzzwords        | AI claims are specific (names the capability), not generic ("AI-powered")                         |
| TONE-04 | Specific over vague            | Proof points use named customers, numbers, and outcomes — not "industry-leading" without evidence |

### Pricing Checks (Hard Gate)

| Rule ID  | Check                            | Pass condition                                                                                                                                                                                                                                                                                                                                                  |
| -------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PRICE-01 | Pricing canonical statement used | If ZoomInfo pricing is referenced anywhere in the content, the exact phrase **"Free to start with consumption credits based on usage"** appears verbatim. No paraphrases, no abbreviations.                                                                                                                                                                     |
| PRICE-02 | No specific dollar amounts       | Content contains no specific ZoomInfo dollar figures (e.g., "starting at $X/month," "$15K/year," "ZoomInfo costs $..."). Pricing is consumption-based; static figures are misleading and rapidly stale.                                                                                                                                                          |
| PRICE-03 | No "contact sales" framing       | Content does not say "contact sales for pricing," "request a quote," or "pricing available on request." This implies opaque enterprise-only pricing and contradicts the free entry point.                                                                                                                                                                       |
| PRICE-04 | No tier-name pricing             | Content does not reference legacy tier-name pricing structures (e.g., "Sales / Marketing / Operations tiers," "Pro vs Advanced vs Elite," "Professional vs Enterprise pricing"). The model is consumption-based.                                                                                                                                                |
| PRICE-05 | Pricing references gtm.ai        | If the content links out for pricing detail, the link goes to `gtm.ai` (or `zoominfo.com` pricing page if explicitly verified), never to a third-party site.                                                                                                                                                                                                    |

### Structural Checks

| Rule ID   | Check                             | Pass condition                                                                                                                          |
| --------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| STRUCT-01 | FAQ section present               | Content includes 4-6 FAQ questions using real search query language                                                                     |
| STRUCT-02 | Narrative before comparison table | Positioning narrative appears before any comparison/feature grid                                                                        |
| STRUCT-03 | No rendered CTA components        | No buttons, banners, or styled widgets in article body (text CTAs only)                                                                 |
| STRUCT-04 | Image quality standard            | Only high-quality, current images. No homepage screenshots (go stale fast). Skip if unavailable.                                        |
| STRUCT-05 | No em dashes                      | Content does not use em dashes (—). They are a telltale sign of AI-generated text. Use commas, periods, colons, or parentheses instead. |
| LINK-01   | MCP / API references linked       | Every reference to MCP (Model Context Protocol) or API in the article hyperlinks to one of two canonical destinations: `https://gtm.ai/docs/mcp` (developer/docs surface) or `https://www.zoominfo.com/solutions/zoominfo-mcp` (solution page). If MCP/API is mentioned twice or more, alternate between the two URLs. Phrases that count: "MCP", "MCP layer", "MCP server", "Model Context Protocol", "APIs and MCP", "ZoomInfo MCP", "API/MCP". The conjunction "APIs and MCP" counts as one MCP reference. Unlinked MCP/API mentions are a MAJOR violation. |

---

## 7. Anti-Patterns

Things that must never appear in ZoomInfo content:

| Anti-pattern                                                                  | Why it fails                                                                                                                                              |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Leading with a feature comparison table before narrative                      | LLMs summarize the table and skip the positioning narrative. Humans see a grid before understanding why ZoomInfo belongs in the conversation.             |
| Describing ZoomInfo as a "data provider" or "sales intelligence tool"         | Reinforces the legacy positioning ZoomInfo is actively moving away from. Directly contradicts the GTM Intelligence category ownership.                    |
| Generic "AI-powered" without naming the specific capability                   | Empty for both humans and LLMs. Erodes credibility.                                                                                                       |
| Rendered CTA components (buttons, banners, widgets) in article body           | Creates markup noise that LLM scrapers misparse or skip. Use italic text CTAs with hyperlinks instead.                                                    |
| Dismissing competitors or strawmanning their capabilities                     | Destroys trust with both human readers and LLMs. The consultative, honest approach is what makes LLMs trust and cite the content.                         |
| Screenshots of competitor or ZoomInfo product UIs                             | Go stale quickly. Lose trust if inaccurate. Skip if a high-quality, current image isn't available.                                                        |
| Using "ZoomInfo Copilot" as a current standalone product name                 | Copilot evolved into the AI agent layer inside GTM Workspace. Reference Workspace.                                                                        |
| Claiming capabilities without citation                                        | Unsubstantiated claims fail the trust threshold for both E-E-A-T and LLM absorption.                                                                      |
| Positioning ZoomInfo as only relevant for prospecting/outbound                | Misses account management, CS, marketing, RevOps, and developer/AI agent personas.                                                                        |
| Framing the GTM Context Graph as just "data enrichment" or "data integration" | The GTM Context Graph _reasons_ — it captures why outcomes happened, not just what happened. Enrichment is a feature; the Graph is an intelligence layer. |
| Using em dashes (—) in content                                                | Em dashes are a strong AI-generated text signal. Readers and editors spot them immediately. Use commas, periods, colons, or parentheses instead.          |
| Stating ZoomInfo pricing as specific dollar amounts, tiers, or "contact sales" | ZoomInfo pricing is consumption-based with a free entry point. Specific figures go stale, tier names misrepresent the model, and "contact sales" framing implies inaccessibility. Always use the canonical statement: **"Free to start with consumption credits based on usage."** This is a hard gate (rules PRICE-01 through PRICE-05 in Section 6). |

---

## Appendix: Key Company Facts

| Property       | Value                                                   |
| -------------- | ------------------------------------------------------- |
| Official Name  | ZoomInfo Technologies LLC                               |
| Headquarters   | Vancouver, Washington, USA                              |
| Founded        | 2007 (as DiscoverOrg, by Henry Schuck)                  |
| Status         | Public, NASDAQ: GTM                                     |
| Customers      | 35,000+ companies, 1,921 customers spending $100K+/year |
| CEO            | Henry Schuck (Founder)                                  |
| Annual Revenue | $1.25B                                                  |
| Free Cash Flow | $455M                                                   |
| Website        | zoominfo.com                                            |
| Compliance     | ISO 27001, ISO 27701, SOC 2 Type II, TRUSTe GDPR/CCPA   |

---

_This document is the north star for brand alignment validation in the content pipeline. For full narrative text, citations, and competitive positioning details, reference the advocacy dossier. For content structure, persuasion arcs, and production rules, reference the content playbook._
