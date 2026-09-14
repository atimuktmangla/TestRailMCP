# TestRail MCP — user guide (client install)

This guide is for **end users** installing **testrail-mcp** from a **wheel** or from the **`testrail-mcp-client-*.zip`** bundle. You do **not** need the source code repository.

**Terminology:** **Client** means your PC and **Cursor** (or another MCP host) talking to this MCP over **stdio**. **TestRail** is your company’s TestRail site (hosted by TestRail).

---

## If you received `testrail-mcp-client-*.zip`

1. Unzip to any folder (for example Desktop).
2. **Windows:** double-click **`INSTALL.cmd`**. **macOS / Linux:** `chmod +x INSTALL.sh && ./INSTALL.sh`.
3. That creates **`.venv`** next to **`README-FIRST.txt`** and installs the package from **`wheel/`**.
4. Configure **Cursor** using **§ Configure Cursor** below. Use the **`.venv`** Python inside this unzipped folder for **`command`** (see examples).

---

## If you only have a `.whl` file

1. Install **Python 3.11+** from [python.org](https://www.python.org/downloads/) (Windows: enable **Add Python to PATH**).
2. Create a virtual environment and install the wheel (see your team’s path to the file):

**Windows (PowerShell):**

```powershell
python -m venv testrail-mcp-venv
.\testrail-mcp-venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install "C:\path\to\testrail_mcp-0.1.0-py3-none-any.whl"
```

**macOS / Linux:**

```bash
python3 -m venv ~/testrail-mcp-venv
source ~/testrail-mcp-venv/bin/activate
pip install --upgrade pip
pip install "/path/to/testrail_mcp-0.1.0-py3-none-any.whl"
```

3. Continue with **§ Configure Cursor** using that venv’s `python`.

---

## Prerequisites (TestRail)

From TestRail you need:

| Variable | Source |
|----------|--------|
| `TESTRAIL_URL` | Your site base URL (no trailing slash), e.g. `https://company.testrail.io` |
| `TESTRAIL_USER` | Your login **email** or username |
| `TESTRAIL_API_KEY` | **My Settings → API Key** (API key / PAT) |

---

## Configure Cursor (recommended: `env` in MCP JSON)

1. Open **Cursor → Settings → MCP** and edit the JSON (exact labels vary by version).
2. Set **`command`** to your **venv `python`**, **`args`** to `["-m", "testrail_mcp"]`, and **`env`** with the variables above.

**Windows example** (ZIP layout: adjust the path to your unzipped folder):

```json
{
  "mcpServers": {
    "testrail": {
      "command": "C:\\Users\\YourName\\Desktop\\testrail-mcp-client-0.1.0\\.venv\\Scripts\\python.exe",
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
      "command": "/Users/YourName/Desktop/testrail-mcp-client-0.1.0/.venv/bin/python",
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

3. Save and **restart Cursor** or reload MCP.

**Find the venv Python:** With the venv activated, run `where python` (Windows) or `which python` (macOS/Linux).

| `env` key | Meaning |
|-----------|---------|
| `TESTRAIL_URL` | TestRail base URL |
| `TESTRAIL_USER` | Email or username |
| `TESTRAIL_API_KEY` | API key from TestRail |
| `TESTRAIL_MCP_TRANSPORT` | Use `stdio` for Cursor |

---

## Optional: credentials in `.env` instead of Cursor

1. Copy **`.env.example`** to **`.env`** in a folder you keep only for config (or in the unzipped bundle folder).
2. Fill in `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY`, and `TESTRAIL_MCP_TRANSPORT=stdio`.
3. In MCP JSON, use **`command`** + **`args`** only, and set **`cwd`** to the folder that contains **`.env`**:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "C:\\Users\\YourName\\path\\.venv\\Scripts\\python.exe",
      "args": ["-m", "testrail_mcp"],
      "cwd": "C:\\Users\\YourName\\path\\to\\folder-with-envfile"
    }
  }
}
```

If both **`.env`** and MCP **`env`** set the same variable, the process environment from Cursor usually wins.

---

## Verify

1. MCP panel shows **testrail** connected.
2. Ask the assistant to run **`TestRail_API_getProjects`** or to list TestRail projects.

---

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| “Missing or invalid configuration” / startup error | Set `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY` (names and spelling). |
| Wrong TestRail instance or old URL | Values in Cursor **`env`** may override **`.env`**. Align both or use only one method. |
| Windows: `testrail-mcp` not found | Use **`python -m testrail_mcp`** via the venv **`command`** path (as in the JSON above). |
| MCP connects but tools fail / empty | Invalid API key; no network to TestRail; VPN/firewall blocking HTTPS to your TestRail host. |
| Path errors after moving the ZIP | Update **`command`** (and **`cwd`** if used) to the new folder location. |

---

## Security

- Do **not** share your **`.env`** or **API key** in chat, screenshots, or public tickets.
- Rotate the TestRail API key if it may have been exposed.
