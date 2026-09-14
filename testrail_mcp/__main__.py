"""CLI entry: run the TestRail MCP server over stdio or Streamable HTTP."""

from __future__ import annotations

import logging
import sys

import anyio
import uvicorn

from testrail_mcp.client import TestRailClient, create_http_client
from testrail_mcp.http_transport import build_streamable_http_app
from testrail_mcp.server import build_server, make_initialization_options
from testrail_mcp.settings import Settings


def main() -> None:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    try:
        settings = Settings()
    except Exception as exc:
        print(
            "Missing or invalid configuration. Set TESTRAIL_URL, TESTRAIL_USER, TESTRAIL_API_KEY.\n"
            f"Details: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    if settings.mcp_transport == "http":
        anyio.run(_run_http, settings)
    else:
        anyio.run(_run_stdio, settings)


async def _run_stdio(settings: Settings) -> None:
    async with create_http_client(settings) as http_client:
        tr = TestRailClient(settings, http_client)
        server = build_server(tr)
        init = make_initialization_options(server)
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                init,
            )


async def _run_http(settings: Settings) -> None:
    async with create_http_client(settings) as http_client:
        tr = TestRailClient(settings, http_client)
        server = build_server(tr)
        app = build_streamable_http_app(
            server,
            path=settings.http_path,
            stateless=settings.http_stateless,
        )
        config = uvicorn.Config(
            app,
            host=settings.http_host,
            port=settings.http_port,
            log_level="info",
        )
        await uvicorn.Server(config).serve()


if __name__ == "__main__":
    main()
