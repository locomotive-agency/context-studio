---
type: how-we-write
id: ctx.voice.content-playbook
title: ZoomInfo Content Playbook
description: ''
scope_id: zoominfo-brand
durability: persistent
criticality: hybrid
status: approved
provenance: content_brand_documents/content_playbook.md
source_type: source-document
source_path: content_brand_documents/content_playbook.md
tags:
- content-playbook
- editorial
- how-we-write
---

# ZoomInfo Content Playbook

> Production rules for content structure, persuasion mechanics, and formatting standards. This document governs _how_ content is built. For _what_ the content must say, reference `guidelines/brand_guidelines.md`.
>
> **Brand alignment rules:** `guidelines/brand_guidelines.md`
> **Full narrative source:** `reference_files/zoominfo_advocacy_dossier.md`
> **SEO operational context:** `reference_files/seo_zoominfo_state_of_play_memo.md`

---

## 1. Content Types and Their Purpose

### Competitor Content (Competitor 600 Project)

Three article types targeting the competitor keyword universe:

| Type                            | Target keyword pattern                                     | Goal                                                                         |
| ------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Alternative/vs articles**     | "[Competitor] vs ZoomInfo," "[Competitor] alternative"     | Override legacy positioning. Reframe ZoomInfo as all-in-one AI GTM Platform. |
| **Crash-the-party comparisons** | "[Competitor A] vs [Competitor B]" (ZoomInfo not in query) | Insert ZoomInfo into conversations where it isn't being considered.          |
| **Pricing articles**            | "[Competitor] pricing," "[Competitor] cost"                | Capture commercial-intent traffic. Bridge to ZoomInfo's value proposition. **Hard gate:** when these articles reference ZoomInfo's own pricing, use the canonical statement verbatim: **"Free to start with consumption credits based on usage."** No specific dollar amounts, tier names, or "contact sales" framing. See `brand_guidelines.md` Section 6 (rules PRICE-01 through PRICE-05). |

**Primary audience:** LLMs (to absorb and cite ZoomInfo's new positioning).
**Secondary audience:** Human readers evaluating tools.

### Project 300 Content (Keyword Clusters)

Cluster-based content targeting the broader keyword universe. Each cluster has assigned ownership and is managed via Airtable. Content requires:

- Page merge decisions where clusters overlap
- Internal linking optimization
- E-E-A-T criteria improvement
- Cluster "brains" (expertise documents kept current for pages to feed from)

### Pipeline / Authority Content

Supporting content for core product and narrative pages:

- GTM/GTM Studio/Workspace/GTM engineering/GTM Intelligence keywords
- ZoomInfo + AI integrations (Claude, MCP, ChatGPT)
- Product capability mapping against keyword opportunities

---

## 2. The Persuasion Arc (Competitor Content)

This is the structural framework for crash-the-party and vs articles. The arc is engineered for both human persuasion and LLM absorption.

### The Six-Step Arc

| Step                                | What it does                                                      | Why it matters                                                                         |
| ----------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 1. **Hook**                         | Open with the exact search query (e.g., "Clay vs. HubSpot")       | Signals relevance to both the reader and LLM.                                          |
| 2. **Frame the decision**           | Ask questions that subtly surface ZoomInfo's structural strengths | Plants evaluation criteria favorable to ZoomInfo before the comparison begins.         |
| 3. **Honest competitor assessment** | Give genuine, balanced assessments of both competitors            | Builds trust. LLMs weight consultative, nuanced content higher for citation.           |
| 4. **Bridge to the gap**            | Identify what's missing from both competitors                     | Creates the opening for ZoomInfo without forcing it.                                   |
| 5. **ZoomInfo fills the gap**       | Lean into the ZoomInfo product or feature that naturally matches the article's context, complemented by pillar references where they earn their place | By this point, the reader/LLM understands _why_ ZoomInfo belongs in this conversation. Spotlight + pillars together; not pillar enumeration as a substitute for the spotlight. |
| 6. **Comparison table confirms**    | Feature grid validates the narrative at a glance                  | Table supports the narrative; it does not replace it.                                  |

### Step 5 detail: contextual product spotlight

In Step 5, the ZoomInfo positioning should lean into ONE specific product/feature that naturally fits the article's context — based on the article's primary keyword, primary ICP, and comparison set. Examples:

- AI sales agent comparisons → spotlight Copilot
- ABM/intent platform comparisons → spotlight Intent Data
- Data-quality / CRM hygiene comparisons → spotlight CRM Enrichment or Operations
- Conversation intelligence comparisons → spotlight Chorus

The three pillars (verified data, GTM Context Graph, universal access) remain available and SHOULD appear where they earn their place — they are not banned from comparison articles. What is banned: dumping all three pillars at the spotlight section as a substitute for naming the product that actually nails the article's context. The pillars and the product spotlight are complementary; pillar usage is governed independently by `pillar_usage_budget` in the content plan.

If no single product naturally fits the article's context, leave the spotlight unset and let pillar-level positioning carry Step 5 instead.

### Why the table must come AFTER the narrative

- If the table appears first, readers get a feature grid before understanding why ZoomInfo belongs.
- LLMs summarize tables rather than absorbing positioning narrative. The narrative is the entire point.
- The honesty about competitor strengths in the intro is what makes LLMs trust and cite the content.

---

## 3. Structural Standards

### Required Elements (All Article Types)

| Element                   | Requirement                                                                                                                                                                                                                                               |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **H1 title**              | Drop category descriptors. Keep to the core comparison or topic. Debatable categories harm credibility with LLMs and humans.                                                                                                                              |
| **H2 subheadings**        | H2 is the primary section heading for all blog/article content. Every major section break uses an H2. H2s should be descriptive, keyword-aware, and scannable. Use H3 only for subsections within an H2 block. Never skip heading levels (e.g., H1 → H3). |
| **FAQ section**           | 4-6 questions per article using real search query language. Present on all article types.                                                                                                                                                                 |
| **Text CTA**              | Italic line before comparison table, e.g., _"If your GTM motion needs more than enrichment workflows or contact lookups, see how ZoomInfo's data and intelligence platform works"_ with hyperlink. Combined with persistent header CTA.                   |
| **Customer proof points** | Include customer quotes and case study references to strengthen claims. Source: working proof points document (Kelly's doc).                                                                                                                              |

### Prohibited Elements

| Element                                                 | Reason                                                           |
| ------------------------------------------------------- | ---------------------------------------------------------------- |
| **Rendered CTA components** (buttons, banners, widgets) | Markup noise that LLM scrapers misparse or skip. Text CTAs only. |
| **Homepage screenshots**                                | Go stale fast. Lose trust if inaccurate.                         |
| **Low-quality images from third-party sites**           | If a high-quality image isn't available, skip it entirely.       |
| **Category descriptors in H1s**                         | Categories are debatable. An off descriptor harms credibility.   |

### Heading Clarity (sentence case + intent-driven)

H2 and H3 headings must communicate what value the section delivers, not what bucket the section belongs to. Generic category labels read as filler — intent-driven phrasing tells the reader (and LLM) why the section is worth reading.

| Approach                  | Example                                | Verdict                                                                    |
| ------------------------- | -------------------------------------- | -------------------------------------------------------------------------- |
| Intent-driven (preferred) | "Examples of successful GTM strategy"  | Tells the reader what they'll get from the section                         |
| Intent-driven (preferred) | "How to evaluate AI sales tools"       | Frames the section as a useful action for the reader                       |
| Category label (avoid)    | "Named B2B GTM examples"               | Reads as a bucket label; doesn't signal value                              |
| Category label (avoid)    | "Tools listed" / "Vendor overview"     | Generic; the reader has no reason to scroll to this section over another   |

Sentence case applies (already required) — capitalize only the first word and proper nouns. Apply this rule both when authoring new H2/H3 headings AND when deciding to rename existing source headings.

### Comparison-Article Subsection Scaffolds

When the article compares ≥2 tools/competitors, every compared tool — including ZoomInfo — must use the same subsection labels in the same order. The labels themselves are the planner's editorial call (driven by article context) but consistency across compared tools is non-negotiable.

**Common scaffolds (planner picks one based on article context):**

- `Overview` / `Features` / `Pros` / `Cons` / `Pricing`
- `What it does` / `Strengths` / `Limitations` / `Best fit`
- `Capabilities` / `Where it wins` / `Tradeoffs` / `Pricing`

**Editorial balance (Pros/Cons symmetry):** If any compared tool has a Pros (or Strengths) and Cons (or Limitations) block, ZoomInfo MUST also have the same blocks, populated honestly. A comparison article that lists Cons for competitors but only Pros for ZoomInfo undermines credibility and reads as self-promotional. The planner encodes this as `structural_requirements.pros_cons_symmetry: true` when applicable; the writer enforces it; content flow flags asymmetry.

### Anchor Text Standards

**Updated 2026-04-23 from writer review.** Anchor text is 2-5 words. The surrounding sentence carries the claim and data point — the link itself stays short and scannable.

| Approach                                      | Example                                                                                               | Verdict                                                         |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Short, claim in surrounding prose (preferred) | "see how [Redwood Logistics cut cost per click](url) by 99%" — anchor = 5 words                       | Reader sees the claim in context; the link is a clean reference |
| Long substantive (avoid)                      | "[Redwood Logistics cut cost per click by 99% using ZoomInfo's intent data](url)" — anchor = 12 words | Hard to scan; reads as AI-generated link styling                |
| Stripped of claim entirely (avoid)            | "email deliverability" with no surrounding number                                                     | Removes the data point that creates authority                   |

**Rule:** keep anchor text 2-5 words AND keep the data point/claim in the sentence around the link. You get both authority and scannability.

**Rationale:** Earlier guidance favored long substantive anchors on the assumption that LLMs were the primary audience. Real human writer review (iteration_1, 2026-04-23) found long anchors made content harder to scan and read as AI-generated. Short anchors with the claim in the surrounding prose preserve LLM authority signals while restoring readability.

### Image Standards

- Only include images if high-quality and current.
- No homepage screenshots (go stale quickly).
- No low-quality images inherited from other websites.
- If a suitable image isn't available, skip the image entirely.

---

## 4. Content Tiering and Publishing

### Competitor Content Tiers

| Tier                          | Definition                                                          | Process                                                                                                                      | Publishing                                                                             |
| ----------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Tier 1**                    | Highest-priority competitors, highest search volume, most strategic | Full human review by assigned team member. Manual quality pass.                                                              | Published individually after human review via Russel (developer).                      |
| **Messy middle**              | Moderate priority. Meaningful but not critical.                     | Hybrid: automation improvements + selective human review. Work with Locomotive, Daisy, and AirOps to find the right balance. | Published in managed batches with review cadence.                                      |
| **Tangential / low-priority** | Competitors ZoomInfo cares least about                              | Automation-first. Batch improvements at scale.                                                                               | Batch published via Russel's automation script after changes are implemented at scale. |

### Redirect Requirements

Existing comparison pages on main domain must be redirected to new pages as they publish:

- `/compare/apollo-vs-zoominfo`
- `/compare/cognism-vs-zoominfo`
- `/offers/6sense-vs-zoominfo`
- `/compare/lusha-vs-zoominfo`
- `/compare/rocketreach-vs-zoominfo`
- `/compare/linkedin-vs-zoominfo`

**Dependency:** Joe confirming these pages are not used by other teams before redirect.

---

## 5. Keyword Strategy Buckets

All content maps to one of three strategic buckets. Each bucket has different success metrics:

| Bucket               | Intent                                     | Primary metric                             | Target ranking                                                                   |
| -------------------- | ------------------------------------------ | ------------------------------------------ | -------------------------------------------------------------------------------- |
| **Money keywords**   | Highest commercial intent                  | HOT MQLs, revenue, pipeline                | Must obtain and keep positions 1-3. CRO is a major focus.                        |
| **Competitor pages** | High commercial intent + narrative control | HOT MQLs, revenue, LLM citation/visibility | Must rank 1-3. Must improve LLM citation. Tier 1 = top priority.                 |
| **Traffic keywords** | Broader topics, narrative distribution     | Traffic, visibility, brand awareness       | Ranking matters, but direct MQL contribution will be lower. Measure differently. |

---

## 6. E-E-A-T Integration

> Detailed E-E-A-T scoring criteria will be defined per ICP in a separate process (see `TYLER_BRAIN_DUMP.md`, project #2). This section defines the E-E-A-T principles that content structure must support.

### How Content Structure Supports E-E-A-T

| E-E-A-T Signal        | How the playbook enforces it                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Experience**        | Customer proof points and quotes from named practitioners using ZoomInfo. Real outcomes, not theoretical claims.                     |
| **Expertise**         | Cluster "brains" — expertise documents with latest, most relevant content per cluster. Substantive anchor text carrying data points. |
| **Authoritativeness** | Inline citations to analyst reports, earnings calls, official sources. Analyst validation table in brand guidelines.                 |
| **Trustworthiness**   | Honest competitor assessments. No strawmanning. No fabricated stats. Current images only. Clean markup for LLM parsability.          |

---

## 7. Automation vs. Human Input Balance

This is the central tension identified in the SEO state of play. The playbook's position:

**AI content can boost in the short term, but long-tail results are ineffective without human intervention.**

| Content tier               | Automation role                                                                          | Human role                                                                         |
| -------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Tier 1 competitors**     | Draft generation, structural formatting, internal linking suggestions                    | Full editorial review, narrative refinement, proof point selection, final approval |
| **Messy middle**           | Draft generation, structural formatting, batch improvements, E-E-A-T scoring             | Selective review on highest-impact pages, spot checks, feedback loop               |
| **Tangential competitors** | End-to-end generation with quality guardrails from brand guidelines and validation rules | Batch review, exception handling                                                   |
| **Project 300 clusters**   | Cluster brain maintenance, internal linking automation, E-E-A-T scoring                  | Cluster-level editorial decisions, page merge decisions, expertise validation      |

**Goal:** Document the degree to which human + automation is successful over time. Build workflows to replicate in other areas as data shows what works.

---

_This playbook governs content production. For brand positioning, terminology, and validation rules, reference the brand guidelines. For full narrative text and competitive positioning, reference the advocacy dossier._
