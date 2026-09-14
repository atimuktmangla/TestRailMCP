import json, pathlib, re
s = json.loads(pathlib.Path("testrail_mcp/data/tools_spec.json").read_text(encoding="utf-8"))
print("TOOL_COUNT", len(s))
for t in s:
    if re.search("case|section|suite", t["name"], re.I):
        print(t["name"])
