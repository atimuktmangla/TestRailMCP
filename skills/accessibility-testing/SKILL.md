---
name: accessibility-testing
description: >-
  Guides accessibility-oriented manual test ideas aligned with WCAG-style thinking—
  keyboard, focus, semantics, forms, and media. Use when drafting TestRail cases for
  inclusive UX or compliance-related suites.
---

# Accessibility testing (TestRail-oriented)

## When to apply

- UI features with interactive controls, forms, navigation, modals, tables, or dynamic updates.
- Regulatory or internal policy calls for WCAG 2.1/2.2 **Level A/AA** (adjust labels to your standard).

## Test design principles

1. **Keyboard first**: every actionable control reachable and operable without a mouse; visible focus; no keyboard traps in modals except documented Escape behavior.
2. **Semantics**: roles/names from accessible names (labels, `aria-label`, headings)—tie expected results to what assistive tech users would perceive.
3. **Forms**: labels associated with inputs; error messages programmatically tied to fields after validation.
4. **Contrast and zoom**: state environment baseline (e.g. 100% zoom); if your process includes contrast checks, reference design tokens or audit tools in **Expected**, not raw color codes unless required.
5. **Motion**: respect `prefers-reduced-motion` when animations are in scope.

## Case structure (for TestRail)

- **Title**: `[A11y] <Component> – <keyboard|screen reader|contrast|zoom> – <behavior>`
- **Preconditions**: browser/AT if relevant (e.g. “NVDA on Windows” only if your team standardizes it).
- **Steps**: focus order, keys used (Tab, Enter, Space, Arrow), what is announced if testing SR.
- **Expected**: focus location, role/name exposed, error association.

## Coverage checklist (pick what applies)

- Skip links / landmarks for main content.
- Modal: focus moves in, restores on close, Escape closes when specified.
- Live regions for toasts/async updates (polite/assertive as per spec).
- Table navigation for data grids (headers, sort announcements if specified).

## Notes

- This skill does **not** replace automated axe checks; it ensures **human-verifiable** cases exist in TestRail for gaps tools miss.
