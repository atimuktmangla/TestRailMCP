---
name: coding-guidelines
description: >-
  Lightweight engineering conventions that improve testability—naming, errors,
  logging, and boundaries—so generated TestRail cases can reference stable hooks
  and failure modes. Adapt names to your stack.
---

# Coding guidelines (for testability)

## General

- **Single responsibility**: functions small enough to describe in one test title.
- **Explicit errors**: domain errors vs validation vs infrastructure; cases should assert user-visible or API-contract behavior per layer.
- **No silent failures**: avoid bare `except`; log context (request id, correlation id) without secrets.

## Naming

- **Modules**: noun or feature area (`billing`, `auth`).
- **Tests mirror source**: `test_<unit>_<behavior>()` maps cleanly to TestRail titles if you sync naming conventions.

## APIs

- **Versioned paths** or backward-compatible changes; document breaking changes in release notes—link from related TestRail **Regression** suites.
- **Idempotency keys** for mutating operations when applicable; cases should cover duplicate submission behavior.

## UI

- Prefer **accessible selectors** for automation (`data-testid` agreed with QA).
- Loading and error states must be reachable in cases (skeleton, empty, error banner).

## Security in code review (feeds test ideas)

- Validate input at boundaries; encode output in templates; parameterized queries only.

## How this skill helps LLM-generated cases

When requirements are vague, infer **test surfaces** from these rules: error handling paths, logging/audit expectations, and role-separated code paths—turn them into explicit TestRail steps.
