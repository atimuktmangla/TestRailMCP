# Deployment and usage guide

**End user with only a `.whl` file?** Use **[CLIENT.md](CLIENT.md)** or **[CLIENT_USER_GUIDE.md](CLIENT_USER_GUIDE.md)**. **Received the client ZIP?** Follow **`docs/CLIENT_USER_GUIDE.md`** inside the bundle. **Building the wheel or ZIP to share?** Use **[SERVER.md](SERVER.md)**.

**First-time user with the source tree?** Use **[STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md)** — project folder on your machine (GitHub optional), venv, and **Cursor MCP JSON** with `TESTRAIL_URL`, `TESTRAIL_USER` (email), and `TESTRAIL_API_KEY` (TestRail API key / PAT). A **`.env`** file is optional.

This document is the full reference for installing, configuring, and running **testrail-mcp** (stdio or HTTP transport), security, and troubleshooting.

---

## What this project provides

- An MCP server that exposes TestRail’s REST API v2 as MCP tools (`testrail_mcp/data/tools_spec.json`).
- **Transports** (one per process):
  - **stdio** (default) — MCP over stdin/stdout (typical for Cursor).
  - **HTTP** — MCP **Streamable HTTP** (Starlette + uvicorn) for clients that connect to a URL.
- Configuration via **`TESTRAIL_*`** environment variables, optionally loaded from **`.env`** in the process working directory.

---

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| **Python** | 3.11 minimum; all newer 3.x supported |
| **Network** | HTTPS to your TestRail host |
| **TestRail** | Account with API access; **API Key** from My Settings (used as `TESTRAIL_API_KEY` / PAT) |
| **MCP client** | stdio and/or Streamable HTTP, depending on transport |

---

## Source code: GitHub (personal repository)

Typical flow for a **personal** GitHub account (replace `YOUR_USERNAME` and `TestRailMCP` if your repo name differs):

1. Create an empty repo on GitHub: `https://github.com/YOUR_USERNAME/TestRailMCP` (HTTPS or SSH).
2. From your project folder (first push):

```bash
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/TestRailMCP.git
git add .
git status
git commit -m "Initial commit: testrail-mcp"
git push -u origin main
```

Do **not** commit `.env` or real PATs. Use `.gitignore` (includes `.env`, `.venv/`, `dist/`).

For **copy-paste blocks** (Git remote, MCP JSON), see **[GITHUB_COPY.md](GITHUB_COPY.md)**.

---

## Install the package

### Option A — From a clone (recommended)

```bash
git clone https://github.com/YOUR_USERNAME/TestRailMCP.git
cd TestRailMCP
python -m venv .venv
```

**Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`  
**macOS / Linux:** `source .venv/bin/activate`

```bash
pip install -e .
```

### Option B — From a wheel (no git)

```bash
pip install build
python -m build --wheel
pip install dist/testrail_mcp-*-py3-none-any.whl
```

### Option C — Private PyPI / internal index

```bash
pip install testrail-mcp==0.1.0 --index-url https://your-internal-pypi/simple/
```

---

## Configuration — TestRail API

| Variable | Required | Description |
|----------|----------|-------------|
| `TESTRAIL_URL` | Yes | TestRail base URL, e.g. `https://yourcompany.testrail.io` |
| `TESTRAIL_USER` | Yes | Email or username for TestRail API auth |
| `TESTRAIL_API_KEY` | Yes | TestRail **API Key** (HTTP Basic password; often called PAT) |
| `TESTRAIL_REQUEST_TIMEOUT_SECONDS` | No | Default `60` |

## Configuration — MCP transport

| Variable | Default | Description |
|----------|---------|-------------|
| `TESTRAIL_MCP_TRANSPORT` | `stdio` | `stdio` or `http` |
| `TESTRAIL_HTTP_HOST` | `127.0.0.1` | MCP HTTP bind address (not TestRail) |
| `TESTRAIL_HTTP_PORT` | `8765` | MCP HTTP port |
| `TESTRAIL_HTTP_PATH` | `/mcp` | Streamable HTTP path |
| `TESTRAIL_HTTP_STATELESS` | `true` | Stateless HTTP sessions (simplest) |

Copy **`.env.example`** → **`.env`** for local secrets. Process **env** overrides **`.env`** if both set the same key.

---

## Running — stdio (default)

```bash
set TESTRAIL_MCP_TRANSPORT=stdio
python -m testrail_mcp
```

Or: `testrail-mcp` if the console script is on `PATH`.

---

## Running — HTTP (Streamable HTTP)

Example endpoint: `http://127.0.0.1:8765/mcp`

```bash
set TESTRAIL_MCP_TRANSPORT=http
set TESTRAIL_HTTP_HOST=127.0.0.1
set TESTRAIL_HTTP_PORT=8765
python -m testrail_mcp
```

Put **TLS + auth** in front if exposing beyond localhost.

---

## Cursor MCP (stdio)

End users set **`env`** with URL, email, and PAT — see **[STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md)** and **[GITHUB_COPY.md](GITHUB_COPY.md)**.

**Alternative:** only `command`, `args`, `cwd`; credentials in **`.env`** in the repo root.

---

## Deployment scenarios

| Scenario | Setup |
|----------|--------|
| **Personal GitHub + local Cursor** | Clone repo, venv, `pip install -e .`, MCP `env` or `.env`. |
| **HTTP on a host** | `TESTRAIL_MCP_TRANSPORT=http`, reverse proxy, firewall. |
| **CI** | Mock HTTP tests; no production keys in logs. |

---

## Security

- Never commit **`TESTRAIL_API_KEY`** or **`.env`**.
- For HTTP: do not expose MCP port publicly without TLS and access control.

---

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| Missing configuration | `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY` |
| Wrong TestRail instance | Env vars overriding `.env` |
| Windows: no `testrail-mcp` command | Use `python -m testrail_mcp` from the venv |
| HTTP: port in use | Change `TESTRAIL_HTTP_PORT` |
| MCP tools empty | Transport mismatch; TestRail key invalid; network |
| **Invalid TOML** at `[build-system]` | **UTF-8 BOM** on `pyproject.toml` — save as UTF-8 **without** BOM, or strip BOM (see [STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md)). |

---

## Optional: local verification

```bash
python scripts/verify_e2e.py
```

Uses mocks; does not call real TestRail unless you extend it.

---

## Further reading

- [SERVER.md](SERVER.md) — build and distribute the wheel  
- [CLIENT.md](CLIENT.md) — install wheel + Cursor (no repo)  
- [CLIENT_USER_GUIDE.md](CLIENT_USER_GUIDE.md) — client-only guide (contents of the client ZIP `docs/` folder)  
- [WIKI_CLIENT.md](WIKI_CLIENT.md) — self-contained client wiki (paste to Confluence; install, tools, examples)  
- [STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md) — step-by-step with source folder  
- [GITHUB_COPY.md](GITHUB_COPY.md) — Git + MCP copy-paste  
- [MCP_SERVER_REFERENCE_PROMPT.md](MCP_SERVER_REFERENCE_PROMPT.md) — portable prompt + checklist for MCP servers in other repos or docs  
- `prompts/sample_tool_prompts.md` — sample phrases per tool  
- `testrail_mcp/data/tools_spec.json` — tool schemas  
