# Contributing

Thanks for your interest in contributing. This guide covers setup, the local
workflow, and the checks that should pass before a pull request is merged.

## Prerequisites

- Python 3.10+
- Git

## Setup

```bash
git clone <your-fork-url>
cd TestRailMCP
python -m venv .venv
# Windows: .venv\Scripts\activate   |   macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"       # or: pip install -r requirements.txt
cp .env.example .env          # fill in your TestRail base URL + credentials
```

## Local workflow

- Run the MCP server per the README.
- `pytest` — run the test suite
- `pytest --cov` — run tests with coverage

## Before opening a pull request

Run and confirm these pass locally:

```bash
pytest --cov
```

If a linter (ruff/flake8) is configured, run it too.

## Pull request conventions

- Branch from `main` using a descriptive name (`fix/...`, `feat/...`, `docs/...`).
- Keep changes focused; one logical change per PR.
- Write a clear PR description: what changed, why, and how you tested it.
- Never commit `.env` or credentials. This server talks to a real TestRail
  instance — keep the base URL and API key in `.env` (git-ignored); see
  `.env.example`. Never paste credentials into issues, logs, or commits.
- Ensure CI is green before requesting review.

## Reporting issues

Use the issue templates. For security problems, follow [SECURITY.md](SECURITY.md)
instead of opening a public issue.
