---
brand: S&P Capital IQ
slug: s-p-capital-iq
primary_url: https://www.spglobal.com/marketintelligence
category: market-intelligence
secondary_categories:
- b2b-data
positioning_archetype: tangential
competes_with_zi_pillars:
- data
competes_with_zi_products:
- Data (Pillar 1)
- APIs & MCP
icp_relevance:
- tangential
pricing_model: enterprise_only
has_free_tier: false
has_mcp_server: false
has_conversation_intelligence: false
has_abm_advertising: false
has_predictive_scoring: false
analyst_recognition:
- TrustRadius likelihood-to-recommend 7.0
research_depth: full
date_researched: 2026-05-08
flags:
- manual_review:icp_mismatch
- vs_brand_missing
- pricing_blocked
- thin_content_spglobal_403
sources_count: 10
sub_products:
- s-p-capital-iq--capital-iq-pro
- s-p-capital-iq--excel-plugin
- s-p-capital-iq--xpressapi
- s-p-capital-iq--compustat-xpressfeed
type: competitive-landscape
id: ctx.competitors.brands.s-p-capital-iq
title: S&P Capital IQ
description: ''
scope_id: zoominfo
durability: persistent
criticality: hybrid
status: approved
provenance: competitor-wiki/wiki/competitors/s-p-capital-iq.md
source_type: competitor
source_path: competitor-wiki/wiki/competitors/s-p-capital-iq.md
tags:
- competitive-landscape
- competitors
resource: https://www.spglobal.com/marketintelligence
---

# S&P Capital IQ

## Sub-products

- [[s-p-capital-iq--capital-iq-pro|S&P Capital IQ Pro]] — competes with Data (Pillar 1)
- [[s-p-capital-iq--excel-plugin|Capital IQ Excel Plug-in]] — competes with ZoomInfo Operations
- [[s-p-capital-iq--xpressapi|Market Intelligence XpressAPI]] — competes with APIs & MCP
- [[s-p-capital-iq--compustat-xpressfeed|Compustat & Xpressfeed]] — competes with Data as a Service

## Summary

S&P Capital IQ is a financial-markets intelligence platform sold by S&P Global Market Intelligence to investment bankers, equity-research analysts, private-equity professionals, valuation firms, and corporate development teams — the front-office desktop for capital-markets workflows, peer to Bloomberg / LSEG Workspace / FactSet (source: https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf). Its primary surfaces are the web-based Capital IQ Pro platform, the Excel Plug-in (with click-through audit-to-source on every data point), and a REST/JSON API (Market Intelligence XpressAPI / Capital IQ API). Overlap with ZoomInfo is narrow and adjacent: Capital IQ profiles 62,000 public and 4.4M private companies plus 3.8M executives, but the dataset is tuned for financial analysis (cap structure, ratings, M&A history, fundamentals) rather than GTM signals — and TrustRadius shows zero ratings against ZoomInfo on Prospecting, Sales Intelligence Data, or Lead Qualification, confirming Capital IQ does not sell into the SDR/AE prospecting use case (source: https://www.trustradius.com/compare-products/capital-iq-vs-zoominfo-sales). Treat as ICP-mismatch — see flags.

## Company Snapshot

| Field | Value |
|---|---|
| Category | Financial markets intelligence / capital-markets data and analytics platform |
| Founded / HQ | Founded 1998–1999 in New York City; acquired by McGraw-Hill (now S&P Global) in 2004 for >$200M; rebranded to S&P Global Market Intelligence in 2016 (sources: https://about.tagnifi.com/capital-iq-reviews-features-pricing-and-alternatives/, https://www.investopedia.com/terms/c/capital-iq.asp) |
| Funding / Ownership | Wholly owned division of S&P Global Inc. (NYSE: SPGI); part of the S&P Global Market Intelligence segment |
| Employee size | ~13,000+ employees attributed to Capital IQ / Market Intelligence on LinkedIn; TrustRadius cites ~5,000 specifically for the Capital IQ business unit (source: https://about.tagnifi.com/capital-iq-reviews-features-pricing-and-alternatives/) |
| Primary buyer | Investment bankers, equity research analysts, private equity / VC professionals, asset managers, corporate development / corporate finance, valuation firms, accounting / advisory firms |

## Product Offerings

### S&P Capital IQ Platform (web-based)

> **Wiki:** [[s-p-capital-iq--capital-iq-pro]]

- **What it does:** Web-based financial intelligence platform combining deep company, market, and people data with screening, modeling, charting, and workflow tools.
- **Key features:**
  - Company Intelligence on 62,000+ public companies and 4.4M private companies (financials, comparables, business relationships, governance)
  - S&P Capital IQ Financials covering 88,000 public companies (~99% of global market cap) and 825,000 private companies
  - Industry-specific data and standardized financial-statement templates across 17 industries (Banks, Insurance, REITs, Oil & Gas, Health Care, etc.)
  - Capital structure data on 82,000+ companies (debt) and 113,000+ (equity); fixed-income coverage with S&P / Moody's ratings, CDS, and security-level details
  - Estimates on 19,000+ active companies from 670+ contributors (EPS, Revenue, EBITDA, Long-Term Growth Rate, Target Price)
  - People Intelligence on 3.8M+ executives, board members, and investment professionals with Relationship Tree mapping
  - Real-Time Workstation with streaming quotes, news, and charting tied to user watch lists
  - Screening tool with 5,000+ financial and 3,000+ qualitative data points, plus Find Buyers / Targeting tools
- **Source URL:** https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf

### S&P Capital IQ Pro

> **Wiki:** [[s-p-capital-iq--capital-iq-pro]]

- **What it does:** Next-generation web platform with deeper near-real-time content, industry-specific modules (formerly SNL Financial), and AI-powered tools — positioned by Duke University Library as "analogous to LSEG Workspace or Bloomberg."
- **Key features:**
  - Deeper, more dynamic content than legacy Capital IQ; near real-time data updates
  - Industry-specific modules covering Banks, Thrifts, Insurance, and Financial Services (formerly SNL Financial)
  - ChatIQ — GenAI-powered multi-document research assistant launched Oct 2025 that analyzes filings, transcripts, investor presentations, and news in a single query
  - Premium analyst (aftermarket) equity research from Citigroup, Barclays, and other top investment banks — exclusive on Capital IQ Pro starting Fall 2025
  - Transaction Screener for M&A and deal screening
  - Dashboards for streaming pricing changes, key developments, news, and earnings calls
- **Source URL:** https://www.spglobal.com/market-intelligence/en/solutions/products/sp-capital-iq-pro

### Capital IQ Excel Plug-in

> **Wiki:** [[s-p-capital-iq--excel-plugin]]

- **What it does:** Microsoft Excel add-in that pulls financial, market, and company data into models with click-through auditability back to source filings.
- **Key features:**
  - Library of 140+ prebuilt templates (trading comps, deal comps, credit comps, M&A and LBO models)
  - Custom Formula Builder for proprietary functions
  - Click-through audit-to-source for every data item (a recurring TrustRadius praise point)
  - Integrates with watch lists, screens, and saved comp sets from the web platform
  - Windows-only — no Mac support, repeatedly flagged by users (source: https://about.tagnifi.com/capital-iq-reviews-features-pricing-and-alternatives/)
- **Source URL:** https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf

### PresCenter

- **What it does:** Productivity suite for Microsoft Office that links Excel models to PowerPoint and Word so deal documents stay in sync.
- **Key features:**
  - Quick Keys for Excel formatting and shortcut commands
  - Dynamic links between Excel, PowerPoint, and Word
  - Custom content libraries for branded deal templates
  - Application Specialist team for onboarding and advanced training
- **Source URL:** https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf

### Market Intelligence XpressAPI / S&P Capital IQ API

> **Wiki:** [[s-p-capital-iq--xpressapi]]

- **What it does:** REST/JSON APIs that deliver Market Intelligence financial and non-financial datasets on demand without requiring customers to host the underlying database.
- **Key features:**
  - REST/JSON over HTTPS; pick-and-choose dataset access
  - Standardized fundamentals covering ~99% of global market capitalization
  - S&P Global Ratings & Research data on 1M+ entities and securities
  - Cross Reference Services for entity / security identifier mapping
  - Python SDK (SPGMICIQ) and API Drive bulk-download for workflow integration
- **Source URL:** https://www.marketplace.spglobal.com/en/solutions/api-solutions-(61953ac7-ea64-4fac-926a-feb7f846c2be)

### Compustat & Xpressfeed

> **Wiki:** [[s-p-capital-iq--compustat-xpressfeed]]

- **What it does:** Bulk financial and statistical market data feeds — Compustat (dating to 1962) delivered via Xpressfeed for users to plug into their own quant tools.
- **Key features:**
  - Compustat fundamentals dating back to 1962 across global equities
  - Xpressfeed delivery for proprietary models and quant systems
  - Money Market Directories for foundations, endowments, and similar funding sources
- **Source URL:** https://www.investopedia.com/terms/c/capital-iq.asp

## Pricing

| Tier | Price | What's included | Source |
|---|---|---|---|
| Capital IQ entry annual price (TagniFi-cited) | $30,000+ / year | Single-platform seat with public, private, M&A, equity, and economic data; equity research reports priced separately | https://about.tagnifi.com/capital-iq-reviews-features-pricing-and-alternatives/ |
| Real-world deployments (TagniFi field data) | $55K (5-user IB firm) → $63K (8-user CPA) → $75K (4-user PE) → $125K (25-user CPA) → $600K (400-user valuation firm) per year | Negotiated multi-seat enterprise contracts | https://about.tagnifi.com/capital-iq-reviews-features-pricing-and-alternatives/ |
| Capital IQ Pro (Capterra) | "Contact vendor" — no free trial, no free version | Web platform plus Excel add-in; pricing handled by S&P sales | https://www.capterra.com/p/210149/S-P-CAPITAL-IQ-PLATFORM/ |

S&P does not publish pricing on its own site (the spglobal.com pages 403 to scrapers — see Flags); above figures are sourced from TagniFi field data and Capterra. TagniFi also flags "expensive subscriptions" and "aggressive annual cost increases" as the top reasons customers leave Capital IQ.

## Target Audience & ICP

- **Industries called out:** Investment banking, private equity / venture capital, asset management, equity research, corporate finance / corporate development, valuation and accounting / advisory firms, banks / insurance / financial services (industry-specific modules from SNL).
- **Company size called out:** Mid-market through enterprise; Capterra lists freelancers and small business under "typical users," but the pricing tiers and feature depth target enterprise capital-markets teams.
- **Persona / role focus:** Investment banking analysts and associates, equity research analysts, portfolio managers and buy-side analysts, PE / VC investment professionals, corporate development / M&A teams, valuation specialists and CPAs, credit analysts.
- **Use cases promoted:**
  - Comparable-company and precedent-transaction analysis
  - M&A deal screening and target identification (Find Buyers / Targeting)
  - Credit risk assessment and probability-of-default modeling (Credit Health Panel, CreditModel)
  - Building and updating financial models (Excel Plug-in templates for LBO, M&A, comps)
  - Real-time market and news monitoring for covered companies
  - Premium analyst research consumption (post-Fall 2025 transition from LSEG Workspace)

## Integrations & Ecosystem

- **CRMs:** Capital IQ-to-CRM connectors exist but are flagged as a "high cost" line item by TagniFi (source: https://about.tagnifi.com/capital-iq-reviews-features-pricing-and-alternatives/); specific named CRMs (Salesforce, HubSpot, Dynamics) were not surfaced on reviewed pages.
- **Sales engagement / outreach:** _Integration list not surfaced on reviewed pages._ Capital IQ does not sell into sales-engagement workflows.
- **Data / enrichment:** Private-company financials sourced via Dun & Bradstreet partnership; Outlook Plug-in syncing investor conferences and earnings calls to user calendars; Excel Plug-in for direct data pull into models; PresCenter for PowerPoint / Word linking.
- **Other notable integrations:** Market Intelligence XpressAPI and S&P Capital IQ API (REST/JSON over HTTPS); Python SDK (SPGMICIQ) for end-of-day and time-series financial data; API Drive bulk-download / data feed; PresCenter for Microsoft Office (Excel, PowerPoint, Word).

## Differentiators (vs the broader category)

- Audit-to-source financials — every value in the Excel Plug-in click-throughs back to the original filing, valued highly by valuation and audit teams (source: https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf)
- Industry-specific data and standardized financial-statement templates across 17 industries (Banks, Insurance, REITs, Oil & Gas, etc.) with SNL-derived sector modules (source: https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf)
- Coverage of 99% of global market capitalization via 88,000 public companies and 825,000 private companies with standardized financials (source: https://www.investopedia.com/terms/c/capital-iq.asp)
- Premium analyst (aftermarket) equity research from Citigroup, Barclays, and other top investment banks — exclusive on Capital IQ Pro from Fall 2025 after the LSEG Workspace transition (source: https://www.spglobal.com/market-intelligence/en/solutions/products/sp-capital-iq-pro)
- ChatIQ GenAI multi-document research assistant (launched Oct 2025) that analyzes filings, transcripts, investor presentations, and news in a single query (source: https://www.spglobal.com/market-intelligence/en/solutions/products/sp-capital-iq-pro)
- Application Specialist teams (former investment bankers) for Excel model conversion, screening setup, and PresCenter onboarding — high-touch service typical of capital-markets vendors (source: https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf)

## Crossover With ZoomInfo

- **Direct overlap:** Capital IQ Company Intelligence (62,000 public + 4.4M private profiles, 3.8M executive profiles) overlaps ZoomInfo's Data foundation at the company-firmographic and executive-profile layer — but Capital IQ's profiles are tuned for capital-markets analysis (financials, governance, ownership, cap structure, M&A history) rather than GTM signals like direct dials, intent, or buyer behavior (source: https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf). The two platforms do NOT share the GTM Context Graph layer, GTM Workspace seller surface, or GTM Studio marketer surface.
- **Adjacent overlap:** Capital IQ APIs and Excel Plug-in deliver structured company / financial data into internal models and CRMs — the same data-into-CRM pattern ZoomInfo Operations and APIs & MCP target — but the payload is fundamentals / cap structure / ownership rather than verified contacts and buying signals (source: https://www.marketplace.spglobal.com/en/solutions/api-solutions-(61953ac7-ea64-4fac-926a-feb7f846c2be)). TagniFi explicitly flags "high cost of API and CRM integrations" as a Capital IQ pain point, suggesting price pressure where the two products meet (source: https://about.tagnifi.com/capital-iq-reviews-features-pricing-and-alternatives/). Notably, Capital IQ's private-company data is sourced via a Dun & Bradstreet partnership — meaning Capital IQ relies on the same upstream vendor ZoomInfo competes against in B2B data.
- **No overlap:** Equity research, credit ratings, capital structure, fixed-income coverage, M&A transaction history, league tables, fund / institutional ownership, commodities pricing, macroeconomic data, real-time streaming quotes, premium broker research from Citigroup / Barclays, and ChatIQ multi-document research are core Capital IQ datasets with no analogue in ZoomInfo's GTM Platform (source: https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf). Conversely, Capital IQ has no sales-prospecting workflow at all — TrustRadius rates Capital IQ on zero categories under Prospecting (Advanced search, Identification of new leads, Ideal customer targeting, etc.), Sales Intelligence Data Standards, Data Augmentation & Lead Qualification, or Sales Intelligence Email Features, while ZoomInfo carries 700+ ratings in each (source: https://www.trustradius.com/compare-products/capital-iq-vs-zoominfo-sales). Capital IQ does not sell into sales, marketing, RevOps, or developer / agent-builder ICPs.
- **Their pitch against ZoomInfo (if found):** No public competitor-authored or ZoomInfo-authored vs-page surfaced — neither vendor positions head-to-head against the other. The closest signal is a TrustRadius user testimonial: _"I think in terms of quality and depth of the data when comparing the two, ZoomInfo is more in-depth and I feel like it is more accurate than Capital IQ. I don't get the feeling that Capital IQ is updated and refreshed nearly as much as ZoomInfo is, which is primarily why I lean [toward ZoomInfo]"_ (source: https://www.trustradius.com/compare-products/capital-iq-vs-zoominfo-sales). See `vs_brand_missing` flag.

## Messaging & Positioning Notes

- **Top-line value prop (their words):** "A powerful array of financial data, analytics and research" on a single web-based platform "for analysis, idea generation and workflow management" — the front-office desktop for capital-markets professionals (source: https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf).
- **Recurring proof points:** 62,000+ public and 4.4M private company profiles; 88,000 public-company financials covering ~99% of global market cap; 5,000+ financial and 3,000+ qualitative data points for screening across 17 industries; 135 billion data points analyzed annually (Investopedia); 20,000+ news sources feeding 124 Key Developments types; 5,550+ companies with earnings transcripts; premium aftermarket research partnerships with Citigroup, Barclays, and other major investment banks; TrustRadius likelihood-to-recommend score of 7.0 (10 ratings) with strong praise for "audit-to-source" Excel Plug-in.
- **Tone / category framing:** Positioned as a peer to Bloomberg Terminal, LSEG Workspace, and FactSet — Duke Library notes "Capital IQ Pro is analogous to LSEG Workspace or Bloomberg." It is NOT positioned in the GTM / sales-intelligence category at all. Tone is institutional, finance-vernacular ("comparable analysis," "Find Buyers," "Credit Health Panel," "PresCenter").

## Flags & Limitations

- `manual_review:icp_mismatch` — S&P Capital IQ sells capital-markets intelligence to investment bankers, equity-research analysts, and PE/VC professionals; ZoomInfo sells GTM intelligence to sales, marketing, and RevOps. Direct overlap is limited to firmographic company data; the two are not true GTM competitors despite both offering deep company datasets.
- `thin_content@https://www.spglobal.com/market-intelligence/en/solutions/products/sp-capital-iq-pro` — page returned HTTP 403 to both Jina and curl_cffi fallback; Capital IQ Pro details sourced from third-party reviewers (Capterra, Stanford / Duke library guides, PR Newswire releases, TrustRadius)
- `thin_content@https://www.spglobal.com/market-intelligence/en` — Market Intelligence homepage HTTP 403 blocked
- `thin_content@https://www.spglobal.com/market-intelligence/en/industries/investment-banking` — Investment Banking solution page HTTP 403 blocked
- `thin_content@https://www.spglobal.com/market-intelligence/en/solutions/artificial-intelligence/ai-solutions-directory` — AI Solutions directory HTTP 403 blocked
- `vs_brand_missing` — no S&P-authored or ZoomInfo-authored vs-page surfaced; only a TrustRadius user testimonial is available as a comparison signal
- `pricing_blocked@https://www.spglobal.com/market-intelligence/en/solutions/products/sp-capital-iq-pro` — Capital IQ does not publish pricing on its own site; figures sourced from TagniFi field-cited deployments and Capterra "Contact vendor"

## Sources

| URL | Status | Used For |
|---|---|---|
| https://www.spglobal.com/market-intelligence/en/solutions/products/sp-capital-iq-pro | blocked (403) | product (Capital IQ Pro) |
| https://www.spglobal.com/market-intelligence/en | blocked (403) | homepage |
| https://www.spglobal.com/market-intelligence/en/industries/investment-banking | blocked (403) | ICP / investment-banking solution |
| https://www.spglobal.com/market-intelligence/en/solutions/artificial-intelligence/ai-solutions-directory | blocked (403) | product (AI / ChatIQ) |
| https://www.trustradius.com/compare-products/capital-iq-vs-zoominfo-sales | success | vs_brand, ICP, feature gap |
| https://about.tagnifi.com/capital-iq-reviews-features-pricing-and-alternatives/ | success | pricing, history, integrations notes |
| https://www.lib.sfu.ca/system/files/33579/s-p-capital-iq-platform-brochure.pdf | success | products, features, ICP, differentiators |
| https://www.investopedia.com/terms/c/capital-iq.asp | success | history, Compustat / Xpressfeed, scale stats |
| https://www.capterra.com/p/210149/S-P-CAPITAL-IQ-PLATFORM/ | success | pricing (Contact vendor), reviews |
| https://www.marketplace.spglobal.com/en/solutions/api-solutions-(61953ac7-ea64-4fac-926a-feb7f846c2be) | success | integrations, API |
