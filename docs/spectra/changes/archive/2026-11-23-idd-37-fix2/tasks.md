## 1. Tests (first)

- [x] 1.1 Example "a temp directory open to others without the sticky bit is refused": a subprocess test in plugins/skill-best-practices/tests/test_hooks.py marked `spec-example: skill-writing-reminder / a temp directory open to others without the sticky bit is refused`. Verified by failing on the round-1 script (4f33f0e) and passing after 2.1.
- [x] 1.2 Example "a sticky shared temp directory keeps markers": a subprocess test marked `spec-example: skill-writing-reminder / a sticky shared temp directory keeps markers`. Verified by passing before and after 2.1, since markers in a sticky temp directory must keep working.
- [x] 1.3 Example "the check runs under the session lock": rewritten as an in-process test with a scripted clock and a scripted `flock`, same marker. Verified by passing after 2.1, and by failing on a mutant whose lock function returns without calling `flock`.
- [x] 1.4 Example "a lock held too long still sends the reminder": rewritten the same way, same marker. Verified by passing after 2.1, and by failing on a mutant that gives up on the first busy attempt.
- [x] 1.5 Example "a lock freed after the deadline is not taken": a new in-process test marked `spec-example: skill-writing-reminder / a lock freed after the deadline is not taken`. Verified by failing on the round-1 script and passing after 2.1.
- [x] 1.7 Added after spectra-verify:
  - Example "who may own the temp directory": an in-process table test of `_temp_dir_trusted`, marked `spec-example: skill-writing-reminder / who may own the temp directory`.
  - Example "the print and the marker write happen under the lock": a test marked `spec-example: skill-writing-reminder / the print and the marker write happen under the lock`, which checks from a second descriptor that the lock is held at both moments.
  - The test for "a lock held too long" also checks that no sleep is longer than the time left.
  Verified by mutants: a check without the owner clause fails the first test, a lock released right after the check fails the second, and an uncapped sleep fails the third.
- [x] 1.6 The subprocess lock test and its in-process companion from fix round 1 are removed, since 1.3 replaces both.

## 2. Script

- [x] 2.1 For the requirement "The session marker is private to the user and written after the reminder is sent", plugins/skill-best-practices/scripts/skill_writing_reminder.py:
  - `_open_marker_dir` checks the open temp directory with `fstat` before it creates or opens the marker directory. The temp directory must be owned by the current user or root, and either have no group or other write bit or have the sticky bit; otherwise the function returns None.
  - `_lock` caps each sleep at the time left before the deadline and starts no attempt once the deadline has passed.
  Verified by 1.1–1.5.
- [x] 2.2 The script's docstring names the temp-directory check and the deadline rule.

## 3. Whole suite

- [x] 3.1 `python3 -m pytest -q plugins/skill-best-practices/tests tests` passes, and the three mutants each fail their test.
