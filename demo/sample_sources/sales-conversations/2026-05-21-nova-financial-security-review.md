# Synthetic Sales Conversation: Nova Financial Security Review

Date: 2026-05-21
Account: Nova Financial Services
Segment: Regulated financial services
Participants: Daniel Brooks, VP Revenue Operations; Elena Ward, Governance Lead; Marcus Lee, Information Security; Jordan Lee, Seller

## Summary

Nova wants to use AI for account-specific sales plays but is concerned that generic retrieval will surface stale regulatory language, draft claims, or notes from unapproved research folders.

## Transcript Excerpt

Jordan: Where does the risk show up in the current workflow?

Elena: People paste whatever they can find into a prompt. Sometimes it is an approved statement. Sometimes it is a draft from a launch folder. Sometimes it is a transcript where a customer used language we cannot repeat.

Marcus: From a security standpoint, I care about login and auditability. If someone can hit an endpoint and retrieve context without being logged in, that is a nonstarter.

Daniel: My team does not need elaborate approvals inside the tool. We already know who can edit. Admins handle users. Editors maintain the content. Viewers consume the context. Please do not turn it into a workflow platform.

Jordan: How should semantic search fit?

Elena: Semantic search is useful over supporting sources. I want to ask, "What are buyers saying about stale context?" and get cited passages. But approved guidance needs to stay deterministic.

Marcus: I would also separate source pointers from tool invocation. Returning that a supporting MCP server exists is different from letting someone invoke a tool.

Daniel: For the demo, show me that a viewer can request a context package and that an editor can upload transcripts to a Collection. That is the heart of it.

## Buyer Language

- "Please do not turn it into a workflow platform."
- "Approved guidance needs to stay deterministic."
- "If someone can hit an endpoint and retrieve context without being logged in, that is a nonstarter."

## Useful Search Terms

regulated language, deterministic guidance, login requirement, semantic search, workflow platform, MCP server
