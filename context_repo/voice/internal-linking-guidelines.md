---
type: how-we-write
id: ctx.voice.internal-linking-guidelines
title: Internal Linking Guidelines
description: ''
scope_id: zoominfo-brand
durability: persistent
criticality: hybrid
status: approved
provenance: content_brand_documents/internal_linking_guidelines.md
source_type: source-document
source_path: content_brand_documents/internal_linking_guidelines.md
tags:
- editorial
- how-we-write
- internal-linking
---

# Internal Linking Guidelines

> Reference for the ZoomInfo content pipeline. Use these rules when selecting and placing internal links — case studies, product pages, and solution pages — in any content asset.
>
> **Core principle: every internal link should earn its place.** If a link doesn't genuinely help the reader, leave it out. No link is always better than a forced link.

> An Update to internal linking rules

---

## Hard Rules (Non-Negotiable)

These rules apply to every link in every piece of content. No exceptions.

1. **NEVER fabricate URLs.** Every link must point to a URL that has been verified to return HTTP 200. If you're unsure whether a page exists, don't link to it. Run `scripts/validate_links.py` before marking content delivery complete. Fabricated links — analyst report pages, survey pages, or product pages that don't exist — are the single worst internal linking mistake because they erode reader trust and signal to search engines that the site has quality issues.

2. **No external domain links** unless the URL was already present in the original source content. Do not link out to Forbes, HBR, Gartner, Forrester, or any non-ZoomInfo domain. External links leak authority and frequently go 404 over time. If you need to cite an external source, reference it as plain text (e.g., "according to Forrester's evaluation...") without hyperlinking. The only acceptable domains for links are:
   - `www.zoominfo.com`
   - `pipeline.zoominfo.com`
   - `market.zoominfo.com`
   - `docs.zoominfo.com`
   - `gtm.ai` — canonical product surface for the GTM Context Graph and GTM AI platform (ZoomInfo property; canonical URL per `brand_guidelines.md` Section 1)

3. **All links must be validated before delivery.** Run `scripts/validate_links.py` on the final content. Any link returning non-200 must be either fixed or removed. This is a hard gate — content with broken links should never be delivered.

4. **No parenthetical case study links.** Never trail a sentence with `([Company case study](URL))` as a citation. The link must be embedded in the natural flow of the sentence — typically anchored on the metric phrase itself (e.g., `[Brown & Brown booked 208% more meetings](URL) after combining intent data...`) or on a natural reading-path phrase (`See how [Outreach lifted connect rates 7×](URL)`). Parenthetical attribution is an academic-citation pattern, not a reader-helpful link, and it consistently produces weak anchor text. If the only place a link fits is in parentheses at the end of a sentence, the sentence needs to be rewritten so the metric or proof point can carry the anchor.

5. **Strong CTAs MUST carry a link.** Any conversion-oriented call-to-action — "Request a demo", "Get a demo", "Start a free trial", "Talk to sales", "See it in action", "Schedule a walkthrough", or any italicized/imperative closing line that invites the reader to take a next step — must hyperlink the action phrase. A CTA without a link is dead weight: it costs the reader's attention without giving them the destination. The canonical destination for ZoomInfo demo/sales CTAs is `https://www.zoominfo.com/free-trial-contact-sales`. The link must be in the writer's output, not deferred to a downstream "designer will fix it" step. Anchor on the action phrase itself (e.g., `[Request a demo](https://www.zoominfo.com/free-trial-contact-sales)`) — never anchor on a generic word like "here". A CTA without a link is a HARD verification failure.

---

## The Problem

ZoomInfo's current internal linking workflow relies on `site:zoominfo.com` search to find link targets. This produces generic, poorly matched case study placements — a cybersecurity-focused article linking to an unrelated SMB case study, or a RevOps piece linking to a sales prospecting story. The result: links that look like SEO filler rather than genuinely useful references.

## The Fix: Context-Matched Case Study Linking

Every case study in the wiki has structured metadata:

```yaml
products: [Sales, Intent Data, Copilot]
icps: [sales_ae_sdr, revops_gtm_eng]
industry: Cybersecurity
company_size: enterprise
recency_tier: fresh | recent | aging | undated
```

Use these fields to select case studies that actually match the content being written.

---

## Selection Rules

### 1. Match on ICP first, product second

The content's target ICP is the primary filter. A case study for the right persona with a tangential product is more valuable than a case study for the right product but wrong persona.

**Priority order:**
1. Same ICP + same product(s) + same industry
2. Same ICP + same product(s) + different industry
3. Same ICP + different product + same industry
4. Different ICP + same product(s) _(use sparingly — only when the proof point is undeniable)_

### 2. Recency tiers

| Tier | Definition | Linking guidance |
|------|-----------|-----------------|
| **fresh** | Published < 90 days ago | Preferred. Link freely. |
| **recent** | Published 90–180 days ago | Good. No restrictions. |
| **aging** | Published 180+ days ago (real date) | Acceptable if metrics/story are strong. |
| **undated** | CMS migration date (2025-07-29) | Treat as evergreen — actual publish date unknown. No recency penalty, but don't claim it's "new" or "recent." |

> **103 of 115 case studies have the migration date.** Do not filter these out — they represent the bulk of the library. Treat them as undated/evergreen and select purely on relevance.

### 3. Prefer specificity over brand recognition

A case study with "175% pipeline growth" from a lesser-known company is a better link than a Fortune 500 logo with vague outcomes. The reader clicked through for proof, not brand association.

**Strong link candidates have:**
- Quantified outcomes (%, $, Nx, time saved)
- Named products and how they were used
- A clear before/after narrative

**Weak link candidates have:**
- Vague outcomes ("improved efficiency")
- No specific metrics
- Generic product references

### 4. Zero is a valid number

Not every piece of content needs a case study link. If the article is educational, conceptual, or early-funnel, forcing a case study reference makes the content feel like a sales pitch disguised as a resource.

**Skip case study links when:**
- The content is a glossary, definition, or explainer with no product-specific angle
- No case study in the library genuinely matches the topic — a tangential case study is worse than none
- The content already has strong proof points (analyst citations, data stats) and adding a case study would feel redundant
- The article is short-form (< 500 words) and a case study link would dominate the link profile

**Include case study links when:**
- The content makes a specific claim about outcomes that a case study can substantiate
- The reader is mid-funnel or lower and would benefit from seeing a real customer example
- The case study directly mirrors the reader's likely use case, industry, or role

### 5. Density targets for case studies specifically

| Content length | Case study links |
|---------------|-----------------|
| < 800 words | 0–1 |
| 800–1,500 words | 0–2 |
| 1,500–2,500 words | 1–3 |
| 2,500+ words | 2–4 max |

These are **case study links only** — separate from product page and pillar page links. Total internal link density should stay within the existing 3–7 per 1,000 words guideline.

---

## Placement Rules

### Where to link case studies

1. **After a claim that needs proof** — "ZoomInfo helped teams reduce CPC by 99%" → link to Redwood Logistics case study
2. **In a "proof" or "results" section** — if the content has a dedicated results/outcomes section, case studies belong here
3. **Inline with a relevant use case description** — when describing how a product solves a problem, the case study is the receipt
4. **In a "Related reading" or "See also" block** — bottom-of-page contextual links

### Where NOT to link case studies

- **In the introduction** — the reader hasn't earned context yet; a case study link here feels like a hard sell
- **Inside data tables or comparison grids** — links in tables are visually noisy and rarely clicked
- **Stacked back-to-back** — never place two case study links in the same paragraph; space them across sections
- **On anchor text that's a data claim** — "96% email deliverability" should not be a hyperlink to a case study; it missets expectations about what the link contains
- **As the only internal link in a section** — if a section has one link and it's a case study, the section looks like an ad

### Anchor text

**Good:**
- "See how [Company] achieved [specific outcome] with [Product]" → natural, sets expectations
- "[Company] reduced [metric] by [amount]" → the proof point IS the anchor (preferred default)
- "Read the [Company] case study" → clear, honest label, used inline (not parenthetically)

**Bad:**
- "Learn more" → no context
- "Click here to see results" → generic
- "As shown in this case study" → vague; which case study?
- Using the full case study title as anchor → too long, looks like a citation not a link
- **Parenthetical citation pattern** — `Outreach saw a 7× lift in connect rates ([Outreach case study](URL))`. The metric is in the prose, the link is a tacked-on parenthetical. Always rewrite so the metric phrase carries the anchor: `[Outreach saw a 7× lift in connect rates](URL) within three weeks...`. This applies to every case study reference — no exceptions.

---

## Product & Solution Page Linking

Product and solution pages are the other major internal link target. The same "earn your place" principle applies — linking to a product page should feel like a natural extension of the content, not a detour into a sales funnel.

### When to link to a product/solution page

- **First mention of a product by name is the DEFAULT link.** When any ZoomInfo product (Sales, Marketing, Operations, GTM Studio, GTM Workspace, Copilot, Intent Data, Chorus, CRM Enrichment, WebSights, FormComplete, MCP, Data, etc.) is named for the first time in the article, link it to its product/solution page unless one of the explicit "When NOT to link" conditions below applies. Subsequent mentions stay unlinked. Hyperlinking every instance of "ZoomInfo Sales" is distracting; linking the first one is the baseline.
- **The content explains a problem the product solves** — if the article describes a pain point (stale CRM data, low connect rates, anonymous web traffic) and a ZoomInfo product directly addresses it, a link is appropriate. The reader is thinking "how do I fix this?" and the product page answers that question.
- **The reader needs to understand what a product does** — if the content references a product capability (e.g., "waterfall enrichment in GTM Studio") and the reader may not know what that means, linking helps them self-serve context.

### When NOT to link to a product/solution page

- **The product mention is incidental** — if an article mentions "ZoomInfo Sales" as part of listing the platform's components but the article isn't about sales prospecting, don't link it. Not every product name is a linking opportunity.
- **The content is educational and product-agnostic** — a "What is buyer intent data?" explainer should educate, not funnel. If the reader wanted a product page, they'd be on one. Linking to the Intent Data product page mid-explanation breaks trust.
- **You're creating a CTA where none belongs** — if the only way to make the link work is to add a sentence like "To learn more about how ZoomInfo solves this, visit our [Product] page," you're writing a CTA, not a link. If the content doesn't naturally reference the product, the link doesn't belong.
- **Multiple product links in the same section** — linking to Sales, Marketing, AND Operations in the same paragraph signals that you're linking for SEO coverage, not reader value. Pick the one most relevant to the section's point.

### Product link placement

**Natural placements:**
- In a "how it works" or "solution" section where the product is the answer to the stated problem
- When comparing approaches or tools and ZoomInfo's product is one option
- In a feature breakdown where linking to the full product page provides deeper detail

**Forced placements (avoid):**
- Bolted-on CTAs at the end of unrelated sections ("Speaking of data quality, check out ZoomInfo Operations")
- Inside author bios or boilerplate footers
- As the anchor text for a generic benefit claim ("improve your go-to-market strategy" linking to /platform)

### Anchor text for product links

**Good:**
- "[Product name]" on first mention → simple, honest, the reader knows what they'll get
- "ZoomInfo's [capability]" → links the capability, not just the brand name
- "[Product] automates [specific workflow]" → the anchor describes what the product does in context

**Bad:**
- "our platform" → vague, could go anywhere
- "the solution" → which solution?
- "powerful tools for revenue teams" → marketing copy posing as a link
- Full product taglines as anchor text → too long, reads like an ad

### MCP / API references — always linked

Every reference to MCP (Model Context Protocol) or API in ZoomInfo content must hyperlink to one of two canonical destinations:

1. **`https://gtm.ai/docs/mcp`** — developer/docs surface (technical audience, integration reference)
2. **`https://www.zoominfo.com/solutions/zoominfo-mcp`** — solution page (generalist/marketing audience, value framing)

**Rules:**

- **One mention** → link to whichever URL fits the audience best. Solution page for general/marketing audience; docs page for developer audience.
- **Two or more mentions** → alternate between the two URLs. Don't double-link to the same destination.
- **Phrases that count as an MCP/API reference:** "MCP", "MCP layer", "MCP server", "MCP integration", "Model Context Protocol", "APIs and MCP", "ZoomInfo MCP", "API/MCP", "API access" (when referencing ZoomInfo's programmatic surface). The conjunction "APIs and MCP" counts as one MCP reference — anchor on "MCP layer" or the whole phrase.
- **Unlinked MCP/API mentions are a MAJOR brand violation** (LINK-01 in `brand_guidelines.md` Section 6). MCP is a strategic differentiator for ZoomInfo (developer/AI-agent access lane in Pillar 3 / Universal Access); unlinked mentions waste a high-intent SEO + LLM-citation surface.

**Why this rule exists:** ZoomInfo's MCP server is a recent product surface (active, standalone — see `brand_guidelines.md` Product Name Accuracy table) with growing developer + AI-agent adoption. Every content mention of MCP/API is a chance to feed the canonical landing pages with link equity AND to surface the right destination to LLMs that may later cite the article when answering "does ZoomInfo support MCP?" or "what's the ZoomInfo API?".

### Product link density

| Content length | Product/solution links |
|---------------|----------------------|
| < 800 words | 0–2 |
| 800–1,500 words | 1–3 |
| 1,500–2,500 words | 2–4 |
| 2,500+ words | 3–5 max |

Combined with case study links, total internal links should stay within **3–7 per 1,000 words**. If you're hitting the ceiling, prioritize whichever link type serves the reader better for that specific piece of content.

---

## Link Distribution Across the Article

Links should be distributed across the full article, not concentrated in early sections. Front-loading links is a common pipeline failure mode — the introduction and first H2 carry most of the case study and product references, then tail-end sections have nothing.

### Distribution guideline

Roughly split the article body into thirds (excluding FAQ unless FAQ contains links that genuinely serve the answer):

- **First third:** ≤40% of internal links
- **Final third:** ≥25% of internal links

These are guidelines, not hard math. The intent is even coverage so claims throughout the article carry sources, not just the opening sections. If a section legitimately has nothing worth linking, leave it unlinked rather than padding to hit the bound.

### FAQ links — expected, not optional

FAQ answers are dual-audience LLM-citation surfaces. AI Overviews, Perplexity, and chat models parse and cite FAQ answers as self-contained units, independent of the surrounding article. Each FAQ answer is its own micro-context. Treat FAQs as link-eligible by default, not as a tail-end afterthought.

**Default expectation: 50%+ of FAQ entries should carry at least one internal link.**

FAQ answers SHOULD contain internal links when:

- The FAQ asks about a concept that a ZoomInfo feature/product page defines (e.g., "What is intent data?" → link to `/features/intent-data`).
- The FAQ asks a comparison/integration question that a product page answers (e.g., "Can AI sales tools integrate with CRMs?" → link to GTM Workspace product page).
- The FAQ's answer cites a customer outcome that a case study proves (e.g., "Will AI replace sales reps?" → link to a case study showing augmentation).
- The FAQ's answer references a feature whose deeper explainer is on a blog or feature page (e.g., "How do AI sales tools handle data privacy?" → link to a relevant compliance/data page if one exists in the whitelist).

FAQ answers MAY NOT contain links that exist only to:

- Hit a distribution target without serving the answer
- Insert a CTA into the FAQ (CTAs belong in their own section)
- Stuff every available URL into FAQs to inflate density

**FAQ exception to the "exactly once" rule.** Principle 4 in `agents/content_planner.md` says each case study URL is linked exactly once at first mention. That rule applies to **body** placements. **FAQs are exempt** — a case study URL may legitimately appear once in the body (at first mention with metric anchor) AND once in a FAQ answer (proving an answer to a different question). Both placements serve the reader; both are independently parseable by LLMs. The "exactly once" guard exists to prevent duplicate CTAs in the body, not to penalize FAQ surfacing.

**Body links and FAQ links are counted separately for distribution checks.** When evaluating front-loading, the body distribution is computed without FAQ entries. FAQ links carry their own quality bar (each link must serve its specific answer) but don't compensate for an under-linked body.

When FAQ links are present and natural, they ALSO count toward the final-third distribution target above (a single link can satisfy both purposes).

### Product page reference

Full product wiki with summaries and capabilities at `case-studies-wiki/wiki/products/`. Key pages:

| Page | URL | Best for |
|------|-----|----------|
| ZoomInfo Sales | /products/sales | Prospecting, contact data, direct dials |
| ZoomInfo Marketing | /products/marketing | ABM, audience targeting, demand gen |
| ZoomInfo Operations | /products/operations | CRM data quality, routing, enrichment |
| GTM Studio | /products/gtm-studio | Codeless automation, play builder |
| GTM Workspace | /gtm-workspace | Unified seller workspace, account briefs |
| Copilot | /copilot | AI sales agent, account prioritization |
| Intent Data | /features/intent-data | Buyer signals, in-market accounts |
| Chorus | /products/chorus | Conversation intelligence, deal analysis |
| CRM Enrichment | /solutions/crm-enrichment | Automated CRM data maintenance |
| ZoomInfo MCP | /solutions/zoominfo-mcp | AI agent integration, API access |
| WebSights | /features/identify-website-visitors | Website visitor identification |
| FormComplete | /features/form-optimization | Form shortening, lead capture |
| ZoomInfo Data | /data | Core B2B database, data coverage |

---

## ICP-to-Case Study Quick Reference

Use this for fast lookups when writing for a specific ICP. Full lists are in the wiki at `case-studies-wiki/wiki/icps/`.

### Sales — AEs & SDRs (`sales_ae_sdr`)

**Best proof points:**
- Pipeline and quota outcomes
- Connect rate and direct dial success
- Time saved on prospecting/research
- Tool consolidation stories

**Top case studies (with metrics):**
- Palo Alto Networks — 1,500+ net-new accounts _(fresh)_
- Xpress Services — 15x revenue growth _(recent)_
- LevelUp Leads — high-volume outbound scaling _(recent)_
- AK Operations — 150% more deals closed
- Elite Interactive Solutions — $30k/month revenue lift

### Account Management & CS (`account_mgmt_cs`)

**Best proof points:**
- Churn reduction / retention improvements
- Expansion revenue and upsell outcomes
- Stakeholder visibility and account health
- Renewal prep and QBR quality

**Top case studies:**
- ChurnZero — customer success + churn prevention
- MongoDB — retention and conversation intelligence
- Sendoso — 70% reduction in inaccurate data, expansion
- Hudl — reduced evaluation time 75%
- Spekit — CS workflow with Copilot

### Marketing & Demand Gen (`marketing_demandgen`)

**Best proof points:**
- MQL/pipeline generation metrics
- Campaign ROI and conversion rates
- ABM program outcomes
- Form optimization results

**Top case studies:**
- Impartner — 12% pipeline boost with Marketing
- Redwood Logistics — 99% CPC reduction, 25 hrs/week saved
- DemandCapture — 1,000 meetings/month with FormComplete
- Remesh — MQL and CVR increases
- Mendix — 14x MQL-to-opportunity rate

### RevOps & GTM Engineers (`revops_gtm_eng`)

**Best proof points:**
- Data quality and CRM cleanup metrics
- Speed-to-lead improvements
- Vendor consolidation outcomes
- Enrichment and routing automation

**Top case studies:**
- Sendoso — 70% reduction in inaccurate data
- Snowflake — data enrichment and CRM integration
- Kaseya — 50% reduction in lead follow-up time
- MongoDB — workflow automation
- Watermark Insights — duplicate record removal

### Developers & AI Agent Builders (`developer_ai_builder`)

**Best proof points:**
- API/MCP integration outcomes
- Engineering time saved
- Data accuracy in production systems
- Compliance and security clearance speed

**Top case studies:**
- _(Limited case study coverage for this ICP — most developer stories are product-page focused rather than standalone case studies. Link to ZoomInfo MCP and Data-as-a-Service product pages instead.)_

---

## Integration with Content Pipeline

When the content generator agent runs, it should:

1. **Read the target ICP** from the content brief or topic cluster
2. **Read the primary product(s)** being discussed
3. **Query the wiki index** (or the CSV) filtering on `icps` and `products` fields
4. **Rank candidates** by: ICP match → product match → industry match → recency tier → metric strength
5. **Select 1–3 case studies** based on content length
6. **Place links** following the placement rules above
7. **Validate links** with `scripts/validate_links.py` before delivery

### Wiki file reference

```
case-studies-wiki/
├── case_studies_crawl.csv          # Source data with body_content
├── wiki/case-studies/*.md          # 115 individual pages with frontmatter metadata
├── wiki/products/*.md              # 29 product pages with linked case studies
├── wiki/icps/*.md                  # 5 ICP pages with linked products and case studies
└── index.md                        # Master index by industry
```

### Frontmatter fields for filtering

```python
# Example: find case studies for a RevOps article about CRM Enrichment
candidates = [cs for cs in case_studies 
              if 'revops_gtm_eng' in cs['icps'] 
              and 'CRM Enrichment' in cs['products']]
```
