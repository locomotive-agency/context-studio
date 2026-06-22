---
name: ZoomInfo MCP - Connect your AI to verified B2B intelligence
slug: zoominfo-mcp
source_url: https://www.zoominfo.com/solutions/zoominfo-mcp
canonical_docs_url: https://gtm.ai/docs/mcp
aliases:
- ZoomInfo MCP
- ZoomInfo MCP Server
- Model Context Protocol server
tags:
- api-access
- case-study-rollup
- mcp
- product
- product-and-offering
type: product-and-offering
id: ctx.products.zoominfo-mcp
title: ZoomInfo MCP - Connect your AI to verified B2B intelligence
description: ''
scope_id: product-zoominfo-mcp
durability: persistent
criticality: controlled
status: approved
provenance: case-studies-wiki/wiki/products/zoominfo-mcp.md
source_type: product
source_path: case-studies-wiki/wiki/products/zoominfo-mcp.md
resource: https://www.zoominfo.com/solutions/zoominfo-mcp
---

# ZoomInfo MCP - Connect your AI to verified B2B intelligence

**Source:** [https://www.zoominfo.com/solutions/zoominfo-mcp](https://www.zoominfo.com/solutions/zoominfo-mcp)
**Documentation:** [https://gtm.ai/docs/mcp](https://gtm.ai/docs/mcp)

## Summary

Model Context Protocol server that enables MCP-compatible AI tools (Claude, ChatGPT, custom agents) to query ZoomInfo's verified B2B intelligence directly inside their workflows. The differentiator: when an AI assistant researches an account through MCP, it draws from the same verified data the revenue team already trusts (100M+ companies, 500M+ contacts, intent signals, conversation intelligence, technographic data) rather than scraping the public web. ZoomInfo MCP is the API/MCP access lane to the [[gtm-context-graph|GTM Context Graph]].

## Key Capabilities

- Native MCP integration with Claude, ChatGPT, and any custom MCP client
- 15 native MCP tools across direct data lookup and AI-orchestrated context agents
- Verified decision-maker information, technographic intelligence, hiring signals, and intent data accessible via tool calls
- Conversation intelligence call data accessible to AI agents (via Chorus integration)
- Automatic tool updates: new tools become available at session start without client changes
- 3-step setup with existing ZoomInfo credentials

## Target Users

- Revenue professionals: AEs, SDRs, Account Managers, RevOps, Marketing Ops, Product Marketing
- Enterprise engineering teams building AI-powered GTM applications
- Use cases: account research, prospecting, competitive intelligence, outreach drafting, data enrichment, custom AI agent grounding

## MCP Tools

The MCP server exposes two tool categories. **Direct Tools** return raw structured data for the AI orchestrator to reason over; **Context Agents** run sub-agent layers that synthesize large data payloads into briefings before returning to the parent agent.

### Direct Tools (13)

| Tool                       | Purpose                                                        | Cost                  |
| -------------------------- | -------------------------------------------------------------- | --------------------- |
| Lookup                     | Retrieve acceptable filter values (industries, regions, roles) | Free                  |
| Search Companies           | Identify companies matching firmographic criteria              | Free                  |
| Search Contacts            | Locate contacts by role, employer, or activity signals         | Free                  |
| Enrich Companies           | Detailed firmographic data on up to 25 companies               | Bulk data credits     |
| Enrich Contacts            | Comprehensive profiles for up to 25 contacts                   | Bulk data credits     |
| Find Similar Companies     | Discover companies with comparable profiles                    | Free                  |
| Find Similar Contacts      | Locate contacts with matching characteristics                  | Free                  |
| Find Recommended Contacts  | Sales-ready contacts for target accounts                       | Free                  |
| Search Intent              | Uncover companies exhibiting buying activity signals           | Free                  |
| Enrich Intent              | Buying signals for identified companies                        | Bulk data credits     |
| Search Scoops              | Companies experiencing notable business events                 | Free                  |
| Enrich Scoops              | Detailed event information for known companies                 | Bulk data credits     |
| Enrich News                | Categorized news coverage by company                           | Bulk data credits     |

### Context Agents (2)

| Agent             | Purpose                                                | Cost               |
| ----------------- | ------------------------------------------------------ | ------------------ |
| Account Research  | Generate comprehensive company intelligence briefing   | AI action credits  |
| Contact Research  | Produce full contact intelligence briefing             | AI action credits  |

## Authentication & Security

- **User-level authentication** with ZoomInfo credentials for personalized tooling and individual context
- **App-level authentication** available for enterprise teams that need centralized credential management
- **Entitlement enforcement** at the access level: MCP queries respect the user's existing ZoomInfo permissions and data scopes
- Data handling, scope, and audit details documented at [gtm.ai/docs/mcp/security](https://gtm.ai/docs/mcp/security)

## Credits & Billing

- **Free to start with consumption credits based on usage** (canonical ZoomInfo pricing statement; per `brand_guidelines.md` PRICE-01)
- **Bulk data credits** consumed by enrichment and detailed-data tools (Enrich Companies, Enrich Contacts, Enrich Intent, Enrich Scoops, Enrich News)
- **AI action credits** consumed by Context Agents (Account Research, Contact Research)
- Search and lookup tools are free
- Recurring monthly credit allocations are not compatible with MCP; bulk data credits must be enabled on the account

**Required:** Active ZoomInfo subscription (Sales, Copilot, Studio, or ZI Lite) with bulk data credits enabled.

## Documentation Reference

The canonical product docs live at [gtm.ai/docs/mcp](https://gtm.ai/docs/mcp) with these sub-sections:

| Sub-page                                                                | Use it when content needs                                                        |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [Getting Started](https://gtm.ai/docs/mcp/getting-started)              | Pre-connect requirements, account prerequisites                                   |
| [Clients](https://gtm.ai/docs/mcp/clients)                              | Setup steps for Claude, ChatGPT, and custom MCP clients                          |
| [Tools](https://gtm.ai/docs/mcp/tools)                                  | Tool-by-tool functionality, parameters, and credit cost                          |
| [Security & Data](https://gtm.ai/docs/mcp/security)                     | Authentication model, entitlements, data handling                                 |
| Credits & Billing (within docs index)                                   | Bulk data vs. AI action credits, admin credit-limit configuration                 |
| FAQ & Troubleshooting (within docs index)                               | Common error resolution and AI-client connection issues                          |

## Connected Products

- [[gtm-context-graph|GTM Context Graph]] — MCP is the API access lane that exposes the graph to MCP-compatible AI clients; the 15 tools and 2 context agents above are the surface area through which Claude, ChatGPT, and custom agents query the graph
- [[chorus|Chorus]] — conversation intelligence data feeds graph context that MCP tools can return
- [[intent-data|Intent Data]] — surfaced through Search Intent and Enrich Intent tools
- [[data|ZoomInfo Data Platform]] — the verified B2B data foundation MCP queries

## Case Studies Using This Product

_See linked case studies in graph view._ Customer outcomes attributed to AI agent grounding, custom MCP client builds, or "AI research grounded in verified data" trace back to this product.
