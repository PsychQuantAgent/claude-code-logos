## 1. Tests (written first)

- [x] 1.1 For the requirement "The session marker is private to the user and written after the reminder is sent", Example "a symlinked marker directory is refused": a test in plugins/skill-best-practices/tests/test_hooks.py marked `spec-example: skill-writing-reminder / a symlinked marker directory is refused`. Verified by failing on the current script and passing after 2.1.
- [x] 1.2 Same requirement, Example "a marker directory open to others is refused": a test marked `spec-example: skill-writing-reminder / a marker directory open to others is refused`. Verified by failing on the current script and passing after 2.1.
- [x] 1.3 Same requirement, Example "a failed read leaves the session unmarked": a test marked `spec-example: skill-writing-reminder / a failed read leaves the session unmarked`. Verified by failing on the current script and passing after 2.1.

- [x] 1.4 Same requirement, Example "a regular file in place of the marker directory is refused": a test marked `spec-example: skill-writing-reminder / a regular file in place of the marker directory is refused`; and an unmarked test that the directory the hook creates has mode 0700 and the marker 0600. Verified by both passing with 2.1 (added after spectra-verify).

## 2. Script

- [x] 2.1 plugins/skill-best-practices/scripts/skill_writing_reminder.py: the marker directory `<temp dir>/skill-best-practices-<uid>` created with mode 0700 and trusted only when lstat shows a directory, not a symlink, owned by the current uid with no group or other bits (user name and only the first two checks where there is no uid); `main()` reads the rule first, returns on a failed read, skips when a marker exists in a trusted directory, prints the context, then creates the marker with O_CREAT, O_EXCL and O_NOFOLLOW, mode 0600; an untrusted directory gets no marker. Verified by tests 1.1–1.3 and the existing once-per-session test passing.

## 3. Whole suite

- [x] 3.1 Both suites pass: python3 -m pytest -q plugins/skill-best-practices/tests tests reports no failure.
