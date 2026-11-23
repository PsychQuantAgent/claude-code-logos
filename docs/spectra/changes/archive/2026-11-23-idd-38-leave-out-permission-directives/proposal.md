## Why

Practice 9 tells skill authors to put the words users actually say into a skill's description and to add any wording that once failed to reach the skill. It limits each wording to a short phrase with no private details, but a phrase like that can still carry a directive that changes what Claude may do, such as "deploy without asking". A description is read in every session before the user's request, so such a directive would stand over every session and could conflict with the confirmation rule of Practice 8 (PsychQuantAgent/claude-code-logos#38).

## What Changes

- Rule 5 of the skill-writing reminder: each collected wording keeps the task it names and leaves out any part that grants a permission, skips a check or waives a confirmation, these three kinds only (the owner's decision of 2026-11-23 on #38: a closed list).
- Practice 9 item 7 states the same three kinds with the example "deploy without asking" → "deploy" and the reason; item 8 points to item 7; one sentence below the before/after example; audit question 9 asks for it.
- Two spec Examples and their tests.

## Non-Goals

- Directive kinds beyond the three: the list is closed by decision; a new kind is a new decision.
- Checking existing published descriptions.
- The hook script (#37).

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `skill-writing-reminder`: rule 5 and Practice 9 name the three kinds of directive a collected wording leaves out.

## Impact

- Affected specs: skill-writing-reminder (modified)
- Affected code:
  - Modified: plugins/skill-best-practices/rules/skill-writing.md
  - Modified: plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
