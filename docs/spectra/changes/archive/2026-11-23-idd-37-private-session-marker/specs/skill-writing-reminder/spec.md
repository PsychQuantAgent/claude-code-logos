## ADDED Requirements

### Requirement: The session marker is private to the user and written after the reminder is sent

The skill-writing reminder hook SHALL keep its session markers in `<temp dir>/skill-best-practices-<uid>`, where `<temp dir>` is the system temp directory (`TMPDIR` when it is set and usable) and `<uid>` the current user id, or the user name where the platform has no user id, and SHALL create that directory with mode 0700 when it is missing. It SHALL trust the directory only when `lstat` shows a directory that is not a symlink and, where the platform has a user id, is owned by the current user with no permission bits for group or others. With an untrusted directory it SHALL send the reminder on every Write or Edit of a SKILL.md and SHALL write no marker. It SHALL read the rule file before it looks at or writes a marker: when the read fails it SHALL add no context and write no marker; otherwise, when no marker for the session exists in a trusted directory, it SHALL print the context and only then create the marker, without following a symlink and failing when the marker already exists. No executable check covers the platform without a user id (Windows): the suite runs on macOS and Linux, so review covers that branch.

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
