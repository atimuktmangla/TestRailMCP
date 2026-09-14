# Client release bundle

The file **`testrail-mcp-client-VERSION.zip`** in this folder is generated for end users: **wheel**, **client-only documentation**, **`INSTALL.cmd` / `INSTALL.sh`**, and **`.env.example`**.

## Generate the ZIP

From the repository root, with **Python 3.11 or any newer 3.x**:

```bash
pip install build
python scripts/build_client_release.py
```

This runs `python -m build --wheel` if `dist/` has no wheel, then writes **`release/testrail-mcp-client-<version>.zip`**.

Options:

- `--skip-build` — fail if `dist/` has no wheel (use when you already built manually).

## ZIP contents (client-only)

| Path | Purpose |
|------|--------|
| `wheel/` | `testrail_mcp-…-py3-none-any.whl` |
| `docs/CLIENT_USER_GUIDE.md` | Self-contained install, Cursor MCP, `.env`, troubleshooting (no publisher/git docs) |
| `.env.example` | Template for optional file-based credentials |
| `README-FIRST.txt` | Quick start after unzip |
| `INSTALL.cmd` | Windows: creates `.venv` and `pip install`s the wheel |
| `INSTALL.sh` | macOS/Linux: same |

Share the **`.zip`** with users who do not have the git repository. They unpack and follow **`README-FIRST.txt`** and **`docs/CLIENT_USER_GUIDE.md`**.
