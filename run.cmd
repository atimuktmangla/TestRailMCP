@echo off
REM ============================================================
REM  TestRail MCP Server - launcher (Windows)
REM  Starts the stdio MCP server.
REM  Requires Python 3.11+ and TESTRAIL_URL / TESTRAIL_USER /
REM  TESTRAIL_API_KEY in the environment (or a .env you load).
REM ============================================================
setlocal
cd /d "%~dp0"

python -c "import testrail_mcp" 1>nul 2>nul
if errorlevel 1 (
  echo [setup] Installing the testrail_mcp package ^(editable^)...
  python -m pip install -e . || goto :err
) else (
  echo [setup] Package already installed - skipping install.
)

echo [start] Starting TestRail MCP server (stdio transport)...
python -m testrail_mcp
goto :eof

:err
echo [ERROR] Install failed. Ensure Python 3.11+ is on PATH.
exit /b 1
