# Client — install testrail-mcp (wheel) and use Cursor

This guide is for **end users** (e.g. PersonA) who received a **`testrail_mcp-…-py3-none-any.whl`** file and **do not** have the git repository.

**If you received the `testrail-mcp-client-*.zip` bundle**, use **[CLIENT_USER_GUIDE.md](CLIENT_USER_GUIDE.md)** — it is the only doc included in that ZIP (self-contained, no publisher steps).

**“Client”** here means **your machine + Cursor** talking to the MCP over **stdio**. Your **TestRail** site is separate (hosted by TestRail).

**Publishers** build the wheel using **[SERVER.md](SERVER.md)**.

### If you received `testrail-mcp-client-*.zip`

1. Unzip to any folder (e.g. Desktop).
2. **Windows:** double-click **`INSTALL.cmd`**. **macOS/Linux:** `chmod +x INSTALL.sh && ./INSTALL.sh`.
3. Open **`README-FIRST.txt`**, then follow **`docs/CLIENT_USER_GUIDE.md`** using the **`.venv`** Python inside the unzipped folder for Cursor’s **`command`** (see §4 below for the same JSON patterns).

---

## Prerequisites

- **Python 3.11 or any newer 3.x** (3.12, 3.13, …) — [python.org](https://www.python.org/downloads/) (Windows: enable **Add Python to PATH**).
- The **`.whl`** file from your team.
- A **TestRail** account with API access: base **URL**, **login email** (or username), and **API Key** from **My Settings → API Key**.

---

## 1. Save the wheel

Put the file somewhere stable, for example:

- Windows: `C:\Users\YourName\packages\testrail_mcp-0.1.0-py3-none-any.whl`
- macOS/Linux: `~/packages/testrail_mcp-0.1.0-py3-none-any.whl`

The exact version in the filename may differ.

---

## 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
cd $HOME
python -m venv testrail-mcp-venv
.\testrail-mcp-venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv ~/testrail-mcp-venv
source ~/testrail-mcp-venv/bin/activate
```

---

## 3. Install the package

```bash
pip install --upgrade pip
pip install "C:\path\to\testrail_mcp-0.1.0-py3-none-any.whl"
```

Use your **real** path and filename inside the quotes.

---

## 4. Configure Cursor (recommended: `env` in MCP JSON)

1. Open **Cursor → Settings → MCP** (wording may vary by version) and edit the JSON.
2. Add a server that uses the **venv Python** from step 2 and passes TestRail settings.

**Windows example** — adjust paths and secrets:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "C:\\Users\\YourName\\testrail-mcp-venv\\Scripts\\python.exe",
      "args": ["-m", "testrail_mcp"],
      "env": {
        "TESTRAIL_MCP_TRANSPORT": "stdio",
        "TESTRAIL_URL": "https://your-company.testrail.io",
        "TESTRAIL_USER": "you@company.com",
        "TESTRAIL_API_KEY": "your-testrail-api-key"
      }
    }
  }
}
```

**macOS / Linux example:**

```json
{
  "mcpServers": {
    "testrail": {
      "command": "/Users/YourName/testrail-mcp-venv/bin/python",
      "args": ["-m", "testrail_mcp"],
      "env": {
        "TESTRAIL_MCP_TRANSPORT": "stdio",
        "TESTRAIL_URL": "https://your-company.testrail.io",
        "TESTRAIL_USER": "you@company.com",
        "TESTRAIL_API_KEY": "your-testrail-api-key"
      }
    }
  }
}
```

3. Save, then **restart Cursor** or reload MCP.

**Finding `python.exe`:** In the activated venv, run `where python` (Windows) or `which python` (macOS/Linux).

---

## 5. Optional: credentials in `.env` instead of Cursor

If you prefer not to store secrets in Cursor’s JSON:

1. Create a folder, e.g. `C:\Users\YourName\testrail-mcp-config`.
2. Create a file **`.env`** in that folder with:

   ```env
   TESTRAIL_URL=https://your-company.testrail.io
   TESTRAIL_USER=you@company.com
   TESTRAIL_API_KEY=your-testrail-api-key
   TESTRAIL_MCP_TRANSPORT=stdio
   ```

3. In MCP JSON, use **`command`** + **`args`** only, and set **`cwd`** to that folder (the app loads `.env` from the process working directory):

```json
{
  "mcpServers": {
    "testrail": {
      "command": "C:\\Users\\YourName\\testrail-mcp-venv\\Scripts\\python.exe",
      "args": ["-m", "testrail_mcp"],
      "cwd": "C:\\Users\\YourName\\testrail-mcp-config"
    }
  }
}
```

---

## 6. Verify

1. MCP panel shows **testrail** connected.
2. Ask the agent to run **`TestRail_API_getProjects`** or to list TestRail projects.

If something fails, see **[DEPLOYMENT.md — Troubleshooting](DEPLOYMENT.md#troubleshooting)**.

---

## Security

- Do **not** commit or share your **`.env`** or API key in public channels.
- Rotate the TestRail API key if it was exposed.

---

## Related docs

- **[SERVER.md](SERVER.md)** — how the wheel is built (publishers)
- **[DEPLOYMENT.md](DEPLOYMENT.md)** — transports, HTTP, full troubleshooting
- **[GITHUB_COPY.md](GITHUB_COPY.md)** — extra MCP JSON patterns (if you later use a git clone)
