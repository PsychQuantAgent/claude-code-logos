## Problem

Cluster verify round 1 for PsychQuantAgent/claude-code-logos#37 found four defects in the private session marker of `idd-37-private-session-marker`:
- the directory is checked by path and used again by path, so it can be swapped in between on a temp directory where others can replace entries;
- on a platform without a user id (Windows) nothing is verified and an NTFS junction passes;
- `tempfile.gettempdir()` can raise before any error handling, losing the reminder;
- two overlapping calls of one session can both print, where the old exclusive create picked one.

## Root Cause

The checks were made on a path rather than on an open directory, the platform without a user id was trusted on assumption, and printing was moved before the exclusive create without anything else serializing the calls.

## Proposed Solution

- Keep markers only where the platform has a user id, descriptor-relative open, stat and mkdir, O_DIRECTORY, O_NOFOLLOW and fcntl. Open the directory relative to the temp directory with O_DIRECTORY and O_NOFOLLOW, check it with fstat, and make every marker operation relative to that descriptor.
- Anywhere else, and whenever the temp directory, the directory or its check fails, send the reminder and write no marker.
- Under the trusted directory, take an exclusive flock on a separate `.lock` file (waiting at most 5 seconds) around the marker check, the print and the marker create.

## Non-Goals

- Verifying Windows ACLs: the hook writes no marker there instead.
- A directory under the home folder.

## Success Criteria

- Three new Examples (no temp directory, a platform that cannot verify, the lock) pass as tests that fail at the round-1 script; the four Examples of idd-37 still pass.

## Impact

- Affected specs: skill-writing-reminder (modified)
- Affected code:
  - Modified: plugins/skill-best-practices/scripts/skill_writing_reminder.py
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
