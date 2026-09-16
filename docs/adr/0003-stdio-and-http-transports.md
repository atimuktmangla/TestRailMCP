# ADR-0003: stdio + Streamable HTTP transports

**Status:** Accepted

## Context

MCP clients connect differently: many spawn a subprocess (stdio); others prefer
a URL (Streamable HTTP). The server should serve both from one package without
duplicating the tool surface.

## Decision

Support both transports, selected by `TESTRAIL_MCP_TRANSPORT` (`settings.py`):
**stdio** (default) and **Streamable HTTP** (Starlette at
`HTTP_HOST:HTTP_PORT + HTTP_PATH`, default `127.0.0.1:8765/mcp`, stateless by
default with an opt-in resumable mode). Both build the same `Server`, so the
tools are identical.

## Alternatives considered

- **stdio only.** The common default, but excludes URL-based clients and shared
  HTTP deployments.
- **HTTP only.** Excludes subprocess-only clients and complicates local use.

## Trade-offs

- (+) One codebase/tool surface serves every client shape.
- (+) Stateless HTTP is simple to scale; resumable is available when needed.
- (−) Two transport paths to maintain; HTTP should stay bound to localhost unless
  deliberately exposed.

## Consequences

- Transport is env-driven; the same `build_server` is used by both.
- HTTP defaults to `127.0.0.1` for safety.
