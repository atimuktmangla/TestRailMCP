#!/usr/bin/env python3
"""Build release/testrail-mcp-client-VERSION.zip for end users (wheel + docs + INSTALL scripts)."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
RELEASE = ROOT / "release"
STAGING_NAME = "staging-client-bundle"


def _version() -> str:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8-sig"))
    return str(data["project"]["version"])


def _ensure_wheel(version: str) -> Path:
    wheels = sorted(DIST.glob("testrail_mcp-*-py3-none-any.whl"))
    if not wheels:
        print("No wheel in dist/. Building...", file=sys.stderr)
        subprocess.run(
            [sys.executable, "-m", "build", "--wheel"],
            cwd=ROOT,
            check=True,
        )
        wheels = sorted(DIST.glob("testrail_mcp-*-py3-none-any.whl"))
    if not wheels:
        raise SystemExit("Build failed: no testrail_mcp-*-py3-none-any.whl in dist/")
    whl = wheels[-1]
    if version not in whl.name:
        print(
            f"Warning: wheel {whl.name} may not match pyproject version {version}",
            file=sys.stderr,
        )
    return whl


def _write_readme_first(version: str, out: Path) -> None:
    text = f"""TestRail MCP — client bundle (v{version})

Requires Python 3.11 or newer — any CPython 3.x from 3.11 upward (3.12, 3.13, …).

Quick start (Windows)
---------------------
1. Double-click INSTALL.cmd, or open PowerShell here and run: .\\INSTALL.cmd
2. Read docs\\\\CLIENT_USER_GUIDE.md — add the MCP server in Cursor (venv Python + TESTRAIL_* env).
3. Optional: copy .env.example to .env and set your TestRail URL, user, and API key.

The installable package is in the wheel\\\\ folder (INSTALL.cmd installs it into .venv here).

macOS / Linux
-------------
Run: chmod +x INSTALL.sh && ./INSTALL.sh
Then follow docs/CLIENT_USER_GUIDE.md for Cursor.

Documentation
---------------
- docs/CLIENT_USER_GUIDE.md — full setup (Cursor, .env, troubleshooting)
"""
    out.write_text(text, encoding="utf-8")


def _write_install_cmd(out_dir: Path) -> None:
    # UTF-8 friendly; runs from bundle root.
    # Resolve PYTHON_EXE to a single path — do not store "py -3" in one variable (CMD splits on spaces).
    content = r"""@echo off
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
"""
    (out_dir / "INSTALL.cmd").write_text(content, encoding="utf-8")


def _write_install_sh(out_dir: Path) -> None:
    content = """#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "========================================"
echo " TestRail MCP - client install (Unix)"
echo "========================================"
echo
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Install Python 3.11 or any newer 3.x."
  exit 1
fi
python3 --version
python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" || {
  echo "ERROR: Python 3.11 or newer is required (3.12, 3.13, …)."
  exit 1
}
shopt -s nullglob
wheels=(wheel/*.whl)
if [ "${#wheels[@]}" -eq 0 ]; then
  echo "ERROR: No .whl file in wheel/"
  exit 1
fi
if [ ! -d .venv ]; then
  echo "Creating virtual environment .venv ..."
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
for f in wheel/*.whl; do
  echo "Installing $f"
  python -m pip install "$f"
done
echo
echo "Done. Next: read docs/CLIENT_USER_GUIDE.md and configure Cursor MCP."
echo "Optional: copy .env.example to .env in this folder."
"""
    p = out_dir / "INSTALL.sh"
    p.write_text(content, encoding="utf-8")
    p.chmod(p.stat().st_mode | 0o111)


def main() -> None:
    parser = argparse.ArgumentParser(description="Package client release ZIP under release/")
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Do not run 'python -m build' when dist/ has no wheel",
    )
    args = parser.parse_args()

    version = _version()
    RELEASE.mkdir(parents=True, exist_ok=True)
    staging = RELEASE / STAGING_NAME
    if staging.exists():
        shutil.rmtree(staging)
    bundle_root = staging / f"testrail-mcp-client-{version}"
    bundle_root.mkdir(parents=True)

    if args.skip_build and not any(DIST.glob("testrail_mcp-*-py3-none-any.whl")):
        raise SystemExit("dist/ has no wheel; run without --skip-build or build manually")

    whl = _ensure_wheel(version)
    wheel_dir = bundle_root / "wheel"
    wheel_dir.mkdir()
    shutil.copy2(whl, wheel_dir / whl.name)

    docs_out = bundle_root / "docs"
    docs_out.mkdir()
    user_guide = ROOT / "docs" / "CLIENT_USER_GUIDE.md"
    if not user_guide.is_file():
        raise SystemExit(f"Missing required doc for client bundle: {user_guide}")
    shutil.copy2(user_guide, docs_out / "CLIENT_USER_GUIDE.md")

    env_ex = ROOT / ".env.example"
    if env_ex.is_file():
        shutil.copy2(env_ex, bundle_root / ".env.example")

    _write_readme_first(version, bundle_root / "README-FIRST.txt")
    _write_install_cmd(bundle_root)
    _write_install_sh(bundle_root)

    zip_name = f"testrail-mcp-client-{version}.zip"
    zip_path = RELEASE / zip_name
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in bundle_root.rglob("*"):
            if path.is_file():
                arc = path.relative_to(staging)
                zf.write(path, arc.as_posix())

    shutil.rmtree(staging)
    print(f"Wrote {zip_path.relative_to(ROOT)} ({zip_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
