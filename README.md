# TestRailMCP

Model Context Protocol (MCP) server for TestRail, with LLM-assisted test case creation.

**Python:** 3.11 minimum; **all newer 3.x releases** (3.12, 3.13, and later) are supported (`requires-python >=3.11` in [`pyproject.toml`](pyproject.toml)).

## Layout

- `testrail_mcp/` — Python package (MCP server, TestRail HTTP client, stdio + Streamable HTTP transports).
- `docs/` — Deployment, **publisher vs end-user** (`SERVER.md`, `CLIENT.md`, **`CLIENT_USER_GUIDE.md`** for ZIP bundles), self-contained **[WIKI_CLIENT.md](docs/WIKI_CLIENT.md)** for internal wikis, step-by-step setup, **GitHub + MCP copy-paste** (`GITHUB_COPY.md`).
- `prompts/` — Sample user prompts per MCP tool.
- `scripts/` — Dev helpers (e.g. `verify_e2e.py`, prompt generator).
- `skills/` — Sample Cursor-style skills (security, accessibility, test writing, coding guidelines, folder structure). Copy into `.cursor/skills/` or reference from prompts.

## Sample skills

| Folder | Topic |
|--------|--------|
| `skills/security-testing/` | Security-oriented test ideas |
| `skills/accessibility-testing/` | WCAG-style manual checks |
| `skills/test-case-writing/` | TestRail case quality |
| `skills/coding-guidelines/` | Testability and conventions |
| `skills/folder-structure/` | Repo layout ↔ TestRail sections |

## Docs

- **[Server — build & distribute the wheel](docs/SERVER.md)** — for developers: `python -m build`, what to send, versioning, security.
- **[Client — install wheel + Cursor](docs/CLIENT.md)** — for end users with **no** git repo: venv, `pip install` the `.whl`, MCP JSON.
- **[Client user guide](docs/CLIENT_USER_GUIDE.md)** — self-contained doc (also the **only** guide inside the client **ZIP**).
- **[Client wiki (copy to Confluence / internal wiki)](docs/WIKI_CLIENT.md)** — self-contained: install, Cursor JSON, env, troubleshooting, **full tool list**, example prompts (no other repo docs required).
- **Client ZIP bundle** — run `python scripts/build_client_release.py` → **`release/testrail-mcp-client-*.zip`** (`wheel/`, **`docs/CLIENT_USER_GUIDE.md`**, installers). See [release/README.md](release/README.md).
- **[Step-by-step setup](docs/STEP_BY_STEP_SETUP.md)** — local folder (no GitHub required), venv, Cursor MCP with URL / email / PAT; optional GitHub at the end.
- **[GitHub + MCP copy-paste](docs/GITHUB_COPY.md)** — remote URL, `git push`, ready-made MCP JSON blocks.
- **[Deployment and usage](docs/DEPLOYMENT.md)** — full reference: install, **stdio** or **HTTP**, security, troubleshooting.
- **[MCP server reference (portable)](docs/MCP_SERVER_REFERENCE_PROMPT.md)** — master prompt, wiki brief, layout, checklist — reuse in **other repos**, chats, or internal docs.
- **Sample prompts** — `prompts/sample_tool_prompts.md` (one example per TestRail tool).
