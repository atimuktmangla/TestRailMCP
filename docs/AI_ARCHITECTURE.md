# AI / Architecture

This document explains how AI relates to TestRailMCP and, precisely, where the
boundaries are. The short version: **the LLM lives in the MCP client** (Cursor,
Claude, …); this server is a **typed, spec-driven TestRail tool bridge** that
makes no LLM call itself.

> **One-line summary:** "LLM-assisted test-case creation" means an AI client uses
> these tools to draft and file TestRail cases. The server exposes TestRail's API
> v2 as MCP tools — each annotated read-only vs write — validates and routes the
> call, and returns structured results. It is deterministic and auditable.

---

## 1. Where the AI is (and isn't)

- **The model is the client's.** The AI in "LLM-assisted" runs in the MCP client;
  it decides what test cases to write and calls the server's tools to create
  them.
- **No LLM in the server.** This package makes no model call. Same tool + args →
  same TestRail request. That keeps the server testable (see `tests/`) and its
  behavior explainable.
- The value is the **tool boundary**: a complete, typed, safety-annotated TestRail
  surface an agent can use correctly.

---

## 2. Spec-driven tool surface

Tools are **data, not hand-written handlers**:

- `testrail_mcp/data/tools_spec.json` declares every tool (name, description,
  JSON-schema arguments).
- `handle_list_tools` emits them; `handle_call_tool` routes generically via
  `tool_suffix_to_api_method` + `build_request_from_spec` (`routing.py`).
- Adding a TestRail endpoint is a **spec edit**, not new code.

This is the defining design choice (ADR-0001): one routing path, uniformly
tested, instead of dozens of bespoke handlers.

---

## 3. Read vs write safety

Every tool carries an MCP `readOnlyHint` annotation, derived deterministically
from the API method (`get_*` → read-only, else write). An agent client can see,
before calling, which tools merely read TestRail (`get_case`, `get_cases`, …) and
which mutate it (`add_case`, `update_case`, `add_attachment_to_*`, …). This is a
real agent-safety signal for a server whose write tools create/modify test
artifacts (ADR-0002).

---

## 4. Transports

Selected by `TESTRAIL_MCP_TRANSPORT` (`settings.py`):

- **stdio** (default) — subprocess MCP for local clients.
- **Streamable HTTP** — Starlette endpoint at `HTTP_HOST:HTTP_PORT + HTTP_PATH`
  (default `127.0.0.1:8765/mcp`), stateless by default (one session per request;
  set `HTTP_STATELESS=false` for resumable sessions).

Same tool surface on both (ADR-0003).

---

## 5. Auth and data boundary

- **Credentials** — `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY`
  (HTTP Basic) via env / `.env` (git-ignored; only `.env.example` with
  placeholders is tracked). Typed and validated by pydantic-settings.
- **Localhost by default** for the HTTP transport.
- **Data flow** — the server calls *your* TestRail instance with *your* key and
  returns the results to the client; it does not transmit anything to a third
  party. The AI client decides what to do with the returned data, under your
  control. No LLM call originates in the server.

---

## 6. Failure handling

- Unknown tool → `isError` result naming the tool (no crash).
- Missing required path param or bad args → `ValueError` surfaced as an `isError`
  text result.
- Any client/TestRail error is caught and returned as a structured error, never an
  unhandled throw across the MCP protocol.
- Bare paginated GETs default to the API max page size (250) to avoid a known
  TestRail 500 on unbounded collections — a small reliability guardrail in
  `routing.py`.

---

## 7. Why this is "AI-ready," not "AI-inside"

The engineering is in the **contract**: a spec-driven, JSON-schema-typed,
read/write-annotated TestRail surface with structured results and deterministic
routing. That is exactly what lets an LLM client create test cases correctly and
safely — without the server needing a model of its own.
