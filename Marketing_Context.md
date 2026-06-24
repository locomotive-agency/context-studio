# Marketing Context for AI

**What this is:** a determinism layer for the skills and agents your team builds. A skill tells the agent how to do the work and where to get information. The surfaces it reaches for that information (RAG, memory, connectors, MCP servers) are not deterministic. RAG in particular returns inconsistent results, and models cannot reliably tell good information from bad. For anything where being wrong is costly, that is the core problem.

This system solves it by putting the important information in one authoritative place, authored through a UX or as flat files in GitHub, and returning a governance signal to the agent: this is controlled, use the approved record and stop if it is missing, versus this is fine to pull from RAG or another MCP server as supporting data. It is a companion for skill determinism that works across the surfaces your team already uses for agentic work.

## The one mental model

Govern each piece of context by the cost of being wrong. Three bands set the agent's retrieval behavior:

- **Controlled:** legal, commercial, or reputational risk if wrong (product facts, pricing, approved claims, disclosures). The agent uses approved records only and blocks the workflow if the record is missing. No RAG, no guessing.
- **Hybrid:** reused and affects quality (brand voice, audience profiles, journey maps, campaign briefs). The agent starts from the structured record, then may use search or connectors for supporting detail.
- **Flexible:** low cost if wrong (brainstorms, rough notes, inspiration). RAG, search, and connectors are fine. Minimal governance.

This is the heart of it: the band tells the agent when determinism is required and when retrieval can stay loose.

## Separation of workflows and data

The context does not have to live on the same folder or machine as the skill. A skill or plugin directs the agent to this tool and to named constructs, and the agent always pulls the most up-to-date records. That separates workflows from data, with governance you can tune per construct: lock down what is controlled, leave exploration flexible.

## Other simple classifications

- **Construct:** the marketing category (Audience Profile, Brand Messaging, Product and Offering, Proof Points, Legal and Compliance, How We Sound, How We Write, and so on).
- **Scope:** where it applies (Company, Brand, Product, Campaign). The most specific level wins.
- **Durability:** ephemeral (drafts), time-bound (campaigns and promos, which expire), or persistent (positioning and product facts, which are versioned and reviewed).
- **Criticality:** the Controlled, Hybrid, or Flexible band above.
- **Provenance:** where it came from, a URL when possible.

## Where it lives

It can run on your computer or in the cloud. Authored through a UX or as flat files, it is designed to work with GitHub credentials, diffs, and version control, so teams get plain history of who changed what and when, behind an approachable editing process. The format is simple and extensible. Controlled and hybrid records live here. Flexible material can stay in the tools people already use, reached through RAG or connectors at runtime. What we provide is a prototype for you to build on top of.

## How it aligns with the Open Knowledge Format (OKF)

OKF is an open spec for human- and agent-readable knowledge: a directory of markdown files with YAML frontmatter, shipped as a git repo, with no required tooling or central registry. That is the same substrate this system uses for flat files in GitHub, so the two fit together cleanly. The mapping is direct:

- **Each context record is an OKF concept:** one markdown file, frontmatter on top, a human-readable body below. The "write the body for humans first" rule is OKF's guidance too.
- **The record fields are frontmatter.** Construct maps naturally to OKF's required `type`. Provenance maps to `resource` and a `# Citations` block. Scope, Status, Criticality, Durability, and Valid Until are producer-defined keys, which OKF explicitly allows and tells consumers to preserve.
- **Scope hierarchy is the directory tree.** Company, Brand, Product, and Campaign become nested folders, and bundle-relative markdown links express the relationships between records.
- **Progressive disclosure is OKF's `index.md`.** Reading a scoped inventory and metadata before opening full records is the index-first traversal OKF describes. Its optional `log.md` adds a plain-language change history on top of git.

What this system adds on top of OKF is governance and determinism. OKF is permissive by design: consumers tolerate unknown types, missing fields, and broken links, and do best-effort reads. That suits discovery, but it is the opposite of what controlled context needs. So the criticality band, status, and validity dates live as OKF frontmatter, and the retrieval policy reads them to decide when to use approved records only and block, versus when RAG or connectors are acceptable. OKF gives the portable, diffable format. This system gives the rules that make retrieval deterministic where it matters.
