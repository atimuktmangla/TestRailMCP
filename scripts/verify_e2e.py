"""Run all local E2E checks (routing, mock HTTP, in-process MCP)."""

from __future__ import annotations

import asyncio
import json
import os
import sys

import httpx

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

from importlib.resources import files

from mcp.shared.memory import create_connected_server_and_client_session

from testrail_mcp.client import TestRailClient
from testrail_mcp.routing import build_request_from_spec, tool_suffix_to_api_method
from testrail_mcp.server import build_server
from testrail_mcp.settings import Settings


def synth_value(key: str, prop: dict):
    t = prop.get("type")
    if t == "integer":
        return 1
    if t == "string":
        return "test@example.com" if "email" in key else "x"
    if t == "boolean":
        return False
    if t == "object":
        return {}
    return None


def check_routing() -> None:
    specs = json.loads(files("testrail_mcp.data").joinpath("tools_spec.json").read_text())
    failures: list[tuple[str, str]] = []
    for spec in specs:
        name = spec["name"]
        suffix = name.removeprefix("TestRail_API_")
        api = tool_suffix_to_api_method(suffix)
        args_schema = spec.get("arguments") or {}
        req = list(args_schema.get("required") or [])
        props = args_schema.get("properties") or {}
        args: dict = {}
        for k in req:
            p = props.get(k) or {}
            if k == "body":
                args[k] = {}
                continue
            v = synth_value(k, p)
            if v is None and k != "body":
                v = 1 if "id" in k else "x"
            args[k] = v
        if api == "update_cases_by_case_id":
            args["suite_id"] = 1
        try:
            build_request_from_spec(name, api, args, required=req, properties=props)
        except Exception as e:
            failures.append((name, str(e)))
    assert not failures, failures[:5]
    print("[ok] routing: 90 tools")


def check_pagination() -> None:
    """Paginated GETs get a default limit; callers override; single reads untouched."""
    paged_props = {
        "project_id": {"type": "integer"},
        "suite_id": {"type": "integer"},
        "limit": {"type": "integer"},
        "offset": {"type": "integer"},
    }

    # get_cases with no limit -> default injected
    p = build_request_from_spec(
        "TestRail_API_getCases", "get_cases",
        {"project_id": 14, "suite_id": 46384},
        required=["project_id"], properties=paged_props,
    )
    assert p.query.get("limit") == 250, p.query
    assert p.uri_suffix == "get_cases/14", p.uri_suffix

    # get_sections with no limit -> default injected
    p = build_request_from_spec(
        "TestRail_API_getSections", "get_sections",
        {"project_id": 14, "suite_id": 46384},
        required=["project_id"], properties=paged_props,
    )
    assert p.query.get("limit") == 250, p.query

    # caller-supplied limit/offset forwarded unchanged
    p = build_request_from_spec(
        "TestRail_API_getCases", "get_cases",
        {"project_id": 14, "suite_id": 46384, "limit": 10, "offset": 20},
        required=["project_id"], properties=paged_props,
    )
    assert p.query.get("limit") == 10 and p.query.get("offset") == 20, p.query

    # single-record read gets no limit
    p = build_request_from_spec(
        "TestRail_API_getSuite", "get_suite",
        {"suite_id": 46384},
        required=["suite_id"], properties={"suite_id": {"type": "integer"}},
    )
    assert "limit" not in p.query, p.query

    # get_suites is not paginated -> no limit injected
    p = build_request_from_spec(
        "TestRail_API_getSuites", "get_suites",
        {"project_id": 14},
        required=["project_id"], properties={"project_id": {"type": "integer"}},
    )
    assert "limit" not in p.query, p.query

    print("[ok] pagination: default limit, caller override, single-read exclusion")


def check_url_format() -> None:
    """TestRail query params must be &-joined onto index.php?, not a second ?."""
    from testrail_mcp.routing import full_api_url

    base = "https://example.testrail.io"
    url = full_api_url(base, "get_cases/14", {"suite_id": 46384, "limit": 250})
    assert url.endswith("get_cases/14&suite_id=46384&limit=250"), url
    # exactly one '?' in the whole URL (the index.php? one)
    assert url.count("?") == 1, url
    # no query -> no trailing separators
    bare = full_api_url(base, "get_suites/1", {})
    assert bare.endswith("get_suites/1") and bare.count("?") == 1, bare

    # End-to-end via the client + mock transport: capture the URL TestRail sees.
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"size": 0, "cases": []})

    async def run() -> None:
        os.environ.setdefault("TESTRAIL_URL", base)
        os.environ.setdefault("TESTRAIL_USER", "u")
        os.environ.setdefault("TESTRAIL_API_KEY", "k")
        settings = Settings()
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport, auth=(settings.user, settings.api_key)) as hc:
            tr = TestRailClient(settings, hc)
            p = build_request_from_spec(
                "TestRail_API_getCases", "get_cases",
                {"project_id": 14, "suite_id": 46384},
                required=["project_id"],
                properties={"project_id": {}, "suite_id": {}, "limit": {}, "offset": {}},
            )
            await tr.execute(p)

    asyncio.run(run())
    got = captured.get("url", "")
    assert "get_cases/14&suite_id=46384&limit=250" in got, got
    assert "get_cases/14?suite_id" not in got, got
    print("[ok] url format: &-joined query, single '?'")

def mock_handler(request: httpx.Request) -> httpx.Response:
    u = str(request.url)
    if "get_projects" in u and request.method == "GET":
        return httpx.Response(200, json=[{"id": 1, "name": "P"}])
    if "get_section/" in u and request.method == "GET":
        return httpx.Response(200, json={"id": 1, "name": "S"})
    return httpx.Response(404, json={"error": u})


async def check_http_mock() -> None:
    os.environ.setdefault("TESTRAIL_URL", "https://example.testrail.io")
    os.environ.setdefault("TESTRAIL_USER", "u")
    os.environ.setdefault("TESTRAIL_API_KEY", "k")
    settings = Settings()
    transport = httpx.MockTransport(mock_handler)
    async with httpx.AsyncClient(transport=transport, auth=(settings.user, settings.api_key)) as hc:
        tr = TestRailClient(settings, hc)
        p = build_request_from_spec("TestRail_API_getProjects", "get_projects", {}, required=[], properties={})
        assert await tr.execute(p) == [{"id": 1, "name": "P"}]
        p2 = build_request_from_spec(
            "TestRail_API_getSection",
            "get_section",
            {"section_id": 5},
            required=["section_id"],
            properties={"section_id": {"type": "integer"}},
        )
        assert (await tr.execute(p2))["name"] == "S"
    print("[ok] httpx mock: get_projects + get_section")


def mcp_projects_handler(request: httpx.Request) -> httpx.Response:
    if "get_projects" in str(request.url) and request.method == "GET":
        return httpx.Response(200, json=[{"id": 1, "name": "Demo"}])
    return httpx.Response(404, json={"error": str(request.url)})


async def check_mcp_memory() -> None:
    os.environ.setdefault("TESTRAIL_URL", "https://example.testrail.io")
    os.environ.setdefault("TESTRAIL_USER", "u")
    os.environ.setdefault("TESTRAIL_API_KEY", "k")
    settings = Settings()
    transport = httpx.MockTransport(mcp_projects_handler)
    async with httpx.AsyncClient(transport=transport, auth=(settings.user, settings.api_key)) as hc:
        tr = TestRailClient(settings, hc)
        server = build_server(tr)
        async with create_connected_server_and_client_session(server, raise_exceptions=True) as session:
            listed = await session.list_tools()
            assert len(listed.tools) == 90
            out = await session.call_tool("TestRail_API_getProjects", {})
            assert not out.isError
            assert out.content and "Demo" in out.content[0].text
    print("[ok] MCP memory: list_tools + call_tool")


def main() -> None:
    check_routing()
    check_pagination()
    check_url_format()
    asyncio.run(check_http_mock())
    asyncio.run(check_mcp_memory())
    print("verify_e2e: all checks passed")


if __name__ == "__main__":
    main()
