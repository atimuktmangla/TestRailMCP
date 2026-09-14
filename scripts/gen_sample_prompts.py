"""Generate prompts/sample_tool_prompts.md from tools_spec.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sample_prompt(name: str, desc: str, req: list[str]) -> str:
    """Build one natural-language sample prompt."""
    desc = (desc or "").strip()
    if desc.startswith("[TestRail API]"):
        desc = desc[len("[TestRail API]") :].strip()
    short = name.removeprefix("TestRail_API_")
    has_body = "body" in req
    ids = [k for k in req if k != "body"]

    # Attachment endpoints share a generic description in the spec
    if short.startswith("addAttachment"):
        if "case_id" in ids:
            return (
                "Upload a file to test case `<case_id>`; pass `body` as a local file path string, "
                "or as an object with `\"file_path\": \"...\"` (this MCP server reads the file from disk)."
            )
        if "plan_id" in ids and "entry_id" in ids:
            return (
                "Upload a file to plan `<plan_id>`, entry `<entry_id>`; `body` = file path or "
                "`{\"file_path\": \"...\"}`."
            )
        if "plan_id" in ids:
            return (
                "Upload a file to test plan `<plan_id>`; `body` = file path or `{\"file_path\": \"...\"}`."
            )
        if "result_id" in ids:
            return (
                "Upload a file to result `<result_id>`; `body` = file path or `{\"file_path\": \"...\"}`."
            )
        if "run_id" in ids:
            return (
                "Upload a file to run `<run_id>`; `body` = file path or `{\"file_path\": \"...\"}`."
            )
        return "Upload an attachment; `body` = file path or `{\"file_path\": \"...\"}`."

    templates: dict[str, str] = {
        "addCase": "Create a new test case under section `<section_id>` with title and fields in the request body.",
        "addConfig": "Add a configuration under config group `<config_group_id>` (body: name and options per TestRail).",
        "addConfigGroup": "Create a configuration group on project `<project_id>`.",
        "addMilestone": "Add a milestone to project `<project_id>`.",
        "addPlan": "Create a test plan on project `<project_id>` with details in the body.",
        "addPlanEntry": "Add an entry to test plan `<plan_id>` (body per TestRail).",
        "addResult": "Submit a test result for test `<test_id>` (status, comment, etc. in body).",
        "addResultForCase": "Add a result for case `<case_id>` in run `<run_id>`.",
        "addResults": "Bulk-add results for run `<run_id>` (array in body).",
        "addResultsForCases": "Add results for multiple cases in run `<run_id>`.",
        "addRun": "Start a new test run for project `<project_id>`.",
        "addRunToPlanEntry": "Add a run to plan `<plan_id>` entry `<entry_id>`.",
        "addSection": "Create a section under project `<project_id>` (suite/section hierarchy in body).",
        "addSharedStep": "Add a shared test step under project `<project_id>`.",
        "addSuite": "Create a test suite on project `<project_id>`.",
        "addUser": "Create a user with email and name (and optional role fields in the same request).",
        "closePlan": "Close test plan `<plan_id>`.",
        "closeRun": "Close test run `<run_id>`.",
        "copyCasesToSection": "Copy cases into section `<section_id>`.",
        "deleteCase": "Delete test case `<case_id>`.",
        "deleteCasesBySuite": "Delete cases for suite `<suite_id>` (destructive).",
        "deleteConfig": "Delete configuration `<config_id>`.",
        "deleteConfigGroup": "Delete configuration group `<config_group_id>`.",
        "deleteMilestone": "Delete milestone `<milestone_id>`.",
        "deleteRun": "Delete run `<run_id>`.",
        "deleteSection": "Delete section `<section_id>`.",
        "deleteSharedStep": "Delete shared step revision `<shared_update_id>`.",
        "deleteSuite": "Delete suite `<suite_id>`.",
        "getAttachment": "Download attachment `<attachment_id>` (response may be base64 in MCP).",
        "getAttachmentsForCase": "List attachments for case `<case_id>`.",
        "getAttachmentsForPlan": "List attachments for plan `<plan_id>`.",
        "getAttachmentsForPlanEntry": "List attachments for plan `<plan_id>` entry `<entry_id>`.",
        "getAttachmentsForRun": "List attachments for run `<run_id>`.",
        "getAttachmentsForTest": "List attachments for test `<test_id>`.",
        "getCase": "Show full details for test case `<case_id>`.",
        "getCaseFields": "List custom case fields defined in TestRail.",
        "getCaseHistory": "Show change history for case `<case_id>`.",
        "getCaseStatuses": "List case statuses.",
        "getCaseTypes": "List case types.",
        "getCases": "List cases for project `<project_id>` (optionally filter by suite, filters in query).",
        "getConfigs": "List configurations for project `<project_id>`.",
        "getCurrentUser": "Who am I in TestRail? (current API user)",
        "getMilestone": "Get milestone `<milestone_id>`.",
        "getMilestones": "List milestones for project `<project_id>`.",
        "getPlan": "Get test plan `<plan_id>`.",
        "getPlans": "List test plans for project `<project_id>`.",
        "getPriorities": "List priority labels.",
        "getProjects": "List all projects I can access.",
        "getResultFields": "List custom result fields.",
        "getResults": "Get results for test `<test_id>`.",
        "getResultsForCase": "Get results for case `<case_id>` in run `<run_id>`.",
        "getResultsForRun": "Get all results for run `<run_id>`.",
        "getRun": "Get test run `<run_id>`.",
        "getRuns": "List runs for project `<project_id>`.",
        "getSection": "Get section `<section_id>`.",
        "getSections": "List sections for project `<project_id>` (optionally by suite).",
        "getSharedStep": "Get shared step `<shared_step_id>`.",
        "getSharedStepHistory": "History for shared step `<shared_step_id>`.",
        "getSharedSteps": "List shared steps for project `<project_id>`.",
        "getStatuses": "List test result statuses.",
        "getSuite": "Get suite `<suite_id>`.",
        "getSuites": "List suites for project `<project_id>`.",
        "getTemplates": "List case templates for project `<project_id>`.",
        "getTest": "Get test `<test_id>` (a row in a run).",
        "getTests": "List tests in run `<run_id>`.",
        "getUser": "Get user `<user_id>`.",
        "getUserByEmail": "Look up user by email address.",
        "getUsers": "List users (scope may depend on role).",
        "getUsersByProject": "List users with access to project `<project_id>`.",
        "moveCasesToSection": "Move cases into section `<section_id>`.",
        "moveSection": "Move/reorder section `<section_id>`.",
        "updateCase": "Update test case `<case_id>` (fields in body).",
        "updateCasesByCaseId": "Bulk-update cases by IDs for suite `<suite_id>` (requires suite_id + case_ids + body).",
        "updateCasesBySuite": "Bulk-update cases in suite `<suite_id>`.",
        "updateConfig": "Update configuration `<config_id>`.",
        "updateConfigGroup": "Update configuration group `<config_group_id>`.",
        "updateMilestone": "Update milestone `<milestone_id>`.",
        "updatePlan": "Update test plan `<plan_id>`.",
        "updatePlanEntry": "Update plan `<plan_id>` entry `<entry_id>`.",
        "updateRun": "Update run `<run_id>`.",
        "updateRunToPlanEntry": "Move/update run `<run_id>` relative to plan `<plan_id>`.",
        "updateSection": "Update section `<section_id>`.",
        "updateSharedStep": "Update shared step `<shared_update_id>`.",
        "updateSuite": "Update suite `<suite_id>`.",
        "updateUser": "Update user `<user_id>`.",
    }

    if short in templates:
        base = templates[short]
    else:
        base = f"{desc} (tool `{short}`)."

    if has_body and "body" not in base.lower():
        base += " Include a JSON `body` with the fields this API expects."

    return base


def main() -> None:
    specs = json.loads(
        (ROOT / "testrail_mcp/data/tools_spec.json").read_text(encoding="utf-8")
    )
    specs.sort(key=lambda x: x["name"])

    out: list[str] = []
    out.append("# Sample prompts for TestRail MCP tools")
    out.append("")
    out.append(
        "Examples of what you can ask an assistant that uses this MCP server. "
        "Replace angle-bracket placeholders with real IDs from your TestRail instance."
    )
    out.append("")
    out.append("---")
    out.append("")

    for s in specs:
        name = s["name"]
        desc = s.get("description") or ""
        args = s.get("arguments") or {}
        req = list(args.get("required") or [])
        api_line = (desc or "").strip()
        if api_line.startswith("[TestRail API]"):
            api_line = api_line[len("[TestRail API]") :].strip()

        out.append(f"## `{name}`")
        out.append("")
        if api_line:
            out.append(f"*Spec description:* {api_line}")
            out.append("")
        out.append(f"**Sample prompt:** {sample_prompt(name, desc, req)}")
        out.append("")
        if req:
            out.append(f"- **Required parameters:** `{req}`")
            out.append("")
        out.append("---")
        out.append("")

    out_dir = ROOT / "prompts"
    out_dir.mkdir(exist_ok=True)
    target = out_dir / "sample_tool_prompts.md"
    target.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {target} ({len(specs)} tools)")


if __name__ == "__main__":
    main()
