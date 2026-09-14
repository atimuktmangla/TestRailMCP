# Requirements Document

_Spec: TestRail MCP Server_

## Introduction

The TestRail MCP Server is a Model Context Protocol (MCP) server that bridges MCP-capable
clients (Kiro, Claude Desktop, IDE agents) to the TestRail REST API v2. It exposes the
TestRail API surface as a catalog of individually-callable MCP tools, generated from a
declarative JSON specification, so that an LLM agent can read and manage TestRail projects,
suites, sections, cases, runs, plans, milestones, results, and attachments through natural
language.

The server is written in Python (>=3.11), uses `httpx` for async HTTP with TestRail HTTP
Basic auth, `pydantic-settings` for configuration, and the official `mcp` SDK. It supports
two wire transports: stdio (default, for local IDE integration) and Streamable HTTP (for
remote deployments, via Starlette + uvicorn). A companion client package and documentation
support LLM-assisted test-case authoring.

## Glossary

- **MCP**: Model Context Protocol; the tool/resource protocol spoken between the agent host and this server.
- **Tool spec**: `testrail_mcp/data/tools_spec.json`, the declarative list of tool definitions (name, description, JSON-schema arguments).
- **api_method**: the snake_case TestRail API v2 method derived from a tool name (e.g. `TestRail_API_getCases` -> `get_cases`).
- **PreparedRequest**: the internal, transport-agnostic description of one outbound HTTP call to TestRail.
- **Paginated collection**: a TestRail list endpoint that returns results in a `{offset, limit, size, _links, <items>}` envelope.

## Requirements

### Requirement 1: Expose TestRail API v2 as MCP tools

**User Story:** As an agent host, I want every supported TestRail operation exposed as a
discrete MCP tool, so that an LLM can discover and invoke TestRail functionality by name.

#### Acceptance Criteria

1. WHEN the server starts THEN it SHALL load tool definitions from `tools_spec.json` bundled in the `testrail_mcp.data` package.
2. WHEN a client calls `list_tools` THEN the server SHALL return one MCP tool per spec entry, preserving name, description, and input JSON schema.
3. WHEN a tool spec defines required and optional arguments THEN the server SHALL surface them in the tool's `inputSchema`.
4. IF a tool's `api_method` begins with `get_` THEN the server SHALL annotate the tool with `readOnlyHint = true`, ELSE `readOnlyHint = false`.
5. WHEN the tool catalog is loaded THEN the total number of exposed tools SHALL equal the number of entries in `tools_spec.json` (the spec is the single source of truth for the count; 90 at time of writing).

### Requirement 2: Route tool calls to correct TestRail HTTP requests

**User Story:** As an agent, I want each tool call translated into the correct TestRail API
v2 HTTP request, so that my intent reaches TestRail accurately.

#### Acceptance Criteria

1. WHEN a tool name is received THEN the server SHALL derive the `api_method` by stripping the `TestRail_API_` prefix and converting CamelCase to snake_case.
2. IF the `api_method` starts with `get_` THEN the HTTP method SHALL be `GET`, ELSE `POST`.
3. WHEN building the request THEN required path parameters (e.g. `project_id`, `suite_id`, `run_id`, `case_id`) SHALL be placed in the URI path in TestRail's expected order.
4. WHEN building a GET request THEN remaining arguments that are declared in the tool's `properties` SHALL be placed in the query string, and undeclared or null arguments SHALL be dropped.
5. WHEN building a POST request with a `body` argument THEN the body SHALL be sent as the JSON payload; WHEN no `body` is present THEN non-path arguments SHALL be merged into the JSON payload.
6. WHEN a required path parameter is missing THEN the server SHALL raise a clear error naming the missing parameter, without issuing an HTTP call.
7. WHEN `update_cases_by_case_id` is called THEN the server SHALL route to `POST update_cases/:suite_id` and require `suite_id`.
8. WHEN any other request-construction validation fails (e.g. unknown tool name, malformed arguments that prevent forming a valid API call) THEN the server SHALL raise a clear error and SHALL NOT issue an HTTP call.

### Requirement 3: Reliable pagination for bulk collection endpoints

**User Story:** As an agent, I want bulk list endpoints to return results reliably, so that
listing cases or sections in a large project does not fail.

#### Acceptance Criteria

1. WHEN a paginated GET endpoint (`get_cases`, `get_sections`, `get_runs`, `get_plans`, `get_milestones`, `get_tests`, `get_results`, `get_results_for_case`, `get_results_for_run`, `get_shared_steps`) is called AND the caller did not supply `limit` THEN the server SHALL inject a default `limit` (250, TestRail's max page size). NOTE: `get_suites` is excluded because it is not a paginated TestRail endpoint.
2. WHEN the caller supplies an explicit `limit` and/or `offset` THEN the server SHALL forward those values unchanged and SHALL NOT override them.
3. WHEN a tool spec supports pagination THEN its `properties` SHALL include `limit` and `offset` so routing forwards them.
4. WHEN a non-paginated GET (e.g. `get_suite`, `get_section`, `get_case`) is called THEN the server SHALL NOT inject a `limit`.
5. WHEN `get_cases` or `get_sections` is called against a valid project/suite THEN the call SHALL return case/section data (verified live: e.g. project 14 / suite 46384 returns 133 cases). The HTTP 500 originally observed was caused by malformed query-string joining (see Requirement 11), not by pagination.

### Requirement 4: Authentication and configuration

**User Story:** As an operator, I want to configure the TestRail connection through
environment variables, so that credentials are not hard-coded.

#### Acceptance Criteria

1. WHEN the server starts THEN it SHALL read settings from environment variables prefixed with `TESTRAIL_`.
2. WHEN a `.env` file is present in the process working directory THEN the server SHALL load values from it, with real environment variables taking precedence over `.env` entries.
3. WHEN an environment variable not recognized by the settings model is present THEN the server SHALL ignore it rather than fail (extra = ignore).
4. THE server SHALL require `TESTRAIL_URL`, `TESTRAIL_USER`, and `TESTRAIL_API_KEY`.
5. WHEN required settings are missing or invalid THEN the process SHALL exit with a non-zero code and a message naming the required variables, without starting the server.
6. WHEN calling TestRail THEN the server SHALL authenticate using HTTP Basic auth with `TESTRAIL_USER` and `TESTRAIL_API_KEY`.
7. THE server SHALL apply a configurable request timeout (default 60 seconds).

### Requirement 5: Transports (stdio and Streamable HTTP)

**User Story:** As an operator, I want to run the server either locally over stdio or
remotely over HTTP, so that it fits both IDE and hosted deployments.

#### Acceptance Criteria

1. WHEN `TESTRAIL_MCP_TRANSPORT` is unset or `stdio` THEN the server SHALL run over stdio.
2. WHEN `TESTRAIL_MCP_TRANSPORT` is `http` THEN the server SHALL serve MCP over Streamable HTTP via Starlette + uvicorn on the configured host, port, and path.
3. WHEN HTTP transport is selected THEN it SHALL default to stateless mode (one MCP session per request) and SHALL support stateful mode when configured.
4. THE server SHALL expose the same tool catalog and routing behavior regardless of transport.

### Requirement 6: Response and error handling

**User Story:** As an agent, I want consistent, machine-readable responses and clear errors,
so that I can act on results and diagnose failures.

#### Acceptance Criteria

1. WHEN TestRail returns HTTP 200 with a JSON body THEN the server SHALL return the parsed JSON as the tool result.
2. WHEN TestRail returns HTTP 200 with an empty body THEN the server SHALL return a null/empty result rather than error.
3. WHEN TestRail returns a 2xx status THEN the server SHALL treat the response as successful; WHEN TestRail returns any non-2xx status THEN the server SHALL raise an error that includes the status code and response detail (parsed JSON when available, else raw text).
4. WHEN the result is a JSON object THEN it SHALL also be surfaced as MCP `structuredContent`; WHEN it is a list THEN it SHALL be wrapped as `{ "items": [...] }` for structured content.
5. WHEN a binary attachment endpoint (`get_attachment`) is called THEN the server SHALL return the content base64-encoded with an `encoding` marker.

### Requirement 7: File attachment uploads

**User Story:** As an agent, I want to upload attachments to TestRail entities, so that
evidence can be attached to cases, runs, plans, and results.

#### Acceptance Criteria

1. WHEN an `add_attachment_to_*` tool is called THEN the server SHALL send a multipart/form-data request with the file under the `attachment` field.
2. WHEN the `body` argument is a filesystem path string, OR a dict containing `file_path` THEN the server SHALL read that file for upload.
3. WHEN the `body` argument does not specify a file (neither a path string nor a dict with `file_path`), OR the referenced file does not exist or is not readable THEN the server SHALL raise a clear validation error before issuing the HTTP request.

### Requirement 8: Verifiability

**User Story:** As a maintainer, I want automated checks for routing and MCP behavior, so
that changes to the spec or routing do not silently break tools.

#### Acceptance Criteria

1. THE project SHALL provide an end-to-end verification script that builds a request for every tool in the spec and asserts no routing errors.
2. THE verification SHALL exercise the client against a mocked HTTP transport for representative GET and path-parameter calls.
3. THE verification SHALL start the server in-process and assert `list_tools` returns the expected tool count and that a sample `call_tool` succeeds.
4. THE verification SHALL derive the expected tool count dynamically from the spec (rather than a hard-coded literal) so that a spec change does not require manually editing the check.
5. THE verification SHALL assert pagination behavior: paginated GETs inject the default `limit`, caller-supplied `limit`/`offset` are forwarded unchanged, and single-record reads and non-paginated endpoints receive no injected `limit`.

### Requirement 9: Client distribution packaging

**User Story:** As a publisher, I want to build a self-contained client bundle, so that end
users can install and run the server without cloning the repository.

#### Acceptance Criteria

1. THE project SHALL provide a build script that produces a versioned client ZIP under `release/` containing the wheel, the client user guide, an `.env.example`, and OS install scripts (`INSTALL.cmd`, `INSTALL.sh`).
2. WHEN no wheel exists in `dist/` THEN the build script SHALL build one before assembling the bundle.
3. THE bundle version SHALL be derived from `pyproject.toml`, and the script SHALL warn when the discovered wheel does not match that version.
4. THE built package SHALL expose a `testrail-mcp` console entry point and SHALL be runnable via `python -m testrail_mcp`.

### Requirement 10: Client configuration and connectivity

**User Story:** As an end user, I want a documented way to configure the MCP server in my
client, so that I can connect to my TestRail instance over stdio.

#### Acceptance Criteria

1. THE client SHALL be configurable by pointing the MCP `command` at the venv Python with `args = ["-m", "testrail_mcp"]`.
2. THE user SHALL be able to supply `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY`, and `TESTRAIL_MCP_TRANSPORT` either via the client's `env` block or via a `.env` file referenced through the process working directory (`cwd`).
3. WHEN the configuration values are valid THEN the client SHALL start and connect; a sample call such as ``TestRail_API_getProjects`` SHALL return a result WHEN the TestRail instance is also reachable. "Configured correctly" refers to valid configuration values and is distinct from network reachability.
4. THE documentation SHALL warn against committing or sharing the `.env` file or API key and SHALL advise rotating an exposed key.

### Requirement 11: TestRail query-string URL construction

**User Story:** As an agent, I want GET query parameters delivered in the exact form
TestRail's router expects, so that filtered and paginated list calls do not fail.

#### Acceptance Criteria

1. THE server SHALL encode the entire API path inside the single `index.php?/api/v2/...` query string.
2. WHEN a GET request has query parameters THEN the server SHALL append them to the URL joined with `&` (e.g. `.../get_cases/14&suite_id=46384&limit=250`) and SHALL NOT introduce a second `?`.
3. THE server SHALL URL-encode query keys and values.
4. THE server SHALL NOT pass query parameters via the HTTP client's separate `params=` mechanism, because that appends a second `?` that TestRail mis-parses (yielding "Unknown controller" 404s or empty-body 500s).
5. THE verification SHALL assert the `&`-joined URL form for a representative paginated GET, both at the URL-builder level and end-to-end through the client.
