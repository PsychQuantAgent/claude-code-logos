## Problem

Verify round 3 for PsychQuantAgent/claude-code-logos#36 found no contradiction in the current text of rule 5 or Practice 9, but found that the guard tests still miss ordinary edits that would bring the round-1 contradiction back: rule 5 is read one physical line at a time although the hook delivers the whole list item, and the Practice 9 check skips everything from the scope paragraph to item 5. It also found text defects: the "Items 6 to 8 apply to every skill" lead-in sits directly before item 1; the "After" example's routing sentence covers any recording; item 6 asks every action name for its object although the action shape makes the object optional; the plaud case is described as more than it shows; the expert results start with a blanket claim; the once-per-session Scenario omits the marker condition.

## Root Cause

The spec stated the scope rules as guarantees about any future text, which no word-matching test can give, so each round found another edit the tests missed. Separately, the tests' extraction and exemption did not match what their Examples describe.

## Proposed Solution

- The decision of 2026-11-23 on #36 sets the bar: the current text is correct, the guard tests are samples, review covers the rest. The spec states the scope rules for the text as written, keeps the mutation tables as samples and adds a "No executable check" line for rewordings outside them.
- Tests match their Examples: rule 5 is the whole list item; Practice 9 skips only the scope paragraph and the blocks of items 1 to 4; sentences end at . ! or ?; mutations go where the Examples say; tilde fences count as fences. No new keyword lists.
- Practice 9 text fixes as listed in the problem, and "by people unfamiliar with it" and the full standalone-skill clause in the spec Examples.

## Non-Goals

- Rules new to this change: plugins that already mix conventions (PsychQuant/che-plugin-devtools#74) and leaving permission-changing directives out of collected wordings (PsychQuantAgent/claude-code-logos#38).
- Extending the keyword lists of the scope checks.
- The hook script (PsychQuantAgent/claude-code-logos#37).

## Success Criteria

- The fix2 tests miss the continuation-line mutation of rule 5 and the before-item-1 and below-table mutations of Practice 9; the fix3 tests report them, and pass on the unmodified text.
- Both suites pass.

## Impact

- Affected specs: skill-writing-reminder (modified)
- Affected code:
  - Modified: plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
