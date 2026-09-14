# Step-by-step setup (local machine + Cursor + TestRail)

You **do not need GitHub**. If the project is already on your PC (folder, zip extract, USB copy, internal share), start at **Part A** and point Cursor’s **`cwd`** at that folder.

**Optional:** Push or clone from GitHub only if you want a remote backup or to share the repo — see **Optional — GitHub** at the end (and [GITHUB_COPY.md](GITHUB_COPY.md)).

**What you need from TestRail:** site **URL**, your **email** (login), and **API Key** (PAT) from **My Settings → API Key** → map to `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY`.

---

## Part A — One-time setup on your computer

### Step 1 — Python 3.11 or newer (3.12, 3.13, …)

```bash
python --version
```

### Step 2 — Project folder on this machine

**Typical (no Git):** open a terminal and go to the folder that contains **`pyproject.toml`** (your copy of TestRailMCP):

```bash
cd C:/path/to/TestRailMCP
```

Use your real path (Windows, WSL, or macOS/Linux). Example Windows:

```powershell
cd C:\Users\YourName\Projects\TestRailMCP
```

**If you use Git and already cloned:** same idea — `cd` into the clone directory.

**If you only have a `.zip`:** extract it, then `cd` into the extracted root (where `pyproject.toml` lives).

### Step 3 — Virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4 — Install

```bash
pip install -e .
```

### Step 5 — TestRail credentials

1. Open TestRail in the browser; note **base URL**.
2. Use your login **email** → `TESTRAIL_USER`.
3. **My Settings → API Key** → copy key → `TESTRAIL_API_KEY` (your PAT).

---

## Part B — Cursor MCP configuration (required)

Set **`command`** (venv Python), **`args`**: `["-m", "testrail_mcp"]`, **`cwd`** (repo root — the same folder as **Step 2**), and **`env`** with TestRail variables.

**Where:** Cursor **Settings → MCP** → edit JSON (exact UI varies by version).

### Windows template

Replace paths with your **local** project folder, plus URL, email, PAT:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "C:/Users/YOUR_USER/path/TestRailMCP/.venv/Scripts/python.exe",
      "args": ["-m", "testrail_mcp"],
      "cwd": "C:/Users/YOUR_USER/path/TestRailMCP",
      "env": {
        "TESTRAIL_MCP_TRANSPORT": "stdio",
        "TESTRAIL_URL": "https://your-company.testrail.io",
        "TESTRAIL_USER": "your.email@company.com",
        "TESTRAIL_API_KEY": "paste-your-PAT-here"
      }
    }
  }
}
```

### macOS / Linux template

```json
{
  "mcpServers": {
    "testrail": {
      "command": "/Users/YOUR_USER/path/TestRailMCP/.venv/bin/python",
      "args": ["-m", "testrail_mcp"],
      "cwd": "/Users/YOUR_USER/path/TestRailMCP",
      "env": {
        "TESTRAIL_MCP_TRANSPORT": "stdio",
        "TESTRAIL_URL": "https://your-company.testrail.io",
        "TESTRAIL_USER": "your.email@company.com",
        "TESTRAIL_API_KEY": "paste-your-PAT-here"
      }
    }
  }
}
```

| `env` key | Value |
|-----------|--------|
| `TESTRAIL_URL` | TestRail site URL |
| `TESTRAIL_USER` | Your email / username |
| `TESTRAIL_API_KEY` | API Key (PAT) from TestRail |
| `TESTRAIL_MCP_TRANSPORT` | `stdio` for Cursor |

Restart Cursor or reload MCP after saving.

**Security:** Do not commit real PATs. Do not paste live secrets into public issues.

---

## Part C — Optional: `.env` instead of MCP `env`

1. `cp .env.example .env` (or `copy` on Windows) and fill `TESTRAIL_*`.
2. MCP config with **only** `command`, `args`, `cwd` (no `env` block) — see **[GITHUB_COPY.md](GITHUB_COPY.md)**.

If both `.env` and MCP `env` set the same variable, the process environment from Cursor often wins.

---

## Part D — Verify

1. MCP panel: **testrail** connected.
2. Try tool **`TestRail_API_getProjects`** or ask the agent to list projects.

Problems: [DEPLOYMENT.md — Troubleshooting](DEPLOYMENT.md#troubleshooting).

---

## Optional — Terminal check

```bash
python -c "from testrail_mcp.settings import Settings; s=Settings(); print('OK:', s.url)"
```

---

## Optional — HTTP transport

[DEPLOYMENT.md — HTTP](DEPLOYMENT.md#running--http-streamable-http)

---

## Optional — GitHub (only if you want a remote repo)

Skip entirely if you are **local-only**.

### Clone from an existing GitHub URL

```bash
git clone https://github.com/SOME_USER/TestRailMCP.git
cd TestRailMCP
```

Then continue from **Part A — Step 3** (venv).

### First-time push to a new personal repo

- Do **not** commit **`.env`** (secrets). Only **`.env.example`** belongs in git.
- Do **not** commit `.venv/`, `dist/`, or caches — see **`.gitignore`**.
- Save **`pyproject.toml`** as **UTF-8 without BOM** (see [DEPLOYMENT.md — Troubleshooting](DEPLOYMENT.md#troubleshooting)).

In the project root (`pyproject.toml` present):

```bash
git init
git branch -M main
git add .
git status
```

Confirm **`.env`** is not listed. If it is: `git reset HEAD .env` and keep `.env` only on your machine.

```bash
git commit -m "Initial commit: testrail-mcp"
```

On [GitHub](https://github.com/new): create a **new empty** repository (e.g. **`TestRailMCP`**). Do not add a README if this folder already has files.

```bash
git remote add origin https://github.com/YOUR_USERNAME/TestRailMCP.git
git push -u origin main
```

Use **SSH** if you prefer: `git@github.com:YOUR_USERNAME/TestRailMCP.git`

**Optional — GitHub CLI:** `gh repo create TestRailMCP --private --source=. --remote=origin --push`

For **ready-to-copy** remote lines, see **[GITHUB_COPY.md](GITHUB_COPY.md)**.

---

## Related docs

- [DEPLOYMENT.md](DEPLOYMENT.md) — full reference  
- [GITHUB_COPY.md](GITHUB_COPY.md) — Git + MCP snippets  
- [MCP_SERVER_REFERENCE_PROMPT.md](MCP_SERVER_REFERENCE_PROMPT.md) — reuse for other MCP projects (prompts, wikis)  
