# ADR-0002: Per-tool read-only annotation

**Status:** Accepted

## Context

This server exposes both read tools (`get_*`) and write tools (`add_*`,
`update_*`, attachment uploads) over TestRail. An autonomous MCP client should be
able to tell, before calling, which tools merely read versus which mutate test
artifacts — otherwise a model can't reason about blast radius.

## Decision

Annotate every tool with MCP `ToolAnnotations(readOnlyHint=...)`, derived
deterministically: `_tool_read_only` maps the tool name to its API method and
returns true when it starts with `get_`. The hint is emitted in
`handle_list_tools`.

## Alternatives considered

- **No annotation.** The client can't distinguish read from write except by
  guessing from names — worse for agent safety.
- **A hand-maintained allowlist.** Redundant with the `get_` convention and prone
  to drift; deriving from the method name stays in sync automatically.

## Trade-offs

- (+) Clients (and humans) see read vs write per tool, for free, always in sync.
- (−) Relies on TestRail's `get_`-prefix convention; a non-conforming method
  would need a special case (none today).

## Consequences

- The read-only classifier is a pure function and is unit-tested.
- Complements the structured `isError` results for safe agent use.
