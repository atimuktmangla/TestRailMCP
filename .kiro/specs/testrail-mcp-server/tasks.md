# Implementation Plan: TestRail MCP Server

## Overview

This plan reflects the current state of the codebase. All tasks are complete: tasks 1-7
and 9 document already-implemented behavior; tasks 8, 10-12 were verified this cycle; task
13 fixed the TestRail query-string URL bug (the real cause of the collection-endpoint 500).
Each task references the requirements it implements.

## Task Dependency Graph

All tasks are complete. The waves below record the dependency order in which the
verifiable and net-new work was carried out.

```json
{
  "waves": [
    { "wave": 1, "tasks": ["1", "2", "4"], "depends_on": [] },
    { "wave": 2, "tasks": ["3"], "depends_on": ["1", "2", "4"] },
    { "wave": 3, "tasks": ["5"], "depends_on": ["3"] },
    { "wave": 4, "tasks": ["6", "7"], "depends_on": ["5"] },
    { "wave": 5, "tasks": ["8.1", "9"], "depends_on": ["7"] },
    { "wave": 6, "tasks": ["8.2"], "depends_on": ["8.1"] },
    { "wave": 7, "tasks": ["8.3"], "depends_on": ["8.2"] },
    { "wave": 8, "tasks": ["10.1"], "depends_on": ["6"] },
    { "wave": 9, "tasks": ["10.2"], "depends_on": ["10.1"] },
    { "wave": 10, "tasks": ["11.1"], "depends_on": ["10.2"] },
    { "wave": 11, "tasks": ["11.2"], "depends_on": ["11.1"] },
    { "wave": 12, "tasks": ["12"], "depends_on": ["3", "9", "10.2", "11.2"] },
    { "wave": 13, "tasks": ["13.1"], "depends_on": ["4"] },
    { "wave": 14, "tasks": ["13.2"], "depends_on": ["13.1"] }
  ]
}
```

## Tasks

- [x] 1. Configuration and settings
  - Implement `Settings` (pydantic-settings) with `TESTRAIL_` prefix and `.env` support
  - Require `url`, `user`, `api_key`; add timeout and transport options
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3_

- [x] 2. Declarative tool spec
  - Maintain `data/tools_spec.json` as the single source of truth for all tools
  - Bundle it in the `testrail_mcp.data` package
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 3. Routing: name -> request
  - Convert tool name to `api_method`; infer HTTP method
  - Assemble path params in canonical order; place remaining GET args in query; build POST body
  - Handle `update_cases_by_case_id` special path and missing-path-param errors
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

- [x] 4. Client: execute requests
  - Wrap `httpx.AsyncClient` with HTTP Basic auth
  - Handle GET/POST, multipart attachment upload, binary responses, non-2xx errors, empty bodies
  - _Requirements: 4.6, 6.1, 6.2, 6.3, 6.5, 7.1, 7.2, 7.3_

- [x] 5. Server: expose and dispatch tools
  - Load spec, implement `list_tools` with read-only annotations
  - Implement `call_tool` mapping results to text + structuredContent, errors to isError
  - _Requirements: 1.2, 1.4, 1.5, 6.4_

- [x] 6. Transports
  - stdio transport (default) in `__main__.py`
  - Streamable HTTP transport via Starlette/uvicorn (`http_transport.py`), stateless default
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [x] 7. Pagination reliability fix
  - [x] 7.1 Add `limit` and `offset` to `getCases` and `getSections` in `tools_spec.json`
    - _Requirements: 3.3_
  - [x] 7.2 Inject `DEFAULT_PAGE_LIMIT` for `PAGINATED_GET_METHODS` when caller omits `limit`
    - Exclude single-record reads; respect caller-supplied `limit`/`offset`
    - _Requirements: 3.1, 3.2, 3.4, 3.5_

- [x] 8. Verify pagination fix end-to-end
  - [x] 8.1 Extend `scripts/verify_e2e.py` with assertions: `get_cases`/`get_sections` inject
        `limit=250` when omitted; caller `limit`/`offset` forwarded unchanged;
        `get_suite` and non-paginated `get_suites` get no `limit`
    - _Requirements: 3.1, 3.2, 3.4, 8.1, 8.5_
  - [x] 8.2 Run `verify_e2e.py` and confirm all layers pass; update expected tool count if changed
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  - [x] 8.3 Root-caused and fixed the real defect: the HTTP 500 was NOT pagination but
        malformed query-string joining. httpx `params=` appended a second `?` to TestRail's
        `index.php?` URL, so TestRail mis-parsed the first param ("Unknown controller"),
        yielding 404/empty-500. Fixed `full_api_url` to append params with `&` + URL-encode,
        and removed `params=` from the client. Live-verified: project 14 / suite 46384 now
        returns 133 cases; project 1 / suite 2 returns 10 (limit=3 override returns 3).
    - _Requirements: 3.5, 11.1, 11.2, 11.3, 11.4_

- [x] 9. Audit remaining paginated endpoints in the spec
  - Confirmed 10 of 11 methods declare `limit`/`offset` in `tools_spec.json`. Found
    `get_suites` is NOT a paginated TestRail endpoint; removed it from
    `PAGINATED_GET_METHODS` rather than adding unsupported params
  - _Requirements: 3.1, 3.3_

- [x] 10. Client distribution packaging
  - [x] 10.1 Verify `scripts/build_client_release.py` builds a versioned client ZIP under
        `release/` containing wheel, `CLIENT_USER_GUIDE.md`, `.env.example`, and install scripts
    - _Requirements: 9.1, 9.2, 9.3_
  - [x] 10.2 Confirm the built package exposes the `testrail-mcp` console entry point and runs
        via `python -m testrail_mcp`
    - _Requirements: 9.4_

- [x] 11. Client configuration and connectivity
  - [x] 11.1 Validate the stdio MCP config (venv Python + `-m testrail_mcp`) with credentials
        via `env` block and via `.env` + `cwd`
    - _Requirements: 10.1, 10.2_
  - [x] 11.2 Confirm a sample `TestRail_API_getProjects` call succeeds once connected
    - _Requirements: 10.3_

- [x] 12. Documentation sync
  - Update `docs/SERVER.md` / `docs/MCP_SERVER_REFERENCE_PROMPT.md` to note pagination
    defaults and how to page with `limit`/`offset`
  - Ensure client docs reflect the `.env` precedence and key-rotation guidance
  - _Requirements: 3.1, 3.2, 10.4_

- [x] 13. Fix TestRail query-string URL construction
  - [x] 13.1 Append GET query params with `&` (URL-encoded) in `full_api_url`; stop passing
        httpx `params=` in `TestRailClient.execute`
    - _Requirements: 11.1, 11.2, 11.3, 11.4_
  - [x] 13.2 Add a `check_url_format` layer to `verify_e2e.py` asserting the `&`-joined URL
        at both the builder level and end-to-end via the mock transport
    - _Requirements: 11.5_

## Notes

- Tasks 1-9 describe already-implemented behavior; they are documented for traceability and
  should not be re-implemented.
- Task 8.3/13 are complete and live-verified against TestRail (suite 46384 -> 133 cases).
  The IDE-managed MCP server process must reload the updated code before the live
  `mcp_testrail_*` tools reflect the fix; `verify_e2e.py` covers it at the logic + client level.
- Requirement references map to `requirements.md` in this spec directory.