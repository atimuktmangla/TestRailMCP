# Portfolio Notes — TestRailMCP

Internal notes on what this repository demonstrates and how to talk about it.
Honest framing only — no claims of usage the repo cannot support.

---

## Senior Engineering Manager signals

- **Enterprise-tool-to-AI bridge, done safely:** exposes TestRail to any MCP
  client with a typed, read/write-annotated tool surface — the kind of internal
  enablement layer a platform team ships.
- **Maintainability by design:** spec-driven tools (new endpoint = spec edit),
  one uniformly-tested routing path.
- **Last-mile focus:** wheel + client ZIP + installer + wiki-ready docs so
  non-technical users can actually adopt it.
- **Quality:** a pure-function routing core, now unit-tested, plus an e2e verify
  script and CI across Python 3.11/3.12/3.13.

## Architecture / MCP signals

- **Spec-driven tool registry** (`tools_spec.json` + generic `call_tool`).
- **Per-tool `readOnlyHint`** derived from the API method — agent-safety signal.
- **Structured results + `isError`** — clean, machine-readable envelope.
- **Two transports** (stdio + Streamable HTTP), typed pydantic settings, HTTP
  localhost-by-default.

## AI leadership signals

- **Honest scope:** the LLM is the client's; the server calls no model. The value
  is the contract, and the docs say so.
- **Safe writes:** the server has real write tools (create/update cases,
  attachments) but annotates them and returns structured errors, so an agent can
  reason about and recover from them.

---

## Interview discussion points

Eight questions a senior interviewer might ask, with the trade-off and a direction.

### 1. Is there an LLM in this server?
- **Direction:** no — the model is in the MCP client. This server is a typed
  TestRail tool bridge; "LLM-assisted" describes the client using the tools.
  (AI_ARCHITECTURE.md)

### 2. Why spec-driven tools instead of a handler per endpoint?
- **Direction:** TestRail has many endpoints; one generic routing path (name →
  method, build request) is uniformly testable, and new tools are spec edits, not
  new code. (ADR-0001)

### 3. How does an agent know which tools are safe to call?
- **Direction:** every tool carries a `readOnlyHint` derived from the API method
  (`get_*` = read, else write), so the client sees read vs write before calling.
  (ADR-0002)

### 4. How do you test something that talks to TestRail?
- **Direction:** the routing logic is pure — name mapping, method inference,
  path-key ordering, request building, URL rendering — and is unit-tested with no
  network; an e2e verify script covers the in-process MCP path.

### 5. Why support both stdio and HTTP?
- **Direction:** subprocess clients want stdio; URL/shared clients want Streamable
  HTTP; one package serves both with the same tool surface, HTTP stateless by
  default. (ADR-0003)

### 6. How are credentials handled?
- **Direction:** `TESTRAIL_URL/USER/API_KEY` via env/`.env` (git-ignored, typed by
  pydantic-settings); HTTP Basic to your instance; the server transmits nothing to
  third parties and calls no LLM.

### 7. Why ship a wheel and a client ZIP?
- **Direction:** two audiences — developers (wheel/PyPI) and end users who want a
  one-page install with no repo (client ZIP + installer + self-contained guide).
  The generated bundles are git-ignored, not committed. (ADR-0004)

### 8. What would you improve next?
- **Direction (honest):** expand tests beyond routing (client error mapping,
  server list/call paths), and consider generating the spec from TestRail's API
  reference to reduce drift.

---

## Strongest interview stories (rank order)

1. **Spec-driven MCP tool surface** — data-defined tools + one tested routing
   path; safe, maintainable enterprise-tool exposure.
2. **Read/write safety annotation** — agent-aware blast-radius signalling.
3. **Distribution polish** — wheel + client ZIP + wiki docs for real adoption.
4. **Testable pure core** — routing unit-tested with no network.
5. **Honest AI framing** — LLM is client-side; the server is the contract.

## Honest gaps (say these before you're asked)

- Test coverage started with the routing core; client/server paths are next.
- The tool spec is hand-maintained (could be generated from TestRail's API ref).
- "LLM-assisted" is a client capability, not a server-side model call.
