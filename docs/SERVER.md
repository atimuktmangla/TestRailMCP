# Server — build and distribute testrail-mcp

This guide is for **you** (developer / publisher): producing the **testrail-mcp** MCP server package and giving it to others **without sharing your git repository**.

**“Server” here** means this Python MCP process (`testrail-mcp`), not your TestRail cloud instance.

**Recipients** of a **`.whl`** only follow **[CLIENT.md](CLIENT.md)** or **[CLIENT_USER_GUIDE.md](CLIENT_USER_GUIDE.md)**. The **client ZIP** includes **`CLIENT_USER_GUIDE.md`** only (no publisher docs).

---

## Prerequisites

- Python **3.11 minimum**; **all newer 3.x** supported
- This repository cloned or copied on your machine (with `pyproject.toml` at the root)
- A virtual environment (recommended)

---

## 1. Prepare a clean build

1. Open a terminal at the **project root** (folder containing `pyproject.toml`).
2. Activate your venv.
3. Install/refresh dev dependencies if needed:
   ```bash
   pip install -U pip build
   ```

4. (Optional) Run local checks:
   ```bash
   pip install -e .
   python scripts/verify_e2e.py
   ```

---

## 2. Build the wheel

From the project root:

```bash
python -m build --wheel
```

Artifacts appear under **`dist/`**, for example:

- `testrail_mcp-0.1.0-py3-none-any.whl`

To build both wheel and source distribution:

```bash
python -m build
```

### One-step client ZIP (wheel + user guide + `INSTALL.cmd`)

From the project root:

```bash
pip install build
python scripts/build_client_release.py
```

Writes **`release/testrail-mcp-client-<version>.zip`**. It contains **end-user files only**: **`wheel/`**, **`docs/CLIENT_USER_GUIDE.md`**, **`.env.example`**, **`README-FIRST.txt`**, **`INSTALL.cmd`**, **`INSTALL.sh`** — no server-side or git setup docs. Share that ZIP with end users; they unpack and run **`INSTALL.cmd`** (Windows) or **`INSTALL.sh`** (Unix). See **[release/README.md](../release/README.md)** and **[CLIENT_USER_GUIDE.md](CLIENT_USER_GUIDE.md)**.

---

## 3. What to send

**Minimum:** the **`.whl`** file only. End users run `pip install` on that file — see **[CLIENT.md](CLIENT.md)** or **[CLIENT_USER_GUIDE.md](CLIENT_USER_GUIDE.md)**.

**Optional:** a short note listing required environment variables (or point them at **CLIENT_USER_GUIDE.md**):

| Variable | Purpose |
|----------|---------|
| `TESTRAIL_URL` | TestRail base URL |
| `TESTRAIL_USER` | Login email or username |
| `TESTRAIL_API_KEY` | API key from TestRail (My Settings → API Key) |

Do **not** email real API keys. Each user uses **their own** TestRail credentials.

---

## 4. Version bumps (when you release again)

1. Edit **`pyproject.toml`**: bump `[project]` `version = "…"`.
2. Rebuild: `python -m build --wheel`.
3. Send the new `.whl`. Users can `pip install --upgrade path\to\new.whl`.

---

## 5. Other distribution options (advanced)

| Method | Notes |
|--------|--------|
| **Private PyPI / internal index** | Upload the wheel; users `pip install testrail-mcp==x.y.z --index-url …`. See [DEPLOYMENT.md](DEPLOYMENT.md). |
| **HTTP transport on a host** | Run with `TESTRAIL_MCP_TRANSPORT=http` behind TLS + auth if exposed beyond localhost. Clients must support Streamable HTTP. Not ideal if **only** your laptop is online intermittently — prefer **wheel on each user’s PC**. |

---

## 6. Security checklist

- Never commit **`.env`** or real **`TESTRAIL_API_KEY`** values.
- Prefer **private** channels (internal share, encrypted transfer) for the `.whl` if the artifact is sensitive.
- Remind users: **API keys belong in their Cursor `env` or local `.env`**, not in screenshots or chat logs.

---

## Client wiki (`WIKI_CLIENT.md`) — maintainers

[`docs/WIKI_CLIENT.md`](WIKI_CLIENT.md) is **client-only** (no links to other repo docs). If [`testrail_mcp/data/tools_spec.json`](../testrail_mcp/data/tools_spec.json) changes, refresh the alphabetical list in **§8.1**:

```bash
python scripts/gen_wiki_tool_list.py
```

Paste the script output over the bullet list in **`WIKI_CLIENT.md`** (section **8.1 Full tool list**).

---

## Behavior notes

### Pagination defaults

Bulk list tools return TestRail's paginated envelope (`offset`, `limit`, `size`, `_links`).
For reliability the server injects a default `limit` of **250** (TestRail's max page size)
on these methods when the caller does not supply one: `getCases`, `getSections`, `getRuns`,
`getPlans`, `getMilestones`, `getTests`, `getResults`, `getResultsForCase`,
`getResultsForRun`, `getSharedSteps`.

- To page through a large collection, pass `limit` and/or `offset` explicitly — your values
  are forwarded unchanged and are never overridden.
- Single-record reads (`getSuite`, `getSection`, `getCase`) and the non-paginated
  `getSuites` never receive an injected `limit`.
- Query parameters are appended to TestRail's `index.php?` URL joined with `&` (not a
  second `?`); the client never uses httpx `params=`. A second `?` makes TestRail mis-parse
  the first parameter ("Unknown controller") and return a 404 or empty-body 500.

### `.env` encoding

The settings loader reads `.env` with `utf-8-sig`, so a file saved with a UTF-8 byte-order
mark (common when editing on Windows) is parsed correctly. Real environment variables take
precedence over `.env` entries; unrecognized variables are ignored.

---

## Related docs

- **[CLIENT.md](CLIENT.md)** — install wheel + Cursor (end users, full repo docs)
- **[CLIENT_USER_GUIDE.md](CLIENT_USER_GUIDE.md)** — same audience, self-contained; **included in the client ZIP** as the only `docs/` file
- **[DEPLOYMENT.md](DEPLOYMENT.md)** — full reference (stdio, HTTP, troubleshooting)
- **[STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md)** — setup when you **do** have the source tree locally
