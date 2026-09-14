# GitHub + MCP — copy-paste reference

Replace **`YOUR_USERNAME`** with your **personal GitHub** username and adjust folder paths.

---

## 1. New personal repository (after `git commit`)

```text
https://github.com/YOUR_USERNAME/TestRailMCP
```

### Add remote and push (HTTPS)

```bash
git remote add origin https://github.com/YOUR_USERNAME/TestRailMCP.git
git branch -M main
git push -u origin main
```

### Add remote and push (SSH)

```bash
git remote add origin git@github.com:YOUR_USERNAME/TestRailMCP.git
git branch -M main
git push -u origin main
```

### Clone (on another machine)

```bash
git clone https://github.com/YOUR_USERNAME/TestRailMCP.git
cd TestRailMCP
```

---

## 2. Cursor MCP — Windows (stdio + `env`)

Replace paths, URL, email, PAT:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "C:/Users/YOUR_USERNAME/projects/TestRailMCP/.venv/Scripts/python.exe",
      "args": ["-m", "testrail_mcp"],
      "cwd": "C:/Users/YOUR_USERNAME/projects/TestRailMCP",
      "env": {
        "TESTRAIL_MCP_TRANSPORT": "stdio",
        "TESTRAIL_URL": "https://your-company.testrail.io",
        "TESTRAIL_USER": "your.email@company.com",
        "TESTRAIL_API_KEY": "your-testrail-api-key-here"
      }
    }
  }
}
```

---

## 3. Cursor MCP — macOS / Linux (stdio + `env`)

```json
{
  "mcpServers": {
    "testrail": {
      "command": "/Users/YOUR_USERNAME/projects/TestRailMCP/.venv/bin/python",
      "args": ["-m", "testrail_mcp"],
      "cwd": "/Users/YOUR_USERNAME/projects/TestRailMCP",
      "env": {
        "TESTRAIL_MCP_TRANSPORT": "stdio",
        "TESTRAIL_URL": "https://your-company.testrail.io",
        "TESTRAIL_USER": "your.email@company.com",
        "TESTRAIL_API_KEY": "your-testrail-api-key-here"
      }
    }
  }
}
```

---

## 4. Cursor MCP — credentials in `.env` only (no `env` in JSON)

Use after `cp .env.example .env` and editing `.env`.

**Windows:**

```json
{
  "mcpServers": {
    "testrail": {
      "command": "C:/Users/YOUR_USERNAME/projects/TestRailMCP/.venv/Scripts/python.exe",
      "args": ["-m", "testrail_mcp"],
      "cwd": "C:/Users/YOUR_USERNAME/projects/TestRailMCP"
    }
  }
}
```

**macOS / Linux:**

```json
{
  "mcpServers": {
    "testrail": {
      "command": "/Users/YOUR_USERNAME/projects/TestRailMCP/.venv/bin/python",
      "args": ["-m", "testrail_mcp"],
      "cwd": "/Users/YOUR_USERNAME/projects/TestRailMCP"
    }
  }
}
```

---

## 5. Minimum install commands (after clone)

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -e .
```

---

## Security

- Never commit **`.env`** or real **`TESTRAIL_API_KEY`** to GitHub.
- Prefer a **private** GitHub repo if the code or docs are internal.
