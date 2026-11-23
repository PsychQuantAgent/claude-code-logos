## Problem

The skill-writing reminder hook keeps its once-per-session marker at `<temp dir>/skill-best-practices/<session>.skill-writing` and checks neither the owner nor whether that directory is a symlink, so on a temp directory shared between users another user can decide where the marker goes. It also creates the marker before it reads `rules/skill-writing.md`, so a failed read silences the reminder for the rest of the session (PsychQuantAgent/claude-code-logos#37).

## Root Cause

`first_time_this_session()` creates the directory with `mkdir(exist_ok=True)` and the marker with `touch`, and `main()` calls it before reading the rule.

## Proposed Solution

- Marker directory `<temp dir>/skill-best-practices-<uid>`, created with mode 0700 and trusted only if `lstat` shows a directory that is not a symlink, owned by the current uid, with no group or other permission bits; without a uid (Windows), the user name in its place and only the symlink and directory checks.
- An untrusted directory: send the reminder on every SKILL.md edit, write no marker (owner's decision of 2026-11-23).
- Order: read the rule, print the context, then create the marker with O_CREAT, O_EXCL and O_NOFOLLOW, mode 0600.

## Non-Goals

- A directory under the home folder: markers are one per session and belong with temporary files.
- Preventing a duplicate reminder when two hooks of one session run at once.

## Success Criteria

- The three new Examples pass as tests that fail at the current script; the existing once-per-session Example still passes.

## Impact

- Affected specs: skill-writing-reminder (added requirement)
- Affected code:
  - Modified: plugins/skill-best-practices/scripts/skill_writing_reminder.py
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
