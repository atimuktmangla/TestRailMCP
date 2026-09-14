"""MCP server exposing TestRail REST tools."""

from __future__ import annotations

import json
from importlib import resources
from typing import Any

import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from testrail_mcp import __version__
from testrail_mcp.client import TestRailClient
from testrail_mcp.routing import build_request_from_spec, tool_suffix_to_api_method


def _load_tool_specs() -> list[dict[str, Any]]:
    pkg = resources.files("testrail_mcp.data")
    raw = pkg.joinpath("tools_spec.json").read_text(encoding="utf-8")
    return json.loads(raw)


def _tool_read_only(tool_name: str) -> bool:
    suffix = tool_name.removeprefix("TestRail_API_")
    api_method = tool_suffix_to_api_method(suffix)
    return api_method.startswith("get_")


def build_server(testrail: TestRailClient) -> Server:
    specs = _load_tool_specs()
    by_name = {s["name"]: s for s in specs}

    server = Server(
        "testrail",
        version=__version__,
        instructions=(
            "TestRail API v2 bridge. Set TESTRAIL_URL, TESTRAIL_USER, and TESTRAIL_API_KEY. "
            "Attachment uploads expect body to be a local file path string (or dict with file_path)."
        ),
    )

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        out: list[types.Tool] = []
        for spec in specs:
            name = spec["name"]
            schema = spec.get("arguments") or {"type": "object", "properties": {}}
            out.append(
                types.Tool(
                    name=name,
                    description=spec.get("description"),
                    inputSchema=schema,
                    annotations=types.ToolAnnotations(readOnlyHint=_tool_read_only(name)),
                )
            )
        return out

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> types.CallToolResult:
        spec = by_name.get(name)
        if spec is None:
            return types.CallToolResult(
                content=[types.TextContent(type="text", text=f"Unknown tool: {name}")],
                isError=True,
            )
        suffix = name.removeprefix("TestRail_API_")
        api_method = tool_suffix_to_api_method(suffix)
        args_schema = spec.get("arguments") or {}
        required = list(args_schema.get("required") or [])
        properties = args_schema.get("properties") or {}
        try:
            prepared = build_request_from_spec(
                name,
                api_method,
                arguments,
                required=required,
                properties=properties,
            )
            result = await testrail.execute(prepared)
        except Exception as exc:
            return types.CallToolResult(
                content=[types.TextContent(type="text", text=str(exc))],
                isError=True,
            )
        text = json.dumps(result, indent=2, default=str)
        sc: dict[str, Any] | None = None
        if isinstance(result, dict):
            sc = dict(result)
        elif isinstance(result, list):
            sc = {"items": result}
        return types.CallToolResult(content=[types.TextContent(type="text", text=text)], structuredContent=sc)

    return server


def make_initialization_options(server: Server) -> InitializationOptions:
    return server.create_initialization_options(
        notification_options=NotificationOptions(tools_changed=False),
    )
