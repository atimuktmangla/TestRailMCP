# Project Story — TestRailMCP

## Problem

Writing and maintaining TestRail test cases is repetitive manual work, and QA
teams increasingly want to do it from inside an AI coding assistant. But letting
an LLM touch a test-management system safely needs a **typed, bounded tool
surface** — not ad-hoc API calls — with a clear line between read and write
operations and no surprises.

## Solution

A **Model Context Protocol server for TestRail** that any MCP client (Cursor,
Claude, …) can drive to create and manage test cases:

- **Spec-driven tools** — TestRail's API v2 is exposed as MCP tools defined in
  `tools_spec.json` and routed generically; adding an endpoint is a spec edit.
- **Read/write safety** — every tool is annotated `readOnlyHint` (get_* = read,
  else write) so an agent knows the blast radius before calling.
- **Two transports** — stdio and Streamable HTTP, from one package.
- **Structured, error-safe results** — tool results carry structured content;
  failures return `isError` text, never an unhandled protocol throw.
- **Real distribution** — a wheel, a self-contained client ZIP + installer, and
  publisher-vs-end-user + wiki-ready docs, so non-technical users can install and
  point their client at it.

## Target users

- **QA / SDET teams** drafting and filing TestRail cases from an AI client.
- **As a portfolio piece:** a reviewer evaluating MCP design, safety annotation,
  and distribution polish.

## Architecture (why this shape)

A small Python package: transport (stdio/HTTP) → `server.py`
(list_tools/call_tool) → spec + generic routing → a thin TestRail HTTP client.
Decisions are recorded in [docs/adr/](docs/adr/); the AI/tool boundary is in
[docs/AI_ARCHITECTURE.md](docs/AI_ARCHITECTURE.md); see
[docs/architecture.mmd](docs/architecture.mmd).

## AI role (precise)

- **The LLM lives in the client**, not the server. "LLM-assisted test-case
  creation" means an AI client uses these tools; the server makes **no** LLM call.
- The server's value is the **contract**: a typed, spec-driven, read/write-
  annotated TestRail surface with structured results — deterministic and
  testable.

## Engineering value

- **Safe agent surface** — read/write annotation + structured errors make the
  tools usable by an autonomous client without foot-guns.
- **Maintainability** — spec-driven tools mean new endpoints don't add code paths.
- **Distribution** — wheel + client ZIP + wiki docs lower the barrier for real
  users.
- **Testable core** — the routing logic is pure and unit-tested (no network).

## Leadership value

Demonstrates MCP/tool-boundary design judgment — exposing an enterprise system to
AI **safely and maintainably** (data-driven tools, explicit read/write hints,
structured results) — plus attention to the last mile (distribution and docs for
non-technical users). It's "make AI usable against a real tool," not a demo.

> Example / reference implementation. No claim of production usage. The LLM is
> client-side; the server calls no model. TestRail credentials stay in a
> git-ignored `.env`.
