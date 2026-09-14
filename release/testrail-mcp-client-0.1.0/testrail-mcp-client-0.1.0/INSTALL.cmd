@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo ========================================
echo  TestRail MCP - client install (Windows)
echo ========================================
echo.

where py >nul 2>&1
if %ERRORLEVEL%==0 (
  py -3.11 --version >nul 2>&1 && (set "PY=py -3.11") || (set "PY=py -3")
) else (
  set "PY=python"
)

echo Using: %PY%
%PY% --version
if errorlevel 1 (
  echo ERROR: Python not found. Install Python 3.11+ from https://www.python.org/downloads/
  echo Enable "Add Python to PATH" on Windows.
  pause
  exit /b 1
)

if not exist "wheel\*.whl" (
  echo ERROR: No .whl file in wheel\
  pause
  exit /b 1
)

if not exist ".venv" (
  echo Creating virtual environment .venv ...
  %PY% -m venv .venv
)

call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
for %%f in (wheel\*.whl) do (
  echo Installing %%f
  python -m pip install "%%f"
)

echo.
echo Done. Next: open docs\CLIENT_USER_GUIDE.md and configure Cursor MCP.
echo Optional: copy .env.example to .env in this folder for credential file mode.
echo.
pause
