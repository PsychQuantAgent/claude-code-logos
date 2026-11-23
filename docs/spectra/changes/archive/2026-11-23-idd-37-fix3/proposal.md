**GitHub-side tracker**: #37

## Problem

Verify round 3 for #37 (comment 7093333783) found one HIGH and four MEDIUM findings in fix round 2:

- The test for "the print and the marker write happen under the lock" accepts any marker name. It records the lock state before the creation succeeds.
- A lock can be taken after the deadline if the process is descheduled between its clock reading and `flock`.
- The scripted `flock` does not notice a blocking attempt.
- Two Scenario lines say more than the requirement.
- The requirement does not say what an error other than busy does.

## Root Cause

- The test matched on a name suffix.
- The deadline was enforced only before each attempt.
- The fake `flock` ignored its flags.

## Proposed Solution

- A lock taken once the 5 seconds have passed is let go, as if no attempt had succeeded.
- The requirement states that an error other than busy ends the wait at once and sends the reminder.
- The print-and-marker test requires a successful creation of exactly `s-1.skill-writing`, after the print.
- The scripted `flock` refuses a blocking attempt, and the always-busy test requires every attempt to start before 5 seconds.
- The two Scenario lines are reworded to match the requirement.

## Non-Goals

- The marker name for session ids outside `[A-Za-z0-9_.-]`: this is #41.

## Success Criteria

- The new Examples' tests pass.
- The test for "a lock taken after the deadline is let go" fails on the fix-round-2 script (883574b).
- Mutants fail their tests:
  - a hook without `LOCK_NB` fails the always-busy test;
  - a hook that keeps a late lock fails the late-lock test.

## Impact

- Affected specs: skill-writing-reminder (one MODIFIED requirement)
- Affected code:
  - Modified: plugins/skill-best-practices/scripts/skill_writing_reminder.py
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
