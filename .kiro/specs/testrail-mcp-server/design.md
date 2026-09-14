# Design: TestRail MCP Server

## Overview

The TestRail MCP Server is a thin, declarative bridge from MCP tool calls to TestRail REST
API v2 HTTP requests. The design goal is that adding or changing a TestRail operation is a
data change (edit `tools_spec.json`) rather than a code change: the server, routing, and
client are generic and driven by the spec.

Request flow:

```
MCP client (Kiro / agent)
        | list_tools / call_tool
        v
  server.py  (build_server)         -- loads spec, exposes tools, dispatches
        |  (tool name, arguments)
        v
  routing.py (build_request_from_spec) -- name -> api_method, args -> PreparedRequest
        |  PreparedRequest
        v
  client.py  (TestRailClient.execute)  -- httpx call, auth, response/error handling
        |  HTTP (Basic auth)
        v
   TestRail REST API v2
```

Transport is selected in `__main__.py`: stdio (default) or Streamable HTTP
(`http_transport.py`). Both wrap the same `Server` object, so tool behavior is identical
across transports.

## Architecture

### Components

| Module | Responsibility |
|--------|----------------|
| `settings.py` | Env-backed configuration (`TESTRAIL_*`), validation, timeouts, transport selection. |
| `data/tools_spec.json` | Declarative catalog of all 90 tools: name, description, JSON-schema arguments, required list. |
| `routing.py` | Pure functions: tool-name -> api_method, HTTP method inference, path/query/body assembly, pagination defaults. Produces `PreparedRequest`. No I/O. |
| `client.py` | `TestRailClient` wraps `httpx.AsyncClient`; executes a `PreparedRequest`, handles auth, multipart uploads, binary responses, and non-2xx errors (all 2xx are success). |
| `server.py` | Loads spec, builds the MCP `Server`, implements `list_tools` and `call_tool`, maps results to MCP content + structuredContent. |
| `http_transport.py` | Starlette ASGI app exposing MCP over Streamable HTTP for remote clients. |
| `__main__.py` | CLI entry point; wires settings + client + server and runs the chosen transport. |
| `scripts/build_client_release.py` | Packaging tool: builds the wheel and assembles the end-user client ZIP under `release/`. |

### Separation of concerns

- **Routing is pure and testable.** `build_request_from_spec` takes the tool name,
  api_method, arguments, and schema metadata and returns a `PreparedRequest` dataclass with
  no side effects. This is what the e2e verifier exercises for all 90 tools.
- **Client is generic.** It knows nothing about individual TestRail methods; it only
  executes a `PreparedRequest` (GET/POST, path, query, JSON body, multipart, binary).
- **Server is spec-driven.** It never hard-codes tool names beyond loading the spec.

## Components and Interfaces

### Settings and configuration (Requirement 4)

`Settings` is a `pydantic-settings` `BaseSettings` with `env_prefix="TESTRAIL_"` and
`env_file=".env"`. Resolution order for each field:

1. A real environment variable (`TESTRAIL_URL`, etc.) - highest precedence.
2. A matching entry in a `.env` file located in the process working directory.
3. The field default (for optional fields).

`extra="ignore"` means unrelated environment variables never cause a startup failure.
Required fields (`url`, `user`, `api_key`) have no default, so a missing value raises a
validation error that `__main__.py` catches and turns into a non-zero exit with a guidance
message. Optional fields: `request_timeout_seconds` (60.0), `mcp_transport`
(`stdio`|`http`), `http_host`, `http_port`, `http_path`, `http_stateless`.

### PreparedRequest

```python
@dataclass(frozen=True)
class PreparedRequest:
    http_method: str          # "GET" | "POST"
    uri_suffix: str           # e.g. "get_cases/14" (path portion after /api/v2/)
    query: dict[str, Any]     # querystring params for GET
    json_body: Any | None     # JSON payload for POST
    is_multipart_path: bool   # attachment upload
    binary_response: bool      # get_attachment
```

`full_api_url(base, uri_suffix, query=None)` renders `"{base}/index.php?/api/v2/{uri_suffix}"`
and, when `query` is present, appends each URL-encoded `key=value` pair joined with `&`
(e.g. `.../get_cases/14&suite_id=46384&limit=250`).

### TestRail query-string joining (Requirement 11)

TestRail encodes the whole API path inside a single `index.php?` query string. Additional
parameters must therefore be appended with `&`, NOT as a second `?`. The HTTP client must
NOT use httpx `params=` for GET calls — that appends a second `?`, which TestRail's router
mis-parses (returning `404 "Unknown controller '<param>'"` or an empty-body `500`). This was
the true cause of the `get_cases`/`get_sections` failures first misattributed to pagination.
`full_api_url` centralizes the `&`-joining and URL-encoding; `TestRailClient.execute` builds
the GET URL via `full_api_url(..., prepared.query)` and passes no `params=`.

### Tool-name -> api_method

Two regexes convert CamelCase to snake_case (`getCases` -> `get_cases`,
`addResultsForCases` -> `add_results_for_cases`). `infer_http_method` returns `GET` for
`get_*`, else `POST`.

### Path-parameter ordering

`PRIORITY_PATH_KEYS` defines a canonical order (project_id, suite_id, plan_id, entry_id,
milestone_id, run_id, case_id, section_id, ...). `default_path_keys` intersects the tool's
required args with this order, with explicit handling for known two-key combinations
(`{run_id, case_id}`, `{plan_id, entry_id}`, `{config_group_id, config_id}`,
`{plan_id, run_id}`).

### Pagination defaults (Requirement 3)

TestRail 6.7+ returns bulk collections in a paginated envelope. To make bare calls return a
full first page predictably, the server injects a default `limit`. (Note: the HTTP 500 first
seen on `get_cases` was NOT caused by a missing `limit` — that was the query-join bug in
Requirement 11. The default `limit` is still useful for large collections.):

```python
DEFAULT_PAGE_LIMIT = 250
PAGINATED_GET_METHODS = frozenset({
    "get_cases", "get_sections", "get_runs", "get_plans",
    "get_milestones", "get_tests", "get_results", "get_results_for_case",
    "get_results_for_run", "get_shared_steps",
})
```

Note: `get_suites` is intentionally excluded - TestRail's `get_suites` is not a paginated
endpoint (it returns all suites and does not accept `limit`/`offset`), so injecting a
`limit` would send an unsupported parameter.

In the GET query-assembly branch, after copying declared args:

```python
if api_method in PAGINATED_GET_METHODS and query.get("limit") is None:
    query["limit"] = DEFAULT_PAGE_LIMIT
```

For routing to forward `limit`/`offset` at all, they must be declared in the tool's
`properties`. `get_cases` and `get_sections` previously lacked them, so even a
caller-supplied `limit` was silently dropped; the spec now declares `limit` and `offset`
for both. Single-record reads (`get_suite`, `get_section`, `get_case`) are intentionally
excluded so they are never given a spurious `limit`.

### TestRailClient.execute

- **GET**: build the URL via `full_api_url(url, uri_suffix, query)` (query `&`-joined and URL-encoded) and call `client.request("GET", url)` with NO httpx `params=` (see Requirement 11).
- **Multipart** (`add_attachment_to_*`): resolve `body` to a file path (string or
  `{file_path}` dict), read bytes, POST as `files={"attachment": (name, bytes)}`. Validate
  existence first.
- **POST**: send `json_body` as JSON.
- **Non-2xx**: raise `RuntimeError("TestRail API HTTP {code}: {detail!r}")` with parsed JSON
  detail when available, else raw text. Any 2xx (200, 201, 204, ...) is treated as success.
- **200 empty body**: return `None`.
- **Binary** (`get_attachment`): return `{"encoding": "base64", "data": <b64>}`.

### server call_tool result mapping

- Serialize result to indented JSON text for `TextContent`.
- If result is a dict, pass it as `structuredContent`; if a list, wrap as `{"items": [...]}`.
- On any exception during build/execute, return `CallToolResult(isError=True)` with the
  message as text.

## Data Models

The authoritative data model is `tools_spec.json`. Each entry:

```json
{
  "name": "TestRail_API_getCases",
  "description": "[TestRail API] Get test cases in a suite (or specific section of suite)",
  "arguments": {
    "type": "object",
    "properties": { "project_id": {"type": "integer"}, "suite_id": {"type": "integer"},
                     "...filters...": {}, "limit": {"type": "integer"}, "offset": {"type": "integer"} },
    "required": ["project_id"]
  }
}
```

Tool categories in the catalog: attachments (get/add), cases (get/add/update/copy/move/delete),
case metadata (fields, statuses, types, priorities, templates, history), configs, milestones,
plans (+entries), projects, results (per test/case/run, +fields), runs, sections, shared steps,
suites, and users.

## Transports (Requirement 5)

`__main__.py` selects the transport from `Settings.mcp_transport`:

- **stdio** (default): `_run_stdio` opens the MCP stdio streams and runs the same `Server`
  built by `build_server`. This is the mode IDE/desktop clients use.
- **http**: `_run_http` builds a Starlette app via `build_streamable_http_app` and serves it
  with uvicorn on `http_host:http_port` at `http_path`. `StreamableHTTPSessionManager` runs
  in the app lifespan. Stateless mode (default) handles each request with a fresh MCP
  session; `http_stateless=False` enables resumable sessions.

Both paths construct the client and server identically, so the tool catalog and routing
behavior are transport-independent.

## Client Packaging and Configuration (Requirements 9, 10)

### Build pipeline

`scripts/build_client_release.py` produces a self-contained end-user bundle:

1. Read the version from `pyproject.toml`.
2. Ensure a wheel exists in `dist/`; if not, invoke `python -m build --wheel`. Warn if the
   discovered wheel name does not match the pyproject version.
3. Stage the wheel plus `docs/CLIENT_USER_GUIDE.md`, an `.env.example`, and OS install
   scripts (`INSTALL.cmd`, `INSTALL.sh`) with a generated `README-FIRST.txt`.
4. Zip the staging folder to `release/testrail-mcp-client-<version>.zip`.

The distributable exposes the `testrail-mcp` console entry point (from `pyproject.toml`
`[project.scripts]`) and is runnable as `python -m testrail_mcp`.

### Client wiring

The client points its MCP `command` at the venv Python with `args = ["-m", "testrail_mcp"]`.
Credentials/transport are supplied one of two ways:

- Inline in the client's `env` block (`TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY`,
  `TESTRAIL_MCP_TRANSPORT`), or
- Via a `.env` file, with the client's `cwd` set to the folder containing it (the settings
  loader reads `.env` from the process working directory).

Connectivity is confirmed when the client shows the server connected and a sample call such
as `TestRail_API_getProjects` returns a result. Documentation warns against committing or
sharing `.env`/API keys and advises rotating an exposed key.

## Error Handling

| Failure | Handling |
|---------|----------|
| Missing required path param | `ValueError` in routing, surfaced as an error tool result; no HTTP call. |
| Missing/invalid settings at startup | Process exits non-zero with guidance message. |
| Non-2xx from TestRail | `RuntimeError` with status + detail; returned as `isError` tool result (all 2xx are success). |
| Empty 200 body | Returns `None` (success). |
| Attachment file not found | `ValueError` before HTTP call. |
| Paginated endpoint without limit | Default `limit=250` injected so bare calls return a full first page. |

## Testing Strategy

`scripts/verify_e2e.py` provides five layers, runnable without a live TestRail:

1. **Routing coverage**: build a `PreparedRequest` for every tool in the spec using
   synthesized argument values; assert zero failures. Guards path/query/body assembly.
2. **Pagination**: assert `build_request_from_spec` for `get_cases`/`get_sections` injects
   `limit=250` when omitted, forwards caller-supplied `limit`/`offset` unchanged, and does
   not add `limit` to single-record reads (`get_suite`) or the non-paginated `get_suites`.
3. **URL format**: assert `full_api_url` `&`-joins query params (single `?`) both at the
   builder level and end-to-end through the client + mock transport (guards Requirement 11).
4. **Mocked HTTP**: run `TestRailClient.execute` against an `httpx.MockTransport` for a
   representative GET (`get_projects`) and a path-param GET (`get_section/:id`).
5. **In-process MCP**: start the server via the MCP memory session, assert `list_tools`
   returns the expected count (derived dynamically from the spec, currently 90), and that
   `call_tool("TestRail_API_getProjects")` returns a non-error result.

The verifier derives the expected tool count from the spec, so a spec change needs no manual
edit to the count assertion.