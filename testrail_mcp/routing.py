"""Map MCP tool names to TestRail API v2 HTTP requests."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

# Tool suffix (CamelCase after TestRail_API_) -> snake_case API method name
_CAMEL_SNAKE_1 = re.compile(r"([A-Z]+)([A-Z][a-z])")
_CAMEL_SNAKE_2 = re.compile(r"([a-z\d])([A-Z])")


def tool_suffix_to_api_method(suffix: str) -> str:
    s = _CAMEL_SNAKE_1.sub(r"\1_\2", suffix)
    s = _CAMEL_SNAKE_2.sub(r"\1_\2", s)
    return s.lower()


def infer_http_method(api_method: str) -> str:
    if api_method.startswith("get_"):
        return "GET"
    return "POST"


# TestRail 6.7+ returns these bulk collections in a paginated envelope. Calling
# them without a limit makes some server versions raise an unhandled HTTP 500
# (empty body). Default to the API's max page size (250) when the caller omits
# limit so bare calls stay reliable; callers can still page via offset/limit.
DEFAULT_PAGE_LIMIT = 250
PAGINATED_GET_METHODS = frozenset(
    {
        "get_cases",
        "get_sections",
        "get_runs",
        "get_plans",
        "get_milestones",
        "get_tests",
        "get_results",
        "get_results_for_case",
        "get_results_for_run",
        "get_shared_steps",
    }
)


PRIORITY_PATH_KEYS = [
    "project_id",
    "suite_id",
    "plan_id",
    "entry_id",
    "milestone_id",
    "run_id",
    "case_id",
    "section_id",
    "case_ids",
    "test_id",
    "result_id",
    "user_id",
    "shared_step_id",
    "shared_update_id",
    "attachment_id",
    "config_group_id",
    "config_id",
    "email",
    "name",
]


def default_path_keys(api_method: str, required: list[str]) -> list[str]:
    keys = set(required) - {"body"}
    if not keys:
        return []
    if keys == {"run_id", "case_id"}:
        return ["run_id", "case_id"]
    if keys == {"plan_id", "entry_id"}:
        return ["plan_id", "entry_id"]
    if keys == {"config_group_id", "config_id"}:
        return ["config_group_id", "config_id"]
    if keys == {"plan_id", "run_id"}:
        return ["plan_id", "run_id"]
    ordered = [k for k in PRIORITY_PATH_KEYS if k in keys]
    rest = sorted(k for k in keys if k not in ordered)
    return ordered + rest


@dataclass(frozen=True)
class PreparedRequest:
    http_method: str
    uri_suffix: str
    query: dict[str, Any]
    json_body: Any | None
    is_multipart_path: bool
    binary_response: bool


def _merge_body_payload(arguments: dict[str, Any]) -> dict[str, Any]:
    raw = arguments.get("body")
    if isinstance(raw, dict):
        return dict(raw)
    return {}


def build_request_from_spec(
    _tool_name: str,
    api_method: str,
    arguments: dict[str, Any] | None,
    *,
    required: list[str],
    properties: dict[str, Any],
) -> PreparedRequest:
    """Build request using JSON-schema metadata from tools_spec."""
    args = dict(arguments or {})
    http_method = infer_http_method(api_method)

    if api_method == "get_current_user":
        return PreparedRequest("GET", "get_current_user", {}, None, False, False)

    if api_method == "get_user_by_email":
        email = args.get("email")
        if email is None:
            raise ValueError("email is required")
        return PreparedRequest("GET", "get_user_by_email", {"email": email}, None, False, False)

    if api_method == "add_user":
        payload = {k: v for k, v in args.items() if v is not None}
        return PreparedRequest("POST", "add_user", {}, payload, False, False)

    prop_keys = set(properties.keys()) if properties else set()

    if api_method == "update_cases_by_case_id":
        suite_id = args.get("suite_id")
        if suite_id is None:
            raise ValueError(
                "update_cases_by_case_id requires suite_id in arguments "
                "(TestRail expects POST update_cases/:suite_id)",
            )
        inner = _merge_body_payload(args)
        top = {k: v for k, v in args.items() if k not in ("body", "suite_id") and v is not None}
        payload = {**top, **inner}
        return PreparedRequest("POST", f"update_cases/{suite_id}", {}, payload, False, False)

    path_keys = default_path_keys(api_method, required)
    if "body" in required:
        path_keys = [k for k in path_keys if k != "body"]

    path_parts: list[str] = [api_method]
    for key in path_keys:
        if key not in args or args[key] is None:
            raise ValueError(f"missing required path parameter '{key}'")
        path_parts.append(str(args[key]))
    uri_suffix = "/".join(path_parts)

    reserved = set(path_keys) | {"body"}
    query: dict[str, Any] = {}
    json_body: Any | None = None
    multipart = bool(http_method == "POST" and api_method.startswith("add_attachment_to"))
    binary_response = api_method == "get_attachment"

    if http_method == "GET":
        for k, v in args.items():
            if k in reserved or v is None:
                continue
            if k in prop_keys:
                query[k] = v
        if api_method in PAGINATED_GET_METHODS and query.get("limit") is None:
            query["limit"] = DEFAULT_PAGE_LIMIT
    else:
        if multipart:
            json_body = args.get("body")
        elif "body" in args:
            body_val = args["body"]
            if isinstance(body_val, dict):
                json_body = body_val
            elif body_val is None:
                json_body = {}
            else:
                json_body = body_val
        else:
            payload = {k: v for k, v in args.items() if k not in reserved and v is not None}
            json_body = payload if payload else None

    return PreparedRequest(http_method, uri_suffix, query, json_body, multipart, binary_response)


def full_api_url(base: str, uri_suffix: str, query: dict[str, Any] | None = None) -> str:
    """Render a TestRail API v2 URL.

    TestRail encodes the entire API path inside a single ``index.php?`` query
    string, so additional query parameters must be appended with ``&`` -- NOT as
    a second ``?`` (httpx ``params=`` would do the latter, which makes TestRail
    parse the first param as an unknown controller and 404/500). We therefore
    URL-encode and join query params here with ``&``.
    """
    from urllib.parse import quote

    root = base.rstrip("/")
    url = f"{root}/index.php?/api/v2/{uri_suffix}"
    if query:
        parts = [
            f"{quote(str(k), safe='')}={quote(str(v), safe='')}"
            for k, v in query.items()
            if v is not None
        ]
        if parts:
            url = url + "&" + "&".join(parts)
    return url
