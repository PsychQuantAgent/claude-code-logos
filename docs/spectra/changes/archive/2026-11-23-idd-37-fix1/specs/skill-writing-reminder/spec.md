## MODIFIED Requirements

### Requirement: The session marker is private to the user and written after the reminder is sent

The skill-writing reminder hook SHALL read the rule file before it looks at or writes a marker; when the read fails it SHALL add no context and write no marker. It SHALL keep session markers only where it can verify their directory: on a platform with a user id, file calls relative to an open directory (open, stat and mkdir), `O_DIRECTORY`, `O_NOFOLLOW` and `fcntl`. There the directory is `<temp dir>/skill-best-practices-<uid>`, where `<temp dir>` is the system temp directory (`TMPDIR` when it is set and usable); the hook SHALL create it with mode 0700 when it is missing, SHALL open it relative to the temp directory without following a symlink, and SHALL trust it only when `fstat` on the open directory shows a directory owned by the current user with no permission bits for group or others. Every marker operation SHALL be made relative to that open directory. On any other platform, and whenever the temp directory cannot be found or the directory cannot be opened or trusted, the hook SHALL write no marker and SHALL send the reminder on every Write or Edit of a SKILL.md. With a trusted directory it SHALL hold an exclusive lock on a lock file in that directory, separate from the markers, while it checks for the session's marker, prints the context when there is none, and only then creates the marker without following a symlink and failing when it exists; when the lock cannot be taken within 5 seconds it SHALL send the reminder and write no marker. No executable check covers a directory swapped between its open and its use, nor the platforms the hook does not verify: the suite runs on macOS and Linux, so review covers them.

#### Scenario: An untrusted marker directory never silences the reminder

- **WHEN** the marker directory is a symlink, is not a directory, or is open to group or others
- **THEN** every Write or Edit of a SKILL.md in the session gets the reminder and no marker is written

##### Example: a symlinked marker directory is refused

- **GIVEN** `TMPDIR` set to a temporary directory in which `skill-best-practices-<uid>` is a symlink to a directory `elsewhere` beside it
- **WHEN** scripts/skill_writing_reminder.py runs twice on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** both runs print additionalContext containing the rule 5 item, and `elsewhere` is still empty

##### Example: a marker directory open to others is refused

- **GIVEN** `TMPDIR` set to a temporary directory in which `skill-best-practices-<uid>` is a directory with mode 0777
- **WHEN** scripts/skill_writing_reminder.py runs twice on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** both runs print additionalContext containing the rule 5 item, and the directory is still empty

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

#### Scenario: The marker check runs under the session lock

- **WHEN** another call holds the lock while the hook runs
- **THEN** the hook waits, and decides on the marker as it stands when the lock is released

##### Example: the check runs under the session lock

- **GIVEN** `TMPDIR` set to a temporary directory holding `skill-best-practices-<uid>` with mode 0700, and the test holding an exclusive lock on its `.lock` file
- **WHEN** scripts/skill_writing_reminder.py starts on an Edit of /repo/skills/y/SKILL.md with session_id s-1, and, while it has not finished, the test creates `s-1.skill-writing` in that directory and then releases the lock
- **THEN** the hook has not finished before the release, and prints nothing

##### Example: a lock held too long still sends the reminder

- **GIVEN** the hook script loaded in the test process with its lock wait set to 0.2 seconds, `tempfile.tempdir` set to a temporary directory holding `skill-best-practices-<uid>` with mode 0700, and the test holding an exclusive lock on its `.lock` file
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it prints additionalContext containing the rule 5 item, and the directory holds only `.lock`
