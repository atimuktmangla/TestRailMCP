# ADR-0004: Wheel + client-ZIP distribution

**Status:** Accepted

## Context

Two audiences consume this server: developers who build/publish it, and end
users who just want to install and point their MCP client at it — often with no
git repo and limited tooling. A single "clone the repo" story doesn't serve the
end user well.

## Decision

Distribute as a **wheel** (`python -m build`) plus a **self-contained client ZIP**
(`scripts/build_client_release.py` → `release/testrail-mcp-client-*.zip`)
containing the wheel, installers, and a standalone `CLIENT_USER_GUIDE.md`. Docs
are split publisher (`SERVER.md`) vs end user (`CLIENT.md`,
`CLIENT_USER_GUIDE.md`, `WIKI_CLIENT.md`).

## Alternatives considered

- **Repo-clone only.** Fine for developers, poor for non-technical end users.
- **PyPI only.** Good for `pip install`, but the ZIP bundles installers + a
  self-contained guide for locked-down environments and internal wikis.

## Trade-offs

- (+) End users install a wheel with a one-page guide; no repo needed.
- (+) Wiki-ready client doc for internal distribution.
- (−) The generated ZIP/wheel must **not** be committed to the repo (they're
  build output) — publish them via GitHub Releases. (Enforced: `release/`
  bundles are git-ignored; only `release/README.md` is tracked.)

## Consequences

- `release/` build artifacts are gitignored; regenerated on demand.
- Distribution docs are maintained per audience.
