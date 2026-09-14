---
name: folder-structure
description: >-
  Conventional repository layout for application code, tests, and docs so TestRail
  suites and components can be named consistently and linked to areas of the codebase.
---

# Folder structure (reference)

> Adjust names to your monorepo or polyrepo strategy. This is a **default template** for aligning **TestRail sections** with **repo areas**.

## Typical application repo

```text
src/                    # Production code (language-specific)
tests/
  unit/                 # Fast, isolated tests
  integration/          # DB/API/component boundaries
  e2e/                  # Browser or full-stack journeys
docs/
  requirements/         # Optional: imported specs
scripts/                # Tooling, codegen, local only
```

## Mapping to TestRail

- **Project** ↔ product or major initiative.
- **Suite** ↔ release train, milestone, or regression cycle.
- **Section** ↔ top-level folder or bounded context (`billing`, `auth`, `reporting`).
- **Case** ↔ feature slice or user journey within that section.

## Naming

- Mirror **two** levels of path in section names if helpful: `src/auth - Login` vs deep file paths (avoid noise).
- For microservices, prefix with service name: `[payments-api] Refunds`.

## Docs and requirements

- Store authoritative **acceptance criteria** where your team looks first (Jira, Confluence, repo). TestRail should **link** there, not duplicate paragraphs.

## LLM usage

When generating cases from requirements, use this skill to **propose section names** and **component tags** that match your repo layout so manual testers can find related code.
