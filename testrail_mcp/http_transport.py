"""MCP Streamable HTTP transport (Starlette + uvicorn) for remote clients."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.types import Receive, Scope, Send


class _StreamableHttpAsgi:
    """Delegates ASGI to StreamableHTTPSessionManager.handle_request."""

    def __init__(self, session_manager: StreamableHTTPSessionManager) -> None:
        self._session_manager = session_manager

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self._session_manager.handle_request(scope, receive, send)


def build_streamable_http_app(
    server: Server[Any, Any],
    *,
    path: str,
    stateless: bool,
) -> Starlette:
    """
    Starlette app exposing MCP over Streamable HTTP at ``path``.

    Stateless mode (recommended for simple deployments) handles each request
    with a fresh MCP session; set ``stateless=False`` for session resumption features.
    """
    session_manager = StreamableHTTPSessionManager(
        app=server,
        event_store=None,
        stateless=stateless,
    )
    asgi = _StreamableHttpAsgi(session_manager)

    @asynccontextmanager
    async def lifespan(_: Starlette):
        async with session_manager.run():
            yield

    normalized = path if path.startswith("/") else f"/{path}"
    return Starlette(
        lifespan=lifespan,
        routes=[Route(normalized, endpoint=asgi)],
    )
