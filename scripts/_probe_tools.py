"""Dev probe: print the TestRail MCP tool count and any case/section/suite tools.

Run from anywhere: resolves the spec file relative to the repo root, not cwd.
"""
import json
import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
spec_path = REPO_ROOT / "testrail_mcp" / "data" / "tools_spec.json"
s = json.loads(spec_path.read_text(encoding="utf-8"))
print("TOOL_COUNT", len(s))
for t in s:
    if re.search("case|section|suite", t["name"], re.I):
        print(t["name"])
