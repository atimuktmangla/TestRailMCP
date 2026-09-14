# Sample prompts for TestRail MCP tools

Examples of what you can ask an assistant that uses this MCP server. Replace angle-bracket placeholders with real IDs from your TestRail instance.

---

## `TestRail_API_addAttachmentToCase`

*Spec description:* Maximum upload size is 256MB

**Sample prompt:** Upload a file to test case `<case_id>`; pass `body` as a local file path string, or as an object with `"file_path": "..."` (this MCP server reads the file from disk).

- **Required parameters:** `['case_id', 'body']`

---

## `TestRail_API_addAttachmentToPlan`

*Spec description:* Maximum upload size is 256MB

**Sample prompt:** Upload a file to test plan `<plan_id>`; `body` = file path or `{"file_path": "..."}`.

- **Required parameters:** `['plan_id', 'body']`

---

## `TestRail_API_addAttachmentToPlanEntry`

*Spec description:* Maximum upload size is 256MB

**Sample prompt:** Upload a file to plan `<plan_id>`, entry `<entry_id>`; `body` = file path or `{"file_path": "..."}`.

- **Required parameters:** `['plan_id', 'entry_id', 'body']`

---

## `TestRail_API_addAttachmentToResult`

*Spec description:* Maximum upload size is 256MB

**Sample prompt:** Upload a file to result `<result_id>`; `body` = file path or `{"file_path": "..."}`.

- **Required parameters:** `['result_id', 'body']`

---

## `TestRail_API_addAttachmentToRun`

*Spec description:* Maximum upload size is 256MB

**Sample prompt:** Upload a file to run `<run_id>`; `body` = file path or `{"file_path": "..."}`.

- **Required parameters:** `['run_id', 'body']`

---

## `TestRail_API_addCase`

*Spec description:* Create a new test case

**Sample prompt:** Create a new test case under section `<section_id>` with title and fields in the request body.

- **Required parameters:** `['section_id', 'body']`

---

## `TestRail_API_addConfig`

*Spec description:* Create a new configuration

**Sample prompt:** Add a configuration under config group `<config_group_id>` (body: name and options per TestRail).

- **Required parameters:** `['config_group_id', 'body']`

---

## `TestRail_API_addConfigGroup`

*Spec description:* Create a new configuration group

**Sample prompt:** Create a configuration group on project `<project_id>`. Include a JSON `body` with the fields this API expects.

- **Required parameters:** `['project_id', 'body']`

---

## `TestRail_API_addMilestone`

*Spec description:* Add a milestone to a project

**Sample prompt:** Add a milestone to project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_addPlan`

*Spec description:* Add a test plan

**Sample prompt:** Create a test plan on project `<project_id>` with details in the body.

- **Required parameters:** `['project_id', 'body']`

---

## `TestRail_API_addPlanEntry`

*Spec description:* Add an entry to a test plan

**Sample prompt:** Add an entry to test plan `<plan_id>` (body per TestRail).

- **Required parameters:** `['plan_id', 'body']`

---

## `TestRail_API_addResult`

*Spec description:* Add a result for a test

**Sample prompt:** Submit a test result for test `<test_id>` (status, comment, etc. in body).

- **Required parameters:** `['test_id']`

---

## `TestRail_API_addResultForCase`

*Spec description:* Add a result for a case in a run

**Sample prompt:** Add a result for case `<case_id>` in run `<run_id>`.

- **Required parameters:** `['run_id', 'case_id']`

---

## `TestRail_API_addResults`

*Spec description:* Add multiple results for a run

**Sample prompt:** Bulk-add results for run `<run_id>` (array in body).

- **Required parameters:** `['run_id', 'body']`

---

## `TestRail_API_addResultsForCases`

*Spec description:* Add results for multiple cases in a run

**Sample prompt:** Add results for multiple cases in run `<run_id>`. Include a JSON `body` with the fields this API expects.

- **Required parameters:** `['run_id', 'body']`

---

## `TestRail_API_addRun`

*Spec description:* Add a test run

**Sample prompt:** Start a new test run for project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_addRunToPlanEntry`

*Spec description:* Add a run to a plan entry

**Sample prompt:** Add a run to plan `<plan_id>` entry `<entry_id>`. Include a JSON `body` with the fields this API expects.

- **Required parameters:** `['plan_id', 'entry_id', 'body']`

---

## `TestRail_API_addSection`

*Spec description:* Add a section to a project

**Sample prompt:** Create a section under project `<project_id>` (suite/section hierarchy in body).

- **Required parameters:** `['project_id']`

---

## `TestRail_API_addSharedStep`

*Spec description:* Add a shared step to a project

**Sample prompt:** Add a shared test step under project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_addSuite`

*Spec description:* Add a suite to a project

**Sample prompt:** Create a test suite on project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_addUser`

*Spec description:* Create a new user

**Sample prompt:** Create a user with email and name (and optional role fields in the same request).

- **Required parameters:** `['email', 'name']`

---

## `TestRail_API_closePlan`

*Spec description:* Close a test plan

**Sample prompt:** Close test plan `<plan_id>`.

- **Required parameters:** `['plan_id']`

---

## `TestRail_API_closeRun`

*Spec description:* Close a test run

**Sample prompt:** Close test run `<run_id>`.

- **Required parameters:** `['run_id']`

---

## `TestRail_API_copyCasesToSection`

*Spec description:* Copy test cases to a section

**Sample prompt:** Copy cases into section `<section_id>`.

- **Required parameters:** `['section_id']`

---

## `TestRail_API_deleteCase`

*Spec description:* Deleting a test case cannot be undone and permanently deletes all test results in active test runs.

**Sample prompt:** Delete test case `<case_id>`.

- **Required parameters:** `['case_id']`

---

## `TestRail_API_deleteCasesBySuite`

*Spec description:* Deleting test cases cannot be undone and permanently deletes all test results in active test runs.

**Sample prompt:** Delete cases for suite `<suite_id>` (destructive).

- **Required parameters:** `['suite_id']`

---

## `TestRail_API_deleteConfig`

*Spec description:* Delete an existing configuration

**Sample prompt:** Delete configuration `<config_id>`.

- **Required parameters:** `['config_id']`

---

## `TestRail_API_deleteConfigGroup`

*Spec description:* Delete a configuration group and all its configurations

**Sample prompt:** Delete configuration group `<config_group_id>`.

- **Required parameters:** `['config_group_id']`

---

## `TestRail_API_deleteMilestone`

*Spec description:* Delete a milestone

**Sample prompt:** Delete milestone `<milestone_id>`.

- **Required parameters:** `['milestone_id']`

---

## `TestRail_API_deleteRun`

*Spec description:* Delete a test run

**Sample prompt:** Delete run `<run_id>`.

- **Required parameters:** `['run_id']`

---

## `TestRail_API_deleteSection`

*Spec description:* Delete a section

**Sample prompt:** Delete section `<section_id>`.

- **Required parameters:** `['section_id']`

---

## `TestRail_API_deleteSharedStep`

*Spec description:* Delete a shared step

**Sample prompt:** Delete shared step revision `<shared_update_id>`.

- **Required parameters:** `['shared_update_id']`

---

## `TestRail_API_deleteSuite`

*Spec description:* Delete a suite

**Sample prompt:** Delete suite `<suite_id>`.

- **Required parameters:** `['suite_id']`

---

## `TestRail_API_getAttachment`

*Spec description:* Get an attachment by ID

**Sample prompt:** Download attachment `<attachment_id>` (response may be base64 in MCP).

- **Required parameters:** `['attachment_id']`

---

## `TestRail_API_getAttachmentsForCase`

*Spec description:* Get attachments for a test case

**Sample prompt:** List attachments for case `<case_id>`.

- **Required parameters:** `['case_id']`

---

## `TestRail_API_getAttachmentsForPlan`

*Spec description:* Get attachments for a test plan

**Sample prompt:** List attachments for plan `<plan_id>`.

- **Required parameters:** `['plan_id']`

---

## `TestRail_API_getAttachmentsForPlanEntry`

*Spec description:* Get attachments for a test plan entry

**Sample prompt:** List attachments for plan `<plan_id>` entry `<entry_id>`.

- **Required parameters:** `['plan_id', 'entry_id']`

---

## `TestRail_API_getAttachmentsForRun`

*Spec description:* Get attachments for a test run

**Sample prompt:** List attachments for run `<run_id>`.

- **Required parameters:** `['run_id']`

---

## `TestRail_API_getAttachmentsForTest`

*Spec description:* Get attachments for a test

**Sample prompt:** List attachments for test `<test_id>`.

- **Required parameters:** `['test_id']`

---

## `TestRail_API_getCase`

*Spec description:* Get a single test case

**Sample prompt:** Show full details for test case `<case_id>`.

- **Required parameters:** `['case_id']`

---

## `TestRail_API_getCaseFields`

*Spec description:* Get custom fields for test cases

**Sample prompt:** List custom case fields defined in TestRail.

---

## `TestRail_API_getCaseHistory`

*Spec description:* Get case history

**Sample prompt:** Show change history for case `<case_id>`.

- **Required parameters:** `['case_id']`

---

## `TestRail_API_getCaseStatuses`

*Spec description:* Get case statuses

**Sample prompt:** List case statuses.

---

## `TestRail_API_getCaseTypes`

*Spec description:* Get case type options

**Sample prompt:** List case types.

---

## `TestRail_API_getCases`

*Spec description:* Get test cases in a suite (or specific section of suite)

**Sample prompt:** List cases for project `<project_id>` (optionally filter by suite, filters in query).

- **Required parameters:** `['project_id']`

---

## `TestRail_API_getConfigs`

*Spec description:* Get configuration groups for a project

**Sample prompt:** List configurations for project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_getCurrentUser`

*Spec description:* Get the current user by ID

**Sample prompt:** Who am I in TestRail? (current API user)

- **Required parameters:** `['user_id']`

---

## `TestRail_API_getMilestone`

*Spec description:* Get a milestone by ID

**Sample prompt:** Get milestone `<milestone_id>`.

- **Required parameters:** `['milestone_id']`

---

## `TestRail_API_getMilestones`

*Spec description:* Get milestones for a project

**Sample prompt:** List milestones for project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_getPlan`

*Spec description:* Get a test plan by ID

**Sample prompt:** Get test plan `<plan_id>`.

- **Required parameters:** `['plan_id']`

---

## `TestRail_API_getPlans`

*Spec description:* Get test plans for a project

**Sample prompt:** List test plans for project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_getPriorities`

*Spec description:* Get priority options for test cases

**Sample prompt:** List priority labels.

---

## `TestRail_API_getProjects`

*Spec description:* Get all projects for the current user

**Sample prompt:** List all projects I can access.

---

## `TestRail_API_getResultFields`

*Spec description:* Get result fields

**Sample prompt:** List custom result fields.

---

## `TestRail_API_getResults`

*Spec description:* Get results for a test

**Sample prompt:** Get results for test `<test_id>`.

- **Required parameters:** `['test_id']`

---

## `TestRail_API_getResultsForCase`

*Spec description:* Get results for a case in a run

**Sample prompt:** Get results for case `<case_id>` in run `<run_id>`.

- **Required parameters:** `['run_id', 'case_id']`

---

## `TestRail_API_getResultsForRun`

*Spec description:* Get results for a run

**Sample prompt:** Get all results for run `<run_id>`.

- **Required parameters:** `['run_id']`

---

## `TestRail_API_getRun`

*Spec description:* Get a test run by ID

**Sample prompt:** Get test run `<run_id>`.

- **Required parameters:** `['run_id']`

---

## `TestRail_API_getRuns`

*Spec description:* Get test runs for a project

**Sample prompt:** List runs for project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_getSection`

*Spec description:* Get a section by ID

**Sample prompt:** Get section `<section_id>`.

- **Required parameters:** `['section_id']`

---

## `TestRail_API_getSections`

*Spec description:* Get sections for a project/suite

**Sample prompt:** List sections for project `<project_id>` (optionally by suite).

- **Required parameters:** `['project_id']`

---

## `TestRail_API_getSharedStep`

*Spec description:* Get a shared step by ID

**Sample prompt:** Get shared step `<shared_step_id>`.

- **Required parameters:** `['shared_step_id']`

---

## `TestRail_API_getSharedStepHistory`

*Spec description:* Get the history of a shared step

**Sample prompt:** History for shared step `<shared_step_id>`.

- **Required parameters:** `['shared_step_id']`

---

## `TestRail_API_getSharedSteps`

*Spec description:* Get shared steps for a project

**Sample prompt:** List shared steps for project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_getStatuses`

*Spec description:* Get all available statuses

**Sample prompt:** List test result statuses.

---

## `TestRail_API_getSuite`

*Spec description:* Get a suite by ID

**Sample prompt:** Get suite `<suite_id>`.

- **Required parameters:** `['suite_id']`

---

## `TestRail_API_getSuites`

*Spec description:* Get all suites for a project

**Sample prompt:** List suites for project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_getTemplates`

*Spec description:* Get templates for test cases per project

**Sample prompt:** List case templates for project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_getTest`

*Spec description:* Get a test by ID

**Sample prompt:** Get test `<test_id>` (a row in a run).

- **Required parameters:** `['test_id']`

---

## `TestRail_API_getTests`

*Spec description:* Get tests for a run

**Sample prompt:** List tests in run `<run_id>`.

- **Required parameters:** `['run_id']`

---

## `TestRail_API_getUser`

*Spec description:* Get a user by ID

**Sample prompt:** Get user `<user_id>`.

- **Required parameters:** `['user_id']`

---

## `TestRail_API_getUserByEmail`

*Spec description:* Find a user by email

**Sample prompt:** Look up user by email address.

- **Required parameters:** `['email']`

---

## `TestRail_API_getUsers`

*Spec description:* Get all users

**Sample prompt:** List users (scope may depend on role).

---

## `TestRail_API_getUsersByProject`

*Spec description:* Get users for a project

**Sample prompt:** List users with access to project `<project_id>`.

- **Required parameters:** `['project_id']`

---

## `TestRail_API_moveCasesToSection`

*Spec description:* Move test cases to a section

**Sample prompt:** Move cases into section `<section_id>`.

- **Required parameters:** `['section_id']`

---

## `TestRail_API_moveSection`

*Spec description:* Move a section

**Sample prompt:** Move/reorder section `<section_id>`.

- **Required parameters:** `['section_id']`

---

## `TestRail_API_updateCase`

*Spec description:* Update an existing test case (partial updates supported)

**Sample prompt:** Update test case `<case_id>` (fields in body).

- **Required parameters:** `['case_id', 'body']`

---

## `TestRail_API_updateCasesByCaseId`

*Spec description:* Updates multiple test cases with the same values. Does not support updating multiple test cases with different values per case.

**Sample prompt:** Bulk-update cases by IDs for suite `<suite_id>` (requires suite_id + case_ids + body).

- **Required parameters:** `['case_ids', 'body']`

---

## `TestRail_API_updateCasesBySuite`

*Spec description:* Updates multiple test cases with the same values. Does not support updating multiple test cases with different values per case.

**Sample prompt:** Bulk-update cases in suite `<suite_id>`. Include a JSON `body` with the fields this API expects.

- **Required parameters:** `['suite_id', 'body']`

---

## `TestRail_API_updateConfig`

*Spec description:* Update an existing configuration

**Sample prompt:** Update configuration `<config_id>`. Include a JSON `body` with the fields this API expects.

- **Required parameters:** `['config_id', 'body']`

---

## `TestRail_API_updateConfigGroup`

*Spec description:* Update an existing configuration group

**Sample prompt:** Update configuration group `<config_group_id>`. Include a JSON `body` with the fields this API expects.

- **Required parameters:** `['config_group_id', 'body']`

---

## `TestRail_API_updateMilestone`

*Spec description:* Update an existing milestone

**Sample prompt:** Update milestone `<milestone_id>`.

- **Required parameters:** `['milestone_id']`

---

## `TestRail_API_updatePlan`

*Spec description:* Update a test plan

**Sample prompt:** Update test plan `<plan_id>`. Include a JSON `body` with the fields this API expects.

- **Required parameters:** `['plan_id', 'body']`

---

## `TestRail_API_updatePlanEntry`

*Spec description:* Update a test plan entry

**Sample prompt:** Update plan `<plan_id>` entry `<entry_id>`. Include a JSON `body` with the fields this API expects.

- **Required parameters:** `['plan_id', 'entry_id', 'body']`

---

## `TestRail_API_updateRun`

*Spec description:* Update a test run

**Sample prompt:** Update run `<run_id>`.

- **Required parameters:** `['run_id']`

---

## `TestRail_API_updateRunToPlanEntry`

*Spec description:* Update a run in a plan entry

**Sample prompt:** Move/update run `<run_id>` relative to plan `<plan_id>`. Include a JSON `body` with the fields this API expects.

- **Required parameters:** `['plan_id', 'run_id', 'body']`

---

## `TestRail_API_updateSection`

*Spec description:* Update a section

**Sample prompt:** Update section `<section_id>`.

- **Required parameters:** `['section_id']`

---

## `TestRail_API_updateSharedStep`

*Spec description:* Update a shared step

**Sample prompt:** Update shared step `<shared_update_id>`.

- **Required parameters:** `['shared_update_id']`

---

## `TestRail_API_updateSuite`

*Spec description:* Update a suite

**Sample prompt:** Update suite `<suite_id>`.

- **Required parameters:** `['suite_id']`

---

## `TestRail_API_updateUser`

*Spec description:* Update an existing user

**Sample prompt:** Update user `<user_id>`.

- **Required parameters:** `['user_id']`

---
