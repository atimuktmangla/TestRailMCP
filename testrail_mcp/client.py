"""Async HTTP client for TestRail API v2."""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

import httpx

from testrail_mcp.routing import PreparedRequest, full_api_url
from testrail_mcp.settings import Settings


class TestRailClient:
    """Thin wrapper around httpx with TestRail basic auth and response handling."""

    def __init__(self, settings: Settings, client: httpx.AsyncClient) -> None:
        self._settings = settings
        self._client = client

    async def execute(self, prepared: PreparedRequest) -> Any:
        timeout = self._settings.request_timeout_seconds

        if prepared.http_method == "GET":
            # TestRail requires query params joined with & onto the index.php?
            # path (not a second ?). full_api_url handles that; do NOT pass
            # httpx params= here.
            url = full_api_url(
                str(self._settings.url), prepared.uri_suffix, prepared.query
            )
            response = await self._client.request(
                "GET",
                url,
                timeout=timeout,
            )
        elif prepared.is_multipart_path:
            url = full_api_url(str(self._settings.url), prepared.uri_suffix)
            body = prepared.json_body
            file_path: Path | None = None
            if isinstance(body, str):
                file_path = Path(body)
            elif isinstance(body, dict) and "file_path" in body:
                file_path = Path(str(body["file_path"]))
            if file_path is None or not file_path.is_file():
                raise ValueError(
                    "Attachment upload requires body as a filesystem path string, "
                    "or dict with 'file_path' pointing to a readable file",
                )
            data_bytes = file_path.read_bytes()
            files = {"attachment": (file_path.name, data_bytes)}
            response = await self._client.post(url, files=files, timeout=timeout)
        else:
            url = full_api_url(
                str(self._settings.url), prepared.uri_suffix, prepared.query
            )
            response = await self._client.request(
                prepared.http_method,
                url,
                json=prepared.json_body if prepared.json_body is not None else None,
                timeout=timeout,
            )

        if not (200 <= response.status_code < 300):
            try:
                detail = response.json()
            except json.JSONDecodeError:
                detail = response.text
            raise RuntimeError(f"TestRail API HTTP {response.status_code}: {detail!r}")

        if prepared.binary_response:
            return {
                "encoding": "base64",
                "data": base64.standard_b64encode(response.content).decode("ascii"),
            }

        text = response.text
        if not text:
            return None
        try:
            return response.json()
        except json.JSONDecodeError:
            return text


def create_http_client(settings: Settings) -> httpx.AsyncClient:
    return httpx.AsyncClient(auth=(settings.user, settings.api_key))
