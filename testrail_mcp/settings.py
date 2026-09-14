"""Environment-backed settings for the TestRail MCP server."""

from __future__ import annotations

from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """TestRail connection and server options."""

    model_config = SettingsConfigDict(
        env_prefix="TESTRAIL_",
        env_file=".env",
        env_file_encoding="utf-8-sig",  # utf-8-sig tolerates a BOM (Windows editors add one)
        extra="ignore",
    )

    url: AnyHttpUrl = Field(
        description="Base URL of your TestRail instance (e.g. https://example.testrail.io)",
    )
    user: str = Field(
        description="TestRail login email or username (set in MCP client as TESTRAIL_USER)",
    )
    api_key: str = Field(
        description="TestRail API key / PAT from My Settings (HTTP Basic password; MCP: TESTRAIL_API_KEY)",
    )

    request_timeout_seconds: float = 60.0

    mcp_transport: Literal["stdio", "http"] = Field(
        default="stdio",
        description='MCP wire protocol: "stdio" (default) or "http" (Streamable HTTP / Starlette)',
    )
    http_host: str = Field(default="127.0.0.1", description="Bind address for MCP HTTP server")
    http_port: int = Field(default=8765, ge=1, le=65535, description="Port for MCP HTTP server")
    http_path: str = Field(
        default="/mcp",
        description="URL path for Streamable HTTP MCP endpoint",
    )
    http_stateless: bool = Field(
        default=True,
        description="Use stateless Streamable HTTP (one MCP session per request); set False for resumable sessions",
    )
