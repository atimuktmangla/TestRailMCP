# ADR-0001: Spec-driven tools over hand-written handlers

**Status:** Accepted

## Context

TestRail's API v2 has many endpoints (cases, sections, runs, plans, results,
attachments, users, …). Writing and maintaining a bespoke MCP handler per
endpoint is repetitive and drifts: each handler re-implements name→method
mapping, path/query building, and error handling.

## Decision

Define tools as **data** in `testrail_mcp/data/tools_spec.json` (name,
description, JSON-schema arguments). `handle_list_tools` emits them and
`handle_call_tool` routes generically through `tool_suffix_to_api_method` +
`build_request_from_spec` (`routing.py`). Adding an endpoint is a spec edit.

## Alternatives considered

- **One handler per endpoint.** Explicit but repetitive; every handler duplicates
  routing/validation and is a place for bugs.
- **Codegen handlers from the spec.** More moving parts than routing generically
  at call time; the generic router is simpler and equally uniform.

## Trade-offs

- (+) One routing path, uniformly unit-tested (`tests/test_routing.py`).
- (+) New tools = spec edits; no new code paths to review.
- (−) The generic router must handle special cases (e.g.
  `update_cases_by_case_id`, attachments) explicitly — but in one place.

## Consequences

- The routing functions are pure and testable without network/TestRail.
- Tool metadata (incl. read-only hints) is derived consistently from the spec.
