## MODIFIED Requirements

### Requirement: The session marker is private to the user and written after the reminder is sent

The skill-writing reminder hook SHALL read the rule file before it looks at or writes a marker; when the read fails it SHALL add no context and write no marker. It SHALL keep session markers only where it can verify their directory: on a platform with a user id, file calls relative to an open directory (open, stat and mkdir), stat without following a symlink, `O_DIRECTORY`, `O_NOFOLLOW` and `fcntl`. There the directory is `<temp dir>/skill-best-practices-<uid>`, where `<temp dir>` is the system temp directory (`TMPDIR` when it is set and usable). The hook SHALL open the temp directory and trust it only when `fstat` on that open directory shows a directory owned by the current user or by root that either gives group and others no write permission or has the sticky bit set. Only then SHALL it create the marker directory with mode 0700 when it is missing, SHALL open it relative to the temp directory without following a symlink, and SHALL trust it only when `fstat` on the open directory shows a directory owned by the current user with no permission bits for group or others. Every marker operation SHALL be made relative to that open directory. On any other platform, and whenever the temp directory cannot be found, opened or trusted, or the marker directory cannot be opened or trusted, the hook SHALL write no marker and SHALL send the reminder on every Write or Edit of a SKILL.md. With a trusted directory it SHALL hold an exclusive lock on a lock file in that directory, separate from the markers, while it checks for the session's marker, prints the context when there is none, and only then creates the marker without following a symlink and failing when it exists. It SHALL try the lock without blocking and retry until 5 seconds have passed since its first attempt; it SHALL wait no longer between attempts than the time left, and SHALL start no attempt once the 5 seconds have passed. A lock it finds taken once the 5 seconds have passed SHALL be let go as if no attempt had succeeded, and an error from the lock other than its being busy SHALL end the wait at once. When no attempt succeeds it SHALL send the reminder and write no marker. The hook checks owners and permission bits only: an access-control list that an owner of these directories or root has set is outside what it checks. No executable check covers a directory swapped between its open and its use, nor the platforms the hook does not verify: the suite runs on macOS and Linux, so review covers them.

#### Scenario: An untrusted marker directory never silences the reminder

- **WHEN** the marker directory is a symlink, is not a directory, or is open to group or others, or the temp directory holding it lets others write to it without the sticky bit
- **THEN** every Write or Edit of a SKILL.md in the session gets the reminder and no marker is written

##### Example: a symlinked marker directory is refused

- **GIVEN** `TMPDIR` set to a temporary directory in which `skill-best-practices-<uid>` is a symlink to a directory `elsewhere` beside it
- **WHEN** scripts/skill_writing_reminder.py runs twice on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** both runs print additionalContext containing the rule 5 item, and `elsewhere` is still empty

##### Example: a marker directory open to others is refused

- **GIVEN** `TMPDIR` set to a temporary directory in which `skill-best-practices-<uid>` is a directory with mode 0777
- **WHEN** scripts/skill_writing_reminder.py runs twice on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** both runs print additionalContext containing the rule 5 item, and the directory is still empty

##### Example: a temp directory open to others without the sticky bit is refused

- **GIVEN** `TMPDIR` set to a temporary directory with mode 0777
- **WHEN** scripts/skill_writing_reminder.py runs twice on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** both runs print additionalContext containing the rule 5 item, and the temporary directory is still empty

##### Example: who may own the temp directory

The hook script is loaded in the test process and its temp-directory check is given a stat result for a directory with the owner and mode below.

| Owner | Mode | Trusted |
| --- | --- | --- |
| the current user | 0700 | yes |
| root | 1777 | yes |
| another user | 0700 | no |
| another user | 1777 | no |
| the current user | 0777 | no |
| the current user | 1777 | yes |

##### Example: a regular file in place of the marker directory is refused

- **GIVEN** `TMPDIR` set to a temporary directory in which `skill-best-practices-<uid>` is a regular file
- **WHEN** scripts/skill_writing_reminder.py runs twice on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** both runs print additionalContext containing the rule 5 item, and the file still holds what it held before

#### Scenario: A failed read leaves the session unmarked

- **WHEN** the hook cannot read the rule file
- **THEN** it adds no context and writes no marker, so a later edit in the same session still gets the reminder

##### Example: a failed read leaves the session unmarked

- **GIVEN** a copy of scripts/skill_writing_reminder.py in a temporary `plugin/scripts/` with no `plugin/rules/skill-writing.md`, and `TMPDIR` set to a separate temporary directory
- **WHEN** the copy runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1, then `plugin/rules/skill-writing.md` is created with the text of the real rule file, then the copy runs on the same input again
- **THEN** the first run prints nothing and the second prints additionalContext containing the rule 5 item


#### Scenario: What the hook cannot verify still gets the reminder

- **WHEN** no temp directory can be found, or the platform lacks what the hook needs to verify the directory
- **THEN** every Write or Edit of a SKILL.md gets the reminder and no marker is written

##### Example: no temp directory still sends the reminder

- **GIVEN** the hook script loaded in the test process with `tempfile.gettempdir` raising `FileNotFoundError`
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it prints additionalContext containing the rule 5 item

##### Example: a platform that cannot verify the directory writes no marker

- **GIVEN** the hook script loaded in the test process with its platform check answering no, and `tempfile.tempdir` set to an empty temporary directory
- **WHEN** its `main()` runs twice on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** both runs print additionalContext containing the rule 5 item, and the temporary directory is still empty

#### Scenario: A shared temp directory with the sticky bit keeps markers

- **WHEN** the temp directory is owned by the current user or by root, lets others write to it, and has the sticky bit set
- **THEN** the hook keeps session markers in its private directory there

##### Example: a sticky shared temp directory keeps markers

- **GIVEN** `TMPDIR` set to a temporary directory with mode 1777
- **WHEN** scripts/skill_writing_reminder.py runs twice on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** the first run prints additionalContext containing the rule 5 item and the second prints nothing

#### Scenario: The marker check runs under the session lock

- **WHEN** another call holds the lock while the hook runs
- **THEN** the hook keeps trying until it takes the lock or the 5 seconds have passed, and once it holds the lock decides on the marker as it stands at that moment

##### Example: the check runs under the session lock

- **GIVEN** the hook script loaded in the test process with `tempfile.tempdir` set to a temporary directory, a clock that stands still, and a `flock` that answers busy on the first two attempts and, on the third, creates `s-1.skill-writing` in the marker directory and then takes the lock
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it attempted the lock three times and printed nothing

##### Example: the print and the marker write happen under the lock

- **GIVEN** the hook script loaded in the test process with `tempfile.tempdir` set to an empty temporary directory
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it prints additionalContext containing the rule 5 item and then creates `s-1.skill-writing`, a second descriptor finds the lock taken both when the hook prints and when that creation has succeeded, and `s-1.skill-writing` exists after the run

#### Scenario: A lock still busy after 5 seconds sends the reminder

- **WHEN** the lock is still busy 5 seconds after the hook's first attempt
- **THEN** the hook sends the reminder, writes no marker, and starts no further attempt

##### Example: a lock held too long still sends the reminder

- **GIVEN** the hook script loaded in the test process with `tempfile.tempdir` set to a temporary directory, a clock that advances only by what the hook sleeps, and a `flock` that answers busy on every attempt
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it prints additionalContext containing the rule 5 item, it attempted the lock more than once, every attempt asked for a non-blocking lock and started while the clock read less than 5 seconds, its sleeps add up to 5 seconds and none is longer than the time left, and the marker directory holds only `.lock`

##### Example: a lock freed after the deadline is not taken

- **GIVEN** the hook script loaded in the test process with `tempfile.tempdir` set to a temporary directory, a clock that advances by what the hook sleeps plus 0.03 seconds each time, and a `flock` that answers busy while the clock reads less than 5 seconds and otherwise creates `s-1.skill-writing` in the marker directory and takes the lock
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it prints additionalContext containing the rule 5 item, every attempt was made while the clock read less than 5 seconds, and the marker directory holds only `.lock`

##### Example: a lock taken after the deadline is let go

The hook script is loaded in the test process with `tempfile.tempdir` set to a temporary directory and a clock that advances only by what the hook sleeps. Its `flock` answers busy while the clock reads less than 4.9 seconds; otherwise it moves the clock to the reading below, creates `s-1.skill-writing` in the marker directory and takes the lock. `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1.

| Clock when the lock is taken | Printed | Lock free after the run |
| --- | --- | --- |
| 5.0 seconds | additionalContext containing the rule 5 item | yes |
| 5.1 seconds | additionalContext containing the rule 5 item | yes |

#### Scenario: A lock error other than busy ends the wait

- **WHEN** taking the lock fails with an error other than its being busy
- **THEN** the hook stops trying, sends the reminder and writes no marker

##### Example: a lock error other than busy sends the reminder at once

- **GIVEN** the hook script loaded in the test process with `tempfile.tempdir` set to a temporary directory and a `flock` that raises an `OSError` with errno `ENOLCK` on every attempt
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it prints additionalContext containing the rule 5 item, it attempted the lock once, and the marker directory holds only `.lock`

