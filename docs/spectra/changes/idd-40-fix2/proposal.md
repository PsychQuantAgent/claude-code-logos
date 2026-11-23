## Problem

Verify round 2 on #40 (issuecomment-7100424425) found these defects in the text and tests left by fix round 1:

- Audit question 9 asks whether the name is "neither a near-synonym … nor general enough to fit several". Under that wording a flagged name fails the question, although the spec scenario says the audit flags names without forbidding any.
- Rule 5 credits the advice on skills with different arguments, syntax or effects to Landauer et al. alone. That advice combines Landauer's syntax result with Rosenberg's near-synonym confusion.
- `numbered_lines_outside_fences` ends a fence at any line that starts with the same character. A three-backtick line inside a four-backtick fence therefore closes it early.
- Item 9 sends every overlap between existing names to a whole-plugin rename.
- The research paragraph states the null vocabulary result as if it proved that word choice mattered little.
- It also describes Rosenberg's first task as picking one operation per name.
- The broad-word example gives no job.
- Item 9 cites Landauer pp. 501 and 503 together for one finding.
- The tests do not pin the affirmative flag wording. The Sources test accepts a URL that merely ends with the DOI URL.

## Root Cause

Fix round 1 added sentences whose wording went further than the sources or the spec. Its guard tests pinned phrases that the right reading and the wrong one share.

## Proposed Solution

- Reword audit question 9 so that "yes" means the name was compared with its neighbours and flagged where needed.
- Remove the different-syntax clause from rule 5, which then points to item 9 for that case.
- Make the item 5 routing in item 9 conditional on a rename.
- Separate Landauer's measured result (p. 501) from the recommendation (p. 503).
- Quote the authors' conclusion on vocabulary as theirs.
- Describe Rosenberg's two tasks as p. 14 states them.
- Give the broad-word example a job.
- Condition the preferred name on "the naming rules that apply to the skill".
- Make the counter track the fence length.
- Strengthen the item 9 and Sources tests.

## Non-Goals

- The fence handling of `practice_9_section` and `audit_question_9` is not changed. Both date from #36 and are tracked in #43.
- The archived records of `idd-40-practice-9-neighbour-names` and `idd-40-fix1` are not edited.
- No new claim about the sources is added.
- The plugin version stays at 0.5.0, which has not been released.

## Success Criteria

- Both a clean name and a flagged name answer yes to audit question 9.
- Rule 5 does not mention Landauer.
- The counter ignores a `9. ` line inside a four-backtick fence that contains a three-backtick line.
- The Example tests fail on 3b46ac3 and pass after the change.
- The plugin tests, `tests/test_practice_lists.py` and `tests/test_marketplace.py` all pass.

## Impact

- Affected specs: skill-writing-reminder
- Affected code:
  - Modified: plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
  - Modified: plugins/skill-best-practices/rules/skill-writing.md
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
