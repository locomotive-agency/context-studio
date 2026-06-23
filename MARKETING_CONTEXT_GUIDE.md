# Structuring Marketing Context for AI Work

Marketing teams have always worked from context: positioning, audience research, campaign plans, product facts, proof points, channel constraints, brand standards, performance data, and the judgment people build from doing the work.

AI changes the cost of using that context. A person can notice when a source looks old, when a claim feels too strong, or when a campaign note should not override the brand strategy. An AI workflow needs those distinctions made explicit. Otherwise it treats a brainstorm, a product fact, a legal disclaimer, and a performance learning as variations of the same thing: text that might be relevant.

That is not enough for repeatable marketing work.

The goal is to build a practical context system that knows how different kinds of marketing knowledge should behave. Some context can be loose and searchable. Some needs review before it becomes approved. Some must be traceable to an approved source. The system should become more deterministic as the cost of being wrong rises with scale.

The architectural pattern is platform-agnostic. The examples use Claude Code plugins and Anthropic Connectors as reference implementations because they provide concrete models for skills, plugin packaging, tool access, and connector-based retrieval.

## The Basic Vocabulary

Marketing teams need a shared vocabulary before they can build reliable AI workflows. The same word often gets used for a team, a process, an artifact, a source, and an instruction. Those are different objects, and the system should treat them differently.

**Functional areas** are categories of work: strategy, research, design, content, development, communication, data, analysis, and planning.

**Processes** are repeatable sequences that turn inputs into outputs. A product page refresh, content gap analysis, campaign launch, and monthly reporting cycle are processes. Each may involve several functional areas.

**Deliverables** are the artifacts those processes produce. A user journey map, information architecture, messaging matrix, content calendar, or campaign brief is a deliverable.

**Context** is the knowledge a person or system uses to do the work. A deliverable may become context for later work, but it is not automatically canonical truth.

**Skills** are instructions for repeatable AI work. A skill should describe the process an agent follows, the context it needs, the tools it can use, and the output it should produce. It should not quietly become the only place where product facts, legal rules, or approved claims live.

**Outcome specs** define what good looks like. They may include a rubric, examples, review criteria, required citations, or performance measures.

For the system, the distinction matters operationally:

* Context says what is true, relevant, allowed, or required.  
* Skills say how to perform the work.  
* Outcome specs say how the result will be judged.

## Why Context Should Be Organized Around Work

If context is organized only by department, AI workflows inherit the same silos people already work around. Research has one set of documents. Content has another. Design has another. Legal has another. Analytics has another.

Most useful marketing work cuts across those boundaries.

A content gap analysis may need audience research, current product priorities, search data, competitive pages, customer journey stages, measurement goals, and the current content inventory. A campaign brief may need positioning, channel constraints, promotion dates, proof points, creative direction, and past performance. A service-line page may need brand voice, provider data, compliance rules, patient concerns, and approved claims.

The context system should therefore support processes and deliverables, not just folders and teams. It should help assemble the context needed for a task, with enough governance to know which parts are flexible and which parts are not.

## The Useful Axes

Every piece of marketing context can be classified across a focused set of axes:

* **Construct**: The marketing category the context belongs to (e.g., brand messaging, audience profile, product offering).  
* **Scope**: Where the context applies within the organizational hierarchy.  
* **Durability**: How long the context remains useful and valid.  
* **Criticality**: The operating band (Flexible, Hybrid, or Controlled) that dictates retrieval and governance rigor based on risk.

These axes give the system enough information to decide how context should be retrieved, governed, and used.

### Construct

The construct is the marketing category the context belongs to.

| Construct | What It Covers |
| :---- | :---- |
| Audience Profile | Target audience, needs, motivations, decision criteria, segments |
| Brand Messaging | Positioning, tagline, brand essence, purpose, differentiation |
| Business Goals | Commercial objectives marketing should support |
| Communication Preferences | Format, cadence, channel, stakeholder, or customer preferences |
| Competitive Landscape | Competitors, market dynamics, positioning, category signals |
| Customer Journey | Stages, questions, objections, conversion moments, content needs |
| How We Look | Visual identity, logo, color, typography, imagery, design principles |
| How We Sound | Voice, tone, personality, spoken and written character |
| How We Write | Editorial standards, grammar, formatting, structure, writing mechanics |
| Legal and Compliance | Regulatory requirements, disclosures, trademarks, approval processes |
| Measurement and KPIs | Funnel metrics, attribution rules, targets, benchmarks |
| Product and Offering | Features, packaging, pricing, availability, plans, service details |
| Proof Points | Case studies, testimonials, awards, certifications, metrics |
| Tech Stack | CMS, analytics, CRM, publishing, workflow, data and measurement tools |
| Use Cases and Solutions | Jobs-to-be-done, scenarios, industries, solution mapping |
| Value Proposition | Why the offer matters and what value it delivers |

These constructs should stay focused on marketing knowledge. Operating details such as approval state, source authority, inheritance, and retrieval behavior are better handled through minimal metadata and workflow rules.

### Scope

Scope defines where the context applies. Context is assigned to a specific hierarchy member. Precedence and inheritance flow upward through parent relationships in the hierarchy. This means context is inherited from the parent and the parent's parent, with priority given to the most granular context in the chain (meaning more specific context overrides broader context for the same construct).

A simple hierarchy might look like this:

```
Company
  Brand A
    Product A
      Campaign A1
      Campaign A2
    Product B
  Brand B
    Product C
```

In this structure:

* Product A inherits context from Brand A and Company.  
* Context assigned directly to Product A overrides context from Brand A and Company for the same construct.  
* Priority is always given to the most granular level in the inheritance chain.

### Durability

Durability defines how long context remains useful and valid.

| Durability | Examples | Handling |
| :---- | :---- | :---- |
| Ephemeral | Draft notes, brainstorms, one-session assumptions | Keep transient, no long-term storage or formal tracking required |
| Time-bound | Campaign briefs, promotions, event details, current-state notes | Require dates and expiry |
| Persistent | Journey maps, research synthesis, approved positioning, product facts | Require version control, source citation, and periodic review |

Durability and risk are different. A short-lived promotion can be controlled. A persistent writing preference can be hybrid.

### Criticality

Criticality defines the governance rigor and retrieval mechanisms based on the risk associated with incorrect context. Rather than utilizing a complex scoring system, the service classifies context into three distinct operating bands—Flexible, Hybrid, and Controlled—each with its own retrieval constraints and review requirements:

| Band | When It Applies | Examples | Retrieval Behavior | Governance |
| :---- | :---- | :---- | :---- | :---- |
| Flexible | A mistake is low-cost, or the context is being used for exploration | Brainstorms, rough notes, creative inspiration, early hypotheses | Retrieved dynamically via connectors, bespoke tooling, or semantic retrieval from unstructured data | Minimal governance, transient/ad-hoc tracking |
| Hybrid | The context is reused across work, affects quality, or needs scope and validity controls | Brand voice, audience profiles, journey maps, campaign briefs, active promotions, reusable messaging | Context service lookup first, with supporting search allowed where useful | Status, version history, provenance, and expiry filters when time-bound |
| Controlled | The context can create legal, commercial, reputational, or customer-facing risk if wrong | Product facts, pricing, approved claims, comparative claims, legal disclosures, regulated language | Deterministic lookup from approved records; halt execution if required context is missing | Approval workflow, source provenance, version history, and service-level runtime audit where needed |

This gives the system practical retrieval behavior:

* **Flexible** context relies on semantic retrieval, system connectors, and ad-hoc query tools.  
* **Hybrid** context combines structured context records with supporting sources retrieved via connectors and semantic search.  
* **Controlled** context requires deterministic lookup from approved records and should halt execution if required context is missing.

## Provenance Metadata

Provenance is required metadata or frontmatter indicating the source of the context information. It specifies the URL, URI, or document name where the information originated. To ensure traceability and authority, URLs are preferred. Provenance metadata is required for any context that is derived from another source, enabling the context service to verify correctness and trace claims to their origin.

## Attention Should Follow Foundation And Risk

Marketing teams should not govern every note with the same rigor. Heavy processes everywhere makes the system unusable. No process around controlled context makes it unsafe.

The right level of governance depends on two questions:

1. How many workflows depend on this context?  
2. How much damage can it cause if it is wrong?

That creates a simple attention model.

| Attention Level | What Belongs Here | Examples | Management Attention |
| :---- | :---- | :---- | :---- |
| High | Controlled context and foundational constructs that influence many workflows | Legal and Compliance, approved claims, pricing, current product facts, core Value Proposition | Approval workflow, deterministic retrieval, version history, provenance, and service-level audit where needed |
| Medium | Shared context that guides repeated work but can tolerate some interpretation | Brand Messaging, How We Sound, How We Write, Audience Profile, Customer Journey, Use Cases and Solutions | Approved status, canonical version, citations, and validity dates where relevant |
| Low | Local, temporal, or exploratory context | Campaign briefs, active promotions, content calendars, brainstorms, rough notes | Status and expiry where needed, semantic retrieval allowed, promote only after review |

This is where management effort should concentrate: foundational constructs that influence many outputs, and controlled constructs that create material risk.

## The System: A Context Service With Governed Records

The system needs to solve a practical problem: skills initiate context needs, people have to add and maintain the context those skills depend on, and AI workflows have to retrieve the right context without guessing which source is authoritative.

The right center of gravity is a **context service**. It is not just a wiki and it is not just retrieval-augmented generation (RAG). It is the layer that knows:

* Who is asking.  
* What role and permissions they have.  
* Which context is governed and approved.  
* Which source systems may contain supporting material.  
* Which retrieval method fits the criticality of the request.  
* Which missing context should block the workflow.  
* Which record versions were used in each AI execution.

The context service should return a **context package** to the AI workflow. The package should stay minimal: approved records, source/provenance links, missing-context blocks, record identifiers, content hashes, and the bundle Git SHA.

The operating model looks like this:

```
User + Skill Request
  -> Context Service
  -> Permission Check
  -> Governed Context Lookup
  -> Known Source Lookup
  -> Connector Search, if allowed
  -> Context Package
  -> Skill Execution
```

This makes retrieval progressive. The system should not jump straight to broad search. It should first check whether the needed context is already governed.

## The Progressive Retrieval Path

The context service should follow the same retrieval path every time.

1. **Check the governed context store.** If the request needs hybrid or controlled context, the service checks approved records first.  
2. **Check known source locations.** If the approved record points to a source document, dataset, or source system, the service can return that provenance link or request a connector lookup.  
3. **Use connector search only when appropriate.** If the context is flexible, or if hybrid context needs supporting evidence, the workflow can search connected systems such as Google Drive, Microsoft 365, Slack, Notion, GitHub, or another available connector.  
4. **Block when controlled context is missing.** If the workflow needs controlled context and no approved record exists, the service should return a missing-context issue, not ask the model to infer the answer.  
5. **Create an update path.** If the user has the right role, the workflow can propose a new or updated record. If not, it can create a review request in the CMS.

Claude connectors matter here because they already give Claude access to common work systems. Anthropic's connector documentation says connectors let Claude access apps and services, retrieve data, and take actions within connected services. It also states that Claude inherits each person's permissions from the connected service, so a connector cannot reach a file, channel, or record the user cannot access ([Claude Connectors](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)). For Google Workspace, Claude can search and retrieve Google Docs, read Sheets, Slides, PDFs, images, and Microsoft Office files, and view file permissions and recent Drive changes ([Google Workspace Connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)).

That means a separate indexing system is not always necessary. Claude's native connectors can often cover flexible lookup. The context service only needs to know when connector search is allowed and what query, location, or provenance link to use.

## Where Each Kind Of Context Lives

The storage model should follow the criticality model.

| Context Type | Where It Should Live | How It Is Retrieved | Editing And Governance |
| :---- | :---- | :---- | :---- |
| Flexible | Existing work systems such as Drive, Notion, Slack, GitHub, Microsoft 365, another connected document system, or local project files | Connector search through the user's authorized tools | Usually no formal review. Promote only when the material becomes reusable |
| Hybrid | Context records in the documentation layer, backed by version-controlled files or database records | Context service lookup first, connector search only for supporting evidence | Status, version history, provenance, and expiry when time-bound |
| Controlled | Approved context records with minimal governance metadata and source provenance | Deterministic lookup from approved records; block when required context is missing | Role-based edit rights, approval workflow, version history, and service-level runtime audit where needed |

This is the main distinction: flexible context can remain where people already work. Hybrid and controlled context need a place where people can review and edit records deliberately.

## The Documentation Layer

The documentation layer has to do more than present content. People need a real interface for reviewing and editing context. Many users will not want to work directly in Git or through an AI chat.

To keep the system simple and intuitive, the system uses a custom **Astro \+ Git-backed CMS** as its documentation and editing layer:

* **Git-Backed File Store**: Context records (JSON or Markdown files) are stored directly on the file system, utilizing Git for all change tracking, history, and version control.  
* **Responsive Web Portal**: Built with Astro, the portal provides non-technical users with a clean, visual interface to browse schemas, review change history, and edit documents.  
* **SQLite for State and RBAC**: A lightweight local SQLite database handles user accounts, sessions, and Role-Based Access Control (RBAC) validations, separating active system state from the document store.  
* **Auditable Git Commits**: Saving changes via the CMS automatically commits modifications to the local Git repository under the editing user's identity, creating a complete Git history.

The architecture pattern is:

```
Astro CMS & Web UI (RBAC)
  <-> Git-backed local file repository (JSON/Markdown)
  -> Context Service (MCP)
  -> AI skills and plugins
```

## Core Components

To keep the system as simple and intuitive as possible, the architecture consists of five core components:

1. **OKF Document Database**: A document database of Open Knowledge Format (OKF) records, stored either as flat files or in a database.  
2. **Schema Model**: A schema definition that maps metadata models to document types, controlling the context axes, governance, and access control.  
3. **Simple CMS**: A web-based content management interface supporting Role-Based Access Control (RBAC) for editing and managing records.  
4. **Context Service (MCP)**: A service that runs the Model Model Protocol (MCP) server, handling client requests to retrieve and manage context.  
5. **Semantic Retrieval Service**: A service that acts as a semantic retrieval layer for buckets of unstructured data (e.g. raw docs or competitor wikis).

The architecture and request flow looks like this:

```
Skill mentions context
  -> Context Service (MCP) runs permission check
  -> Context Service checks Schema Model to resolve access, axes, and retrieval behavior
  -> Context Service retrieves OKF record from the OKF Document Database
  -> Context Service queries Semantic Retrieval Service if unstructured data is allowed
  -> Context Package is returned to the executing skill
```

### Schema Database

The schema database is the part that keeps the system from becoming a loose wiki. It defines which fields each context type requires and how the context service should retrieve it.

For example, a controlled product fact needs status, criticality, scope, provenance, and version history. A hybrid audience summary may need scope, provenance, status, and a `valid_until` date if it is time-bound. A flexible note may only need optional tags or a source location.

A Pydantic-style schema could look like this:

```py
from datetime import date
from typing import Literal
from pydantic import BaseModel


class ContextRecord(BaseModel):
    id: str
    title: str
    type: str
    description: str = ""
    scope_id: str | None = None
    durability: Literal["ephemeral", "time_bound", "persistent"] = "persistent"
    provenance: str | None = None  # URL, URI, or document name of the source (required if derived)
    criticality: Literal["flexible", "hybrid", "controlled"] = "hybrid"
    edit_roles: list[str] = []
    status: Literal["draft", "proposed", "approved", "archived"] = "approved"
    valid_until: date | None = None
    resource: str | None = None
    tags: list[str] = []
```

The schema database should be the source of truth for how a context record behaves. Skills should not decide whether `product-offering` is controlled or whether `legal-and-compliance` needs deterministic retrieval. The context record and schema should decide that.

Governance metadata should stay minimal. Do not add `owner_role`, `approver_role`, `audit_required`, `source_refs`, `retrieval_policy`, `exact_language_required`, or similar per-record workflow fields back into the model. Use the existing axes: `criticality`, `status`, `durability`, `scope_id`, `provenance`, `valid_until`, and `edit_roles` only if lightweight folder or document edit hints are still useful.

Runtime audit should be service behavior, not per-record metadata. Git history tells us what changed in the record. If the service needs to record which AI execution used which controlled record version, that belongs in an application-level audit log keyed by runtime use, not in the OKF document frontmatter.

### Context Records

Context records must conform to the **Open Knowledge Format (OKF)** specification ([OKF SPEC](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/2d0bb3f547b847fcbd1c7611bdab8a9e2ccb098f/okf/SPEC.md)), which structures metadata attributes and frontmatter to ensure that context remains machine-readable, auditable, and easily parsed. Each hybrid or controlled record includes metadata and a body:

```
id: ctx.product-a-pricing.2026-06
title: Product A pricing
type: product-offering
scope_id: product-a-us
durability: persistent
provenance: https://drive.google.com/example
criticality: controlled
edit_roles:
  - revenue-ops
status: approved
```

These records do two jobs. They give humans a documented source of truth, and they give the context service enough structure to make retrieval decisions.

### Context Editing And Update Skills

Context editing and updates must support a range of contribution workflows governed by Role-Based Access Control (RBAC). These actions can be performed via:

* **CMS integrations**: Direct web-based content management interfaces.  
* **File editing**: Direct file-level edits in the repository (e.g. Markdown or JSON).  
* **MCP Tools with RBAC validation**: Remote agent tool executions that check user permissions prior to writing changes.

Updating context remains a governed process rather than an open-ended chat command. The editing skill should:

1. Validate the user's role and check editing permissions.  
2. Structure new drafts or updates.  
3. Validate metadata attributes against the OKF schema.  
4. Route controlled-context changes through the CMS review workflow based on the record's criticality and status.

## Skills, Plugins, And Context Are Separate

The process layer should live separately from the context layer.

Claude Code plugins are a good fit for packaging repeatable AI work. The Claude plugin documentation describes plugins as shareable extensions that can include skills, agents, hooks, MCP servers, executables, settings, and a `.claude-plugin/plugin.json` manifest. Skills live in `skills/<name>/SKILL.md`, agents live in `agents/`, MCP configuration can live in `.mcp.json`, and executables can live in `bin/` ([Claude Code Plugins](https://code.claude.com/docs/en/plugins)). Claude skills can also include supporting files such as references, examples, and scripts inside the skill directory ([Claude Code Skills](https://code.claude.com/docs/en/skills)).

The plugin repository should contain workflow instructions, templates, scripts, assets, agents, and tool requirements. It should not contain approved pricing, legal language, current product facts, or other governed context.

```
marketing-ai-plugins/
  product-marketing/
    .claude-plugin/
      plugin.json
    skills/
      product-page-refresh/
        SKILL.md
        resources/
          output-template.md
          review-checklist.md
        scripts/
          validate-brief.ts
    agents/
      product-marketing-reviewer.md
    bin/
      build-context-package
    .mcp.json
    README.md
```

The skill should mention context using the same labels used by the context system:

```
---
description: Refresh a product page using approved product, claim, brand, and compliance context.
context:
  - product-offering
  - value-proposition
  - proof-points
  - legal-and-compliance
  - how-we-sound
  - how-we-write
required_tools:
  - context.lookup
  - connector.google-drive
  - mcp.cms
---
```

Those labels are the important shared keys. The context system should maintain canonical labels and aliases so the phrasing in `SKILL.md` maps to the right context records. For example:

| Canonical Label | Common Aliases |
| :---- | :---- |
| `product-offering` | product facts, offer details, pricing, packaging |
| `legal-and-compliance` | disclosures, disclaimers, compliance rules |
| `how-we-sound` | voice, tone, tone of voice |
| `proof-points` | claims support, substantiation, evidence |

MCP handles tool access. Connectors handle source access where available. The context service decides which source or record should be used, checks whether the user can access it, and returns the package the skill needs.

### Where More Advanced Tools Fit

Pinecone Nexus is relevant if the team wants a managed context compiler rather than a local Git-centered workflow. It points in the same direction: compiled, task-specific knowledge for agents rather than raw chunk retrieval ([Pinecone Nexus](https://www.pinecone.io/blog/knowledge-infrastructure-for-agents/)). The default path should be to prove the operating model first with a local Astro CMS documentation layer, a governed context repository, connector-aware retrieval, and a lightweight context service.

GraphRAG belongs later. It can help when the relationship model becomes difficult to manage with metadata alone, or when baseline retrieval misses relationships across documents. Microsoft describes GraphRAG as extracting entities, relationships, claims, and community summaries from source text, then using those structures at query time ([Microsoft GraphRAG](https://microsoft.github.io/graphrag/)). It should support compiled context, not replace it.

## Examples

### Healthcare Landing Page

A hospital landing page mixes foundational and critical context.

| Context | Criticality | Retrieval |
| :---- | ----: | :---- |
| Required medical disclaimer | Controlled | Approved record |
| Provider and location facts | Controlled | Approved record |
| Service-line description | Controlled | Approved record |
| Proof points | Controlled | Approved record with substantiation |
| Brand voice | Hybrid | Hybrid retrieval |
| Patient journey | Hybrid | Hybrid retrieval |
| Draft creative ideas | Flexible | Semantic retrieval |

If the disclaimer or provider facts are missing, the workflow should stop.

### Seasonal Retail Campaign

A seasonal campaign can use lighter governance for most context, with stricter handling for offer details.

| Context | Criticality | Retrieval |
| :---- | ----: | :---- |
| Promotion dates | Controlled | Approved record |
| Discount rules | Controlled | Approved record |
| Brand voice | Hybrid | Hybrid retrieval |
| Campaign brief | Hybrid | Scoped retrieval with expiry |
| Past campaign learnings | Hybrid | Hybrid retrieval with recency filter |
| Brainstorm concepts | Flexible | Semantic retrieval |

The campaign brief should expire. It should not become durable brand truth.

### SaaS Competitive Page

A competitive page needs to separate external observation from company claims.

| Context | Criticality | Retrieval |
| :---- | ----: | :---- |
| Current product facts | Controlled | Approved record |
| Pricing and packaging | Controlled | Approved record |
| Competitor website statements | Hybrid | Source-cited retrieval |
| Approved comparative claims | Controlled | Approved record |
| Proof points | Controlled | Approved record with substantiation |
| Messaging hypotheses | Flexible | Semantic retrieval |

"The competitor says X" and "we claim X about the competitor" are different objects. They need different governance.

## Implementation Path

Start with the highest-value foundation, not the whole organization.

### Phase 1: Classify The Foundation

Prioritize the constructs that influence many workflows or carry meaningful risk:

* Legal and Compliance.  
* Product and Offering.  
* Value Proposition.  
* Brand Messaging.  
* Proof Points.  
* How We Sound.  
* How We Write.  
* Audience Profile.

Assign scope, durability, provenance, criticality, status, and validity dates where needed.

### Phase 2: Build The First Registry

Create a lightweight registry that supports:

* Context records.  
* Version history.  
* Source links.  
* Scope filtering.  
* Validity dates.  
* Criticality bands.  
* Deterministic retrieval for approved records.  
* Semantic retrieval for low-risk material.

A structured repository or lightweight database is enough to test the model.

### Phase 3: Connect One Workflow

Pick one repeatable task:

* Product page refresh.  
* Content brief generation.  
* Content gap analysis.  
* Campaign brief synthesis.  
* Approved claim lookup.

Build the context package, write the skill, define the review gate, and run real examples.

### Phase 4: Evaluate

Track:

* Did the workflow retrieve the right context?  
* Did it avoid expired or unapproved context?  
* Did it cite sources where needed?  
* Did it block when critical context was missing?  
* Did review time go down?  
* Did reviewers trust the result more than plain retrieval?

RAG evaluation work increasingly separates retrieval, generation, safety, and efficiency rather than treating the system as one black box ([RAG Evaluation Survey](https://arxiv.org/html/2504.14891v1)). Marketing workflows should do the same.

## Design Principles

1. Keep the marketing construct taxonomy focused.  
2. Use minimal metadata for criticality, status, durability, scope, provenance, and validity dates.  
3. Let criticality drive retrieval.  
4. Keep low-risk context lightweight.  
5. Make high-risk context deterministic and traceable.  
6. Treat temporal context as expiring by default.  
7. Treat external sources as evidence, not truth.  
8. Promote outcome learnings deliberately.  
9. Block when critical context is missing.  
10. Give skills context packages, not open-ended document search.

## Closing

Marketing context should not be forced into one rigid shape. The system should be flexible where the work is exploratory and strict where mistakes matter.

That means semantic retrieval for low-risk material, hybrid retrieval for reusable foundational context, deterministic lookup for approved facts and claims, and blocking when required controlled context is missing.

The result is a practical middle ground: one context layer that can support creative work, repeatable workflows, and high-governance marketing without treating every note like a legal disclosure or every legal disclosure like a note.

## Sources

* [Pinecone Nexus: The Knowledge Engine for Agents](https://www.pinecone.io/blog/knowledge-infrastructure-for-agents/)  
* [Microsoft GraphRAG](https://microsoft.github.io/graphrag/)  
* [Claude Code Plugins](https://code.claude.com/docs/en/plugins)  
* [Claude Code Skills](https://code.claude.com/docs/en/skills)  
* [Claude Connectors](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)  
* [Google Workspace Connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)  
* [RAG Evaluation Survey](https://arxiv.org/html/2504.14891v1)  
* [LangExtract](https://github.com/google/langextract)  
* [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)  
* [GitHub Docs: About Git](https://docs.github.com/en/get-started/using-git/about-git)  
* [GitHub Repository Roles](https://docs.github.com/organizations/managing-user-access-to-your-organizations-repositories/repository-roles-for-an-organization)  
* [GitHub Protected Branches](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

