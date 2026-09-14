@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo ========================================
echo  TestRail MCP - client install (Windows)
echo ========================================
echo.

set "PYTHON_EXE="

REM 1) Python Launcher first: picks the real Python 3.x install (minimum 3.11; any newer 3.x OK)
REM    Avoids taking "python" from PATH first — the Microsoft Store stub in WindowsApps
REM    often appears first and fails in cmd.exe even when python.org 3.13 is installed.
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
  for /f "usebackq delims=" %%P in (`py -3 -c "import sys; print(sys.executable)" 2^>nul`) do (
    set "PYTHON_EXE=%%P"
    goto :have_python
  )
)

REM 2) python.exe on PATH (first match)
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
  for /f "usebackq delims=" %%P in (`where python`) do (
    set "PYTHON_EXE=%%P"
    goto :have_python
  )
)

REM 3) python3 (some installs)
where python3 >nul 2>&1
if %ERRORLEVEL% equ 0 (
  for /f "usebackq delims=" %%P in (`where python3`) do (
    set "PYTHON_EXE=%%P"
    goto :have_python
  )
)

echo ERROR: Python not found for this Command Prompt.
echo.
echo Fix: install Python 3.11 or any newer 3.x from https://www.python.org/downloads/
echo   with "Add python.exe to PATH", or run this script from a terminal where "py -3 --version" works.
echo.
pause
exit /b 1

:have_python
echo Using: "%PYTHON_EXE%"
"%PYTHON_EXE%" --version
if errorlevel 1 (
  echo ERROR: Python failed to run.
  pause
  exit /b 1
)

"%PYTHON_EXE%" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" 2>nul
if errorlevel 1 (
  echo ERROR: Python 3.11 or newer is required. This package supports all CPython 3.x releases from 3.11 upward.
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
  "%PYTHON_EXE%" -m venv .venv
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
