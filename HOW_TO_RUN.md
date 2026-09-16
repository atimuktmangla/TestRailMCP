# How to run

TestRail Model Context Protocol (MCP) server (Python). Exposes TestRail to MCP
clients over stdio or Streamable HTTP.

## Prerequisites

- Python 3.11+
- TestRail connection settings via `TESTRAIL_*` environment variables:
  `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY` (see `.env.example` and
  `docs/DEPLOYMENT.md`).

## Install

Install the package (editable) from the repo root:

```bash
pip install -e .
```

(There is no `requirements.txt`; dependencies are declared in `pyproject.toml`.)

## Run

```bash
python -m testrail_mcp            # stdio transport (for local MCP clients)
python -m testrail_mcp --http     # Streamable HTTP transport
```

`run.cmd` (Windows) installs the package and starts the stdio server.

## Test

```bash
pytest                            # 20 tests (routing / request building)
```

## Build a distributable client bundle

```bash
python scripts/build_client_release.py   # produces the release/ ZIP + wheel
```

See `docs/SERVER.md` and `docs/DEPLOYMENT.md` for full install/registration
reference.
