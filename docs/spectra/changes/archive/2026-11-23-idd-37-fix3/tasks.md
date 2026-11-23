## 1. Tests (first)

- [x] 1.1 Example "the print and the marker write happen under the lock": the test requires a successful creation of exactly `s-1.skill-writing`. It records the order of print and creation, and checks that the marker exists after the run. Verified by passing on 883574b and after 2.1.
- [x] 1.2 Example "a lock held too long still sends the reminder":
  - the scripted `flock` raises an assertion on any exclusive attempt without `LOCK_NB`;
  - the test requires every attempt to start before 5 seconds.
  Verified by a mutant without `LOCK_NB` failing it.
- [x] 1.3 Example "a lock taken after the deadline is let go": a new in-process test marked `spec-example: skill-writing-reminder / a lock taken after the deadline is let go`. Verified by failing on 883574b and passing after 2.1.
- [x] 1.4 Example "a lock error other than busy sends the reminder at once": a new in-process test marked `spec-example: skill-writing-reminder / a lock error other than busy sends the reminder at once`. Verified by passing on 883574b and after 2.1, because it states existing behaviour.

- [x] 1.5 Added after spectra-verify:
  - the late-lock Example becomes a two-row table (5.0 and 5.1 seconds), and its test checks that the lock is free after the run;
  - the ENOLCK test uses the scripted clock and `flock`.
  Verified by mutants: one that keeps a lock taken at exactly 5.0 seconds fails, and one that does not release the late lock fails.

## 2. Script

- [x] 2.1 For the requirement "The session marker is private to the user and written after the reminder is sent": in plugins/skill-best-practices/scripts/skill_writing_reminder.py, `_lock` releases a lock it holds once the clock reads the deadline or later, and returns None. Verified by 1.3.

## 3. Whole suite

- [x] 3.1 `python3 -m pytest -q plugins/skill-best-practices/tests tests` passes, and the mutants of 1.2 and 1.3 fail their tests.
