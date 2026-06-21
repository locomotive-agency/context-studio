# Development Governance

This file defines how we build the project. Architecture and product requirements belong in the roadmap and sprint docs.

## Principles

- Prefer the simplest useful design.
- Solve the user's actual workflow before adding configuration.
- Keep concepts separate when merging them would create confusion.
- Do not add fields, screens, or workflows unless they remove real work for the user.
- Avoid clever abstractions until repeated code proves they are needed.
- Use plain language in UI and docs.

## Engineering Standards

- Follow the existing repo patterns before introducing new structure.
- Keep changes small and focused.
- Use typed request and response models at API boundaries.
- Validate inputs at the edge of the system and return clear errors.
- Keep business rules in services, persistence in repositories, and UI formatting in the UI.
- Prefer deterministic behavior when the data model supports it.
- Make configuration explicit and fail fast when required settings are missing.
- Do not fix symptoms while leaving the source problem intact.
- When something fails, find the root cause, write down the evidence, and resolve that cause directly.
- Prefer one clear source fix over patches spread across callers, UI guards, or retry logic.
- Never store secrets in source files, fixtures, docs, or logs.
- Add RBAC checks anywhere data leaves the system or an external tool can be invoked.

## Testing Standards

- Use TDD for new behavior when practical: failing test, minimal implementation, passing test.
- Add regression tests for every bug fix.
- Test user-visible behavior, not private implementation details.
- Cover security and permission rules directly.
- Keep fixtures small and readable.
- Do not mark work complete until the relevant tests or checks have been run in the current session.

## Code Quality

- DRY means remove meaningful duplication, not force everything through one abstraction.
- YAGNI applies by default.
- Prefer boring, readable code over framework tricks.
- Name things after the user's domain language.
- Keep modules focused enough that a reviewer can understand the change without reading the whole app.
- Comments should explain non-obvious decisions, not restate the code.

## Product Discipline

- Do not make users approve or configure hundreds of items one at a time.
- Do not add summarization, generation, or automation features unless the product requirement explicitly asks for them.
- Do not resurrect previously rejected complexity under a new name.
- When a decision is uncertain, write down the tradeoff before implementing it.
- Favor workflows that let users inspect the real system behavior, not mock previews.

## Review Checklist

Before merging a change, verify:

- The change solves the stated user problem.
- The simplest reasonable design was used.
- Tests or checks were run and their results are known.
- Security, RBAC, and error states were considered.
- User-facing text is plain and accurate.
- No unrelated refactors or metadata churn were included.
