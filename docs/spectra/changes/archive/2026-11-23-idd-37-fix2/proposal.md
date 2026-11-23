**GitHub-side tracker**: #37

## Problem

Verify round 2 for #37 (comment 7093050590) found five HIGH findings in fix round 1:

- The lock loop checks its 5-second deadline only after a failed attempt. An attempt can therefore start after the deadline, and if the marker appeared meanwhile, the hook prints nothing instead of the fallback reminder.
- Two of the lock Example tests do not show what their Examples claim. A child that has not reached the check passes the first; a hook that gives up on the first busy attempt passes the second.
- In a temp directory that others can write to and that has no sticky bit, another user can rename the private directory, so two calls can lock different files.
- An ACL can grant another user rights that mode bits do not show.

## Root Cause

- The deadline was written as a check after each failure, not as a bound on when an attempt may start.
- The tests relied on wall-clock sleeps.
- Only the private directory was checked, not the temp directory it sits in, which decides who can rename it.

## Proposed Solution

- Before creating or opening the private directory, check the open temp directory with `fstat`. It must be owned by the user or by root, and either be closed to writes by group and others or have the sticky bit. Otherwise send the reminder and write no marker.
- Cap each wait between lock attempts at the time left, and start no attempt once 5 seconds have passed.
- State the boundary in the requirement: the hook checks owners and permission bits only. An ACL that an owner of these directories or root has set is outside what it checks. Only an owner or root can set one, and an inherited ACL comes from the temp directory, which is now checked to be owned by the user or root.
- Rewrite the lock Examples so their tests run in the test process with a scripted clock and a scripted `flock`. Each test fails against a mutant script:
  - one that skips the lock;
  - one that gives up on the first busy attempt;
  - one that accepts a lock freed after the deadline.

## Non-Goals

- Reading ACLs.
- A temp directory owned by root is not tested, because the suite does not run as root.

## Success Criteria

- The new Examples' tests pass on the fixed script.
- The tests for "a temp directory open to others without the sticky bit is refused" and "a lock freed after the deadline is not taken" fail on the round-1 script.
- Each lock test fails on its mutant.

## Impact

- Affected specs: skill-writing-reminder (one MODIFIED requirement)
- Affected code:
  - Modified: plugins/skill-best-practices/scripts/skill_writing_reminder.py
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
