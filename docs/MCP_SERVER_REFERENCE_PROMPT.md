# MCP server (Python) — reusable reference

Use this document **anywhere** you need a consistent blueprint for a Python MCP server: **new repositories**, **AI chat prompts**, **internal wikis**, **design docs**, **PR templates**, or **onboarding**. It is **generic**; the **TestRailMCP** codebase is only an **example implementation** of these patterns.

**How to use**

| Where | What to copy |
|-------|----------------|
| **New chat / coding agent** | The [Master prompt](#master-prompt-copy-for-future-projects) block (fill placeholders first). |
| **Wiki / Confluence / Notion** | [Architecture summary](#architecture-summary-for-wikis), [Layout](#suggested-repository-layout), [Checklist](#checklist-before-calling-a-project-done). |
| **Issue or epic description** | [Short project brief](#short-project-brief-issues--epics). |
| **Code review** | [Review checklist](#checklist-before-calling-a-project-done) + [Why this shape](#why-this-shape). |
| **Another git repo** | Copy this file into `docs/MCP_SERVER_REFERENCE_PROMPT.md` (or link to a canonical URL); replace “example implementation” links with your paths. |

**Before pasting the master prompt**, replace:

| Placeholder | Example |
|-------------|---------|
| `EXTERNAL_SYSTEM` | Your CRM, Jira, internal REST API, Postgres, etc. |
| `ENV_PREFIX` | `MYAPI_`, `JIRA_`, `ACME_` — one prefix for all settings |
| `PACKAGE_NAME` | Python import name, e.g. `acme_mcp` |

---

## Master prompt (copy for future projects)

Copy everything inside the fence below into a new chat or project brief when you want an LLM to scaffold or review an MCP server.

```text
You are helping design and implement a Python MCP (Model Context Protocol) server that exposes EXTERNAL_SYSTEM (REST API, database, or other backend) as MCP tools.

Requirements and conventions:

1. **Stack**
   - Python 3.11 minimum; all newer 3.x supported
   - Official `mcp` package: low-level `mcp.server.lowlevel.Server` with `@server.list_tools()` and `@server.call_tool()`, OR FastMCP if the team prefers decorators-only.
   - `httpx` for async HTTP to external APIs; `pydantic-settings` for configuration.
   - Optional second transport: **Streamable HTTP** via `mcp.server.streamable_http_manager.StreamableHTTPSessionManager` + Starlette + uvicorn (not only stdio).

2. **Configuration**
   - One env prefix for all settings (use ENV_PREFIX consistently, e.g. MYAPI_).
   - Required secrets and base URLs via environment variables; support optional `.env` in the process working directory.
   - Never commit real secrets; provide `.env.example` with placeholders and `.gitignore` listing `.env`.

3. **Tools**
   - Prefer a machine-readable tool catalog (`tools_spec.json` or generated from OpenAPI) that defines `name`, `description`, and JSON Schema `arguments` per tool.
   - Implement a single routing layer that maps tool name + arguments → HTTP method, path, query, and body for the backend (avoid dozens of copy-pasted handlers unless necessary).
   - Return tool results as JSON text in `CallToolResult` for LLM consumption; use `structuredContent` when it helps clients.

4. **Entry point**
   - `python -m PACKAGE_NAME` and/or console script in `pyproject.toml`.
   - Branch on transport: **stdio** (default) for Cursor/subprocess clients; **http** for remote Streamable HTTP when `*_MCP_TRANSPORT=http`.

5. **Packaging**
   - `pyproject.toml` with `hatchling`; **no UTF-8 BOM** on TOML (use UTF-8 without BOM; add `.editorconfig`).
   - Include package data (JSON specs) inside the installable package under `importlib.resources`.

6. **Docs and DX**
   - `docs/DEPLOYMENT.md`: install, env vars, stdio vs HTTP, security, troubleshooting (include TOML-BOM issue).
   - Optional: `docs/CLIENT_USER_GUIDE.md` or similar if you ship a wheel/ZIP to non-developers.
   - `prompts/`: optional sample user phrases per tool.
   - `scripts/`: smoke tests (routing, mocked HTTP, in-process MCP via `mcp.shared.memory` if available).

7. **Security**
   - Treat API keys like passwords; document rotation; recommend reverse proxy + TLS for HTTP transport in production.

Deliver: package layout, `settings.py`, client/routing, `server.py`, `__main__.py`, optional `http_transport.py`, `.env.example`, minimal tests or `verify_e2e.py`, and deployment doc. Keep scope focused; no unrelated refactors.
```

---

## Short project brief (issues / epics)

Paste and edit:

```text
Build a Python MCP server (3.11 minimum; support all newer 3.x) bridging [EXTERNAL_SYSTEM] with stdio (Cursor) and optional Streamable HTTP.
Config: ENV_PREFIX + .env; tools driven by tools_spec.json + router; hatchling package; docs/DEPLOYMENT.md.
Security: no secrets in git; TLS/auth for HTTP in production.
```

---

## Architecture summary (for wikis)

- **MCP** exposes backend capabilities as **tools** (name + JSON arguments) and returns structured results to the host (e.g. Cursor).
- **Stdio** is the default transport for locally spawned processes; **Streamable HTTP** suits remote clients or a shared server behind a reverse proxy.
- **Single tool catalog** (JSON or generated) keeps `list_tools` aligned with backend coverage; a **router** maps tool calls to HTTP/DB operations instead of one file per endpoint when the API is uniform.
- **Settings** use one env prefix and optional `.env` in `cwd` for developer ergonomics.

---

## Why this shape

| Topic | Recommendation |
|--------|------------------|
| **Stdio** | Default for IDE-spawned MCP (Cursor, Claude Desktop patterns). |
| **Streamable HTTP** | For clients that connect to a URL, or for running one shared process behind a reverse proxy. |
| **Bundled JSON tools** | Keeps MCP `list_tools` in sync with a single source of truth; enables codegen or static review. |
| **Router instead of N files** | Easier to maintain when the backend has many similar endpoints (REST). |
| **BOM on `pyproject.toml`** | Breaks TOML parsers; enforce UTF-8 without BOM. |

---

## Suggested repository layout

```text
src/<package_name>/          # or flat <package_name>/ at repo root
  __init__.py
  __main__.py                  # stdio vs http branch
  settings.py                  # pydantic-settings + env prefix
  client.py                    # backend HTTP / DB access
  routing.py                   # tool name → backend request
  server.py                    # MCP Server + handlers
  http_transport.py            # optional Starlette + Streamable HTTP
  data/
    tools_spec.json            # optional
docs/
  DEPLOYMENT.md
  MCP_SERVER_REFERENCE_PROMPT.md   # optional: this file, for your team
prompts/
  sample_tool_prompts.md       # optional; can be generated
scripts/
  verify_e2e.py                # optional smoke tests
.env.example
.gitignore                     # include .env
.editorconfig                  # charset utf-8
pyproject.toml                 # UTF-8, no BOM
README.md
```

Adapt names (`src/` layout vs flat) to your org’s Python guidelines.

---

## Checklist before calling a project “done”

- [ ] `pip install -e .` works; `pyproject.toml` parses (no BOM).
- [ ] All required env vars documented in `.env.example`.
- [ ] Stdio MCP session works with at least one real tool call.
- [ ] If HTTP is supported: bind address/port documented; warn about TLS/auth for production.
- [ ] No secrets in git history for the default branch.
- [ ] Optional: `scripts/verify_e2e.py` or pytest for routing and smoke MCP.
- [ ] Optional: wheel build + end-user doc if non-developers install from an artifact only.

---

## Example implementation (this repository)

These paths illustrate the patterns above; **rename** when you copy ideas into another repo.

| File | Role |
|------|------|
| `docs/DEPLOYMENT.md` | Install, transports, troubleshooting |
| `testrail_mcp/server.py` | Low-level MCP server + tool handlers |
| `testrail_mcp/http_transport.py` | Streamable HTTP Starlette app |
| `testrail_mcp/settings.py` | Env-driven settings |
| `scripts/verify_e2e.py` | Local verification |

Keep the **master prompt** block portable: paste it into new projects or link to this file from your team handbook.
