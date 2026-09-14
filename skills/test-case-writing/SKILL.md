---
name: test-case-writing
description: >-
  Standards for clear, maintainable TestRail cases—titles, fields, steps, expected
  results, and traceability to requirements. Use whenever authoring or refactoring
  cases for manual or hybrid manual/automation suites.
---

# Test case writing

## Title

- **One intent per case**: avoid “and verify everything.”
- Prefer **Given/When/Then** phrasing in the title only if your team uses BDD; otherwise use concise action + outcome.
- Include **scope marker** in prefix if your project uses tags: `[Smoke]`, `[Regression]`, `[API]`, etc.

## Fields

- **Preconditions**: minimal facts needed before step 1 (user role, data state, feature flags). Avoid duplicating whole stories.
- **References**: requirement ID, user story, or Jira key in a dedicated field if TestRail is configured for it; otherwise first line of **Description**.

## Steps

1. **Atomic**: one user action or observation per step where possible.
2. **Observable**: each step should have a checkable **Expected Result** (same row if using separated steps/expected in TestRail).
3. **Data**: use symbolic names (`UserA`, `Order #12345`) consistent with test data docs.
4. **Automation hints**: if automation will follow, add stable `data-testid` or API path in **Notes**, not in customer-facing wording unless required.

## Expected results

- Specific: “Status **Published**” not “Status is correct.”
- Include error paths: invalid input shows message **X** and field **Y** is highlighted.

## Traceability

- Map each case to **at least one** acceptance criterion or requirement ID when available.
- For duplicates, prefer **merge** or **reference case** instead of copy-paste drift.

## Maintenance

- Deprecate cases for removed features; link replacement cases in **Comment** when TestRail supports it.
