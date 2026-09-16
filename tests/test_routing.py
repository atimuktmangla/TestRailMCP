"""
Unit tests for the pure request-routing logic. No network, no TestRail, no LLM —
these lock the CamelCase->snake mapping, HTTP-method inference, path-key
ordering, request building, URL rendering, and pagination defaults.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from testrail_mcp.routing import (  # noqa: E402
    DEFAULT_PAGE_LIMIT,
    build_request_from_spec,
    default_path_keys,
    full_api_url,
    infer_http_method,
    tool_suffix_to_api_method,
)


# ── tool_suffix_to_api_method ─────────────────────────────────────────────────

def test_suffix_simple():
    assert tool_suffix_to_api_method("GetCase") == "get_case"
    assert tool_suffix_to_api_method("AddCase") == "add_case"


def test_suffix_multiword():
    assert tool_suffix_to_api_method("GetResultsForCase") == "get_results_for_case"
    assert tool_suffix_to_api_method("UpdateCasesByCaseId") == "update_cases_by_case_id"


def test_suffix_acronym_boundary():
    # GetUserByEmail -> get_user_by_email (no stray splits)
    assert tool_suffix_to_api_method("GetUserByEmail") == "get_user_by_email"


# ── infer_http_method ─────────────────────────────────────────────────────────

def test_get_methods_are_GET():
    assert infer_http_method("get_case") == "GET"
    assert infer_http_method("get_results_for_run") == "GET"


def test_non_get_methods_are_POST():
    assert infer_http_method("add_case") == "POST"
    assert infer_http_method("update_case") == "POST"
    assert infer_http_method("delete_case") == "POST"


# ── default_path_keys ─────────────────────────────────────────────────────────

def test_path_keys_priority_order():
    # project_id should precede suite_id per PRIORITY_PATH_KEYS
    assert default_path_keys("get_cases", ["suite_id", "project_id"]) == [
        "project_id",
        "suite_id",
    ]


def test_path_keys_special_pair():
    assert default_path_keys("get_results_for_case", ["case_id", "run_id"]) == [
        "run_id",
        "case_id",
    ]


def test_path_keys_excludes_body():
    assert default_path_keys("add_case", ["section_id", "body"]) == ["section_id"]


# ── build_request_from_spec ───────────────────────────────────────────────────

def _build(api_method, args, required=None, properties=None):
    return build_request_from_spec(
        f"TestRail_API_{api_method}", api_method, args,
        required=required or [], properties=properties or {},
    )


def test_build_get_with_path_param():
    req = _build("get_case", {"case_id": 42}, required=["case_id"])
    assert req.http_method == "GET"
    assert req.uri_suffix == "get_case/42"
    assert req.json_body is None


def test_build_get_missing_path_param_raises():
    import pytest
    with pytest.raises(ValueError):
        _build("get_case", {}, required=["case_id"])


def test_build_paginated_get_defaults_limit():
    req = _build("get_cases", {"project_id": 1}, required=["project_id"],
                 properties={"project_id": {}, "limit": {}})
    assert req.query.get("limit") == DEFAULT_PAGE_LIMIT


def test_build_paginated_get_respects_explicit_limit():
    req = _build("get_cases", {"project_id": 1, "limit": 10}, required=["project_id"],
                 properties={"project_id": {}, "limit": {}})
    assert req.query.get("limit") == 10


def test_build_post_body_dict():
    req = _build("add_case", {"section_id": 5, "body": {"title": "x"}},
                 required=["section_id", "body"])
    assert req.http_method == "POST"
    assert req.uri_suffix == "add_case/5"
    assert req.json_body == {"title": "x"}


def test_build_get_user_by_email():
    req = _build("get_user_by_email", {"email": "a@b.com"})
    assert req.http_method == "GET"
    assert req.query == {"email": "a@b.com"}


def test_build_get_user_by_email_missing_raises():
    import pytest
    with pytest.raises(ValueError):
        _build("get_user_by_email", {})


def test_build_add_attachment_is_multipart():
    req = _build("add_attachment_to_case", {"case_id": 7, "body": "/tmp/x.png"},
                 required=["case_id", "body"])
    assert req.is_multipart_path is True


def test_build_get_attachment_binary_response():
    req = _build("get_attachment", {"attachment_id": 3}, required=["attachment_id"])
    assert req.binary_response is True


# ── full_api_url ──────────────────────────────────────────────────────────────

def test_url_no_query():
    url = full_api_url("https://tr.example.com/", "get_case/42")
    assert url == "https://tr.example.com/index.php?/api/v2/get_case/42"


def test_url_query_joined_with_ampersand():
    # TestRail requires & (not a second ?) for extra params.
    url = full_api_url("https://tr.example.com", "get_cases/1", {"limit": 250, "offset": 0})
    assert url.startswith("https://tr.example.com/index.php?/api/v2/get_cases/1&")
    assert "limit=250" in url and "offset=0" in url
    assert url.count("?") == 1


def test_url_skips_none_query():
    url = full_api_url("https://tr.example.com", "get_cases/1", {"limit": None})
    assert "limit" not in url
