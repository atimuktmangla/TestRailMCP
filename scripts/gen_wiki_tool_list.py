"""Print alphabetical MCP tool bullets for docs/WIKI_CLIENT.md §6.1 (from tools_spec.json)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = json.loads((ROOT / "testrail_mcp/data/tools_spec.json").read_text(encoding="utf-8"))
for t in sorted(spec, key=lambda x: x["name"]):
    print(f"- `{t['name']}`")
