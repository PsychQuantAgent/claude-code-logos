## 1. Tests (written first)

- [x] 1.1 For the requirement "The session marker is private to the user and written after the reminder is sent", Example "no temp directory still sends the reminder": an in-process test in plugins/skill-best-practices/tests/test_hooks.py marked `spec-example: skill-writing-reminder / no temp directory still sends the reminder`. Verified by failing on the round-1 script and passing after 2.1.
- [x] 1.2 Same requirement, Example "a platform that cannot verify the directory writes no marker": an in-process test marked `spec-example: skill-writing-reminder / a platform that cannot verify the directory writes no marker`. Verified by failing on the round-1 script (it has no platform check to turn off) and passing after 2.1.
- [x] 1.3 Same requirement, Example "the check runs under the session lock": a subprocess test marked `spec-example: skill-writing-reminder / the check runs under the session lock`. Verified by failing on the round-1 script (it prints at once) and passing after 2.1.

- [x] 1.4 Same requirement, Example "a lock held too long still sends the reminder": an in-process test marked `spec-example: skill-writing-reminder / a lock held too long still sends the reminder`, plus an unmarked in-process test that the marker check runs after the lock is taken (the marker appears inside `flock`). Added after spectra-verify; verified by passing with 2.1.

## 2. Script

- [x] 2.1 plugins/skill-best-practices/scripts/skill_writing_reminder.py: a platform check (user id; os.open, os.stat and os.mkdir in os.supports_dir_fd; O_DIRECTORY; O_NOFOLLOW; fcntl); the temp directory looked up inside the error handling; the marker directory created and opened relative to the temp directory with O_DIRECTORY and O_NOFOLLOW and checked with fstat; flock on `.lock` in it with a 5-second wait; marker check and create with dir_fd; every failure sends the reminder without a marker. Verified by tests 1.1–1.3 and the four idd-37 Example tests passing.
- [x] 2.2 The permission test lists the markers without `.lock`. Verified by it passing.

## 3. Whole suite

- [x] 3.1 Both suites pass: python3 -m pytest -q plugins/skill-best-practices/tests tests reports no failure.
