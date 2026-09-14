# TestRail MCP — client wiki page

This page is **self-contained** for **end users**: paste it into your internal wiki (Confluence, Notion, SharePoint, etc.). You do not need any other documentation file to install and use TestRail MCP with **Cursor**.

**Terminology:** **Client** means your PC and **Cursor** (or another MCP host) talking to this MCP over **stdio**. **TestRail** is your company’s TestRail site.

**Python:** **3.11** minimum; **all newer CPython 3.x** (3.12, 3.13, …) are supported.

---

## 1. What this is

- **TestRail MCP** exposes your TestRail **REST API v2** as **MCP tools** so an AI assistant in **Cursor** can list projects, read cases, add results, and more—subject to the user’s TestRail permissions.
- **Transport:** typically **stdio** (local process). You provide **TestRail URL**, **user**, and **API key** via environment variables or a `.env` file.

---

## 2. What you need

| Item | Notes |
|------|--------|
| **TestRail URL** | Base URL, e.g. `https://yourcompany.testrail.io` |
| **TestRail user** | Login email or username |
| **API key** | **My Settings → API Key** in TestRail |
| **Install** | Client ZIP or `.whl` from your team — follow **§3** below |
| **Cursor** | MCP server entry with venv `python` and `python -m testrail_mcp` |

---

## 3. Install and configure Cursor

### 3.1 If you received a client ZIP bundle

1. Unzip to any folder (for example Desktop).
2. **Windows:** double-click **`INSTALL.cmd`**. **macOS / Linux:** `chmod +x INSTALL.sh && ./INSTALL.sh`.
3. That creates **`.venv`** in the folder and installs the package from the **`wheel/`** folder.
4. Configure Cursor using **§3.3**; set **`command`** to the **`.venv`** Python inside that folder.

### 3.2 If you only have a `.whl` file

1. Install **Python 3.11 or any newer 3.x** from `https://www.python.org/downloads/` (Windows: enable **Add Python to PATH**).
2. Create a virtual environment and install the wheel (use the path your team gives you):

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

3. Continue with **§3.3** using that venv’s `python` path for **`command`**.

### 3.3 Cursor MCP (recommended: `env` in JSON)

1. Open **Cursor → Settings → MCP** and edit the JSON (labels vary by version).
2. Set **`command`** to your **venv Python**, **`args`** to `["-m", "testrail_mcp"]`, and **`env`** with your TestRail variables.

**Windows example** (adjust paths to your folder):

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

### 3.4 Optional: credentials in `.env` instead of Cursor

1. Copy **`.env.example`** to **`.env`** in a config folder (or the unzipped bundle folder).
2. Fill in `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY`, and `TESTRAIL_MCP_TRANSPORT=stdio`.
3. In MCP JSON use **`command`** + **`args`** only, and set **`cwd`** to the folder that contains **`.env`:**

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

## 4. Environment variables

| Variable | Required | Description |
|----------|------------|-------------|
| `TESTRAIL_URL` | Yes | TestRail base URL |
| `TESTRAIL_USER` | Yes | Email or username |
| `TESTRAIL_API_KEY` | Yes | API key / PAT from TestRail |
| `TESTRAIL_MCP_TRANSPORT` | For Cursor | `stdio` |
| `TESTRAIL_REQUEST_TIMEOUT_SECONDS` | No | Default `60` |

| `env` key (in MCP JSON) | Meaning |
|-----------|---------|
| `TESTRAIL_URL` | TestRail base URL |
| `TESTRAIL_USER` | Email or username |
| `TESTRAIL_API_KEY` | API key from TestRail |
| `TESTRAIL_MCP_TRANSPORT` | Use `stdio` for Cursor |

---

## 5. Verify

1. MCP shows the **testrail** server as connected.
2. Ask the assistant to run **`TestRail_API_getProjects`** or to list TestRail projects.

---

## 6. Troubleshooting

| Issue | What to check |
|-------|----------------|
| “Missing or invalid configuration” / startup error | Set `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY` (names and spelling). |
| Wrong TestRail instance or old URL | Values in Cursor **`env`** may override **`.env`**. Align both or use only one method. |
| Windows: `testrail-mcp` not found | Use **`python -m testrail_mcp`** via the venv **`command`** path (as in the JSON above). |
| MCP connects but tools fail / empty | Invalid API key; no network to TestRail; VPN/firewall blocking HTTPS. |
| Path errors after moving the install folder | Update **`command`** (and **`cwd`** if used) to the new location. |
| **`INSTALL.cmd`**: “Python not found” but Python works elsewhere | **cmd.exe** may not see the same **PATH** as PowerShell. On Windows, **`py -3 --version`** in **cmd** helps confirm; install Python from `https://www.python.org/downloads/` with **Add python.exe to PATH**, or run **`py -3 -m venv .venv`**, activate, then **`pip install wheel\*.whl`**. |

---

## 7. Security

- Do **not** share your **`.env`** or **API key** in chat, screenshots, or public tickets.
- Rotate the TestRail API key if it may have been exposed.

---

## 8. MCP tools (90)

The MCP server exposes **90** tools aligned with the TestRail API. Names follow `TestRail_API_<Operation>`. The authoritative names are listed below.

### 8.1 Full tool list (alphabetical)

- `TestRail_API_addAttachmentToCase`
- `TestRail_API_addAttachmentToPlan`
- `TestRail_API_addAttachmentToPlanEntry`
- `TestRail_API_addAttachmentToResult`
- `TestRail_API_addAttachmentToRun`
- `TestRail_API_addCase`
- `TestRail_API_addConfig`
- `TestRail_API_addConfigGroup`
- `TestRail_API_addMilestone`
- `TestRail_API_addPlan`
- `TestRail_API_addPlanEntry`
- `TestRail_API_addResult`
- `TestRail_API_addResultForCase`
- `TestRail_API_addResults`
- `TestRail_API_addResultsForCases`
- `TestRail_API_addRun`
- `TestRail_API_addRunToPlanEntry`
- `TestRail_API_addSection`
- `TestRail_API_addSharedStep`
- `TestRail_API_addSuite`
- `TestRail_API_addUser`
- `TestRail_API_closePlan`
- `TestRail_API_closeRun`
- `TestRail_API_copyCasesToSection`
- `TestRail_API_deleteCase`
- `TestRail_API_deleteCasesBySuite`
- `TestRail_API_deleteConfig`
- `TestRail_API_deleteConfigGroup`
- `TestRail_API_deleteMilestone`
- `TestRail_API_deleteRun`
- `TestRail_API_deleteSection`
- `TestRail_API_deleteSharedStep`
- `TestRail_API_deleteSuite`
- `TestRail_API_getAttachment`
- `TestRail_API_getAttachmentsForCase`
- `TestRail_API_getAttachmentsForPlan`
- `TestRail_API_getAttachmentsForPlanEntry`
- `TestRail_API_getAttachmentsForRun`
- `TestRail_API_getAttachmentsForTest`
- `TestRail_API_getCase`
- `TestRail_API_getCaseFields`
- `TestRail_API_getCaseHistory`
- `TestRail_API_getCaseStatuses`
- `TestRail_API_getCaseTypes`
- `TestRail_API_getCases`
- `TestRail_API_getConfigs`
- `TestRail_API_getCurrentUser`
- `TestRail_API_getMilestone`
- `TestRail_API_getMilestones`
- `TestRail_API_getPlan`
- `TestRail_API_getPlans`
- `TestRail_API_getPriorities`
- `TestRail_API_getProjects`
- `TestRail_API_getResultFields`
- `TestRail_API_getResults`
- `TestRail_API_getResultsForCase`
- `TestRail_API_getResultsForRun`
- `TestRail_API_getRun`
- `TestRail_API_getRuns`
- `TestRail_API_getSection`
- `TestRail_API_getSections`
- `TestRail_API_getSharedStep`
- `TestRail_API_getSharedStepHistory`
- `TestRail_API_getSharedSteps`
- `TestRail_API_getStatuses`
- `TestRail_API_getSuite`
- `TestRail_API_getSuites`
- `TestRail_API_getTemplates`
- `TestRail_API_getTest`
- `TestRail_API_getTests`
- `TestRail_API_getUser`
- `TestRail_API_getUserByEmail`
- `TestRail_API_getUsers`
- `TestRail_API_getUsersByProject`
- `TestRail_API_moveCasesToSection`
- `TestRail_API_moveSection`
- `TestRail_API_updateCase`
- `TestRail_API_updateCasesByCaseId`
- `TestRail_API_updateCasesBySuite`
- `TestRail_API_updateConfig`
- `TestRail_API_updateConfigGroup`
- `TestRail_API_updateMilestone`
- `TestRail_API_updatePlan`
- `TestRail_API_updatePlanEntry`
- `TestRail_API_updateRun`
- `TestRail_API_updateRunToPlanEntry`
- `TestRail_API_updateSection`
- `TestRail_API_updateSharedStep`
- `TestRail_API_updateSuite`
- `TestRail_API_updateUser`

### 8.2 By rough category (for browsing)

| Category | Example tools |
|----------|----------------|
| **Projects & meta** | `TestRail_API_getProjects`, `TestRail_API_getTemplates`, `TestRail_API_getPriorities`, `TestRail_API_getStatuses`, `TestRail_API_getCaseTypes` |
| **Suites & sections & cases** | `TestRail_API_getSuites`, `TestRail_API_getSections`, `TestRail_API_getCases`, `TestRail_API_getCase`, `TestRail_API_addCase`, `TestRail_API_updateCase` |
| **Runs & tests & results** | `TestRail_API_getRuns`, `TestRail_API_getTests`, `TestRail_API_getTest`, `TestRail_API_addRun`, `TestRail_API_addResult`, `TestRail_API_getResults` |
| **Plans & milestones** | `TestRail_API_getPlans`, `TestRail_API_getPlan`, `TestRail_API_addPlan`, `TestRail_API_getMilestones`, `TestRail_API_addMilestone` |
| **Users** | `TestRail_API_getCurrentUser`, `TestRail_API_getUsers`, `TestRail_API_getUser` |
| **Attachments** | `TestRail_API_getAttachmentsForCase`, `TestRail_API_addAttachmentToCase`, … |

---

## 9. Example prompts (natural language)

Use these patterns in Cursor; the assistant should pick the right **tool** and IDs. Replace placeholders with real values from your instance. You can phrase requests in everyday language—the assistant maps them to tools.

### Discovery & read

| Example ask | Typical tool(s) |
|-------------|-----------------|
| “List all TestRail projects I can see.” | `TestRail_API_getProjects` |
| “Show suites for project ID 3.” | `TestRail_API_getSuites` |
| “Get test case 12345 including steps.” | `TestRail_API_getCase` |
| “List tests in run 987.” | `TestRail_API_getTests` |
| “What’s the status of test 555 in run 987?” | `TestRail_API_getTest` |

### Runs & results

| Example ask | Typical tool(s) |
|-------------|-----------------|
| “Create a new test run for project 1, suite 2.” | `TestRail_API_addRun` |
| “Mark test 555 in run 987 as passed with comment ‘Smoke OK’.” | `TestRail_API_addResult` / `TestRail_API_addResultForCase` |
| “Submit results for multiple cases in one call for run 987.” | `TestRail_API_addResultsForCases` |

### Plans & organization

| Example ask | Typical tool(s) |
|-------------|-----------------|
| “List open test plans for project 3.” | `TestRail_API_getPlans` |
| “Add a milestone ‘Sprint 12’ to project 3.” | `TestRail_API_addMilestone` |

### Users

| Example ask | Typical tool(s) |
|-------------|-----------------|
| “Who am I in TestRail?” | `TestRail_API_getCurrentUser` |
| “Look up user by email jane@company.com.” | `TestRail_API_getUserByEmail` |

---

## 10. Extra phrasing tips

Ask for **IDs** when needed (“use project ID 5”, “run 1001”). If the assistant picks the wrong tool, name the tool from **§8** explicitly (e.g. “Call `TestRail_API_getRuns` for project 3”).
