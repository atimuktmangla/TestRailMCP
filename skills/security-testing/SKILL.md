---
name: security-testing
description: >-
  Guides security-focused test design for features under review—authn/authz, injection,
  secrets, sessions, and common OWASP-style checks. Use when generating or reviewing
  TestRail cases for security-sensitive areas.
---

# Security testing (TestRail-oriented)

## When to apply

- Requirements mention login, roles, permissions, tokens, APIs, uploads, or PII.
- You are drafting or refining **manual or automated** test cases destined for TestRail.

## Test design principles

1. **Positive and negative**: valid use cases plus abuse cases (missing token, wrong role, expired session).
2. **Least privilege**: each role should only reach resources allowed by spec; document role name and expected HTTP/UI outcome.
3. **Injection surfaces**: inputs that become queries, commands, HTML, or URLs—include boundary and encoded payloads only in **safe, approved** test environments.
4. **Secrets**: never put real credentials in case steps; use placeholders like `{valid_user}` and reference a test data matrix in comments if needed.
5. **Idempotency and replay**: where APIs allow retries, note whether duplicate submissions should fail or dedupe.

## Case structure (for TestRail)

- **Title**: `[Security] <Area> – <behavior under test>`
- **Preconditions**: environment, role, feature flag, data seed.
- **Steps**: numbered, atomic; include exact UI/API path when known.
- **Expected**: observable outcome (status code, message, audit log if in scope).

## Coverage checklist (adapt to feature)

- Authentication: valid login, invalid password lockout policy if specified, logout/session expiry.
- Authorization: horizontal (other user’s ID) and vertical (lower role accessing admin action).
- Input validation: max length, type, required fields.
- Transport: HTTPS for sensitive operations (environment assumption, not a UI click step unless testing mixed content).

## Out of scope for generic skills

- Formal penetration testing sign-off; this skill only improves **test case quality** and traceability.
