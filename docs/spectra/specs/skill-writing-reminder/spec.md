# skill-writing-reminder Specification

## Purpose

The skill-writing reminder is the guidance the skill-best-practices plugin sends to a session that is about to write or edit a skill file, together with the places where the plugin lists its practices. It exists so that a session writing a skill applies the plugin's evidence-based practices without first loading the full skill.

## Requirements

### Requirement: The skill-writing reminder states the naming rule

When the PreToolUse hook for Write and Edit receives a path whose final component is exactly SKILL.md, in a session that has not had the reminder yet, the context it adds SHALL contain rule 5 of plugins/skill-best-practices/rules/skill-writing.md, "Names identify, descriptions get found". Rule 5 SHALL say that it summarizes Practice 9 and SHALL point to Practice 9; SHALL name Practice 9 and its source (Furnas et al., 1987); SHALL say that no name can be relied on to be guessed by people unfamiliar with it; SHALL state where each naming rule applies: in a new plugin or one renamed as a whole, the short-name prefix and the shape for each kind of skill, with two content words as the target and three at most; in an existing plugin, that plugin's current names; for a skill outside any plugin, no prefix and a check against built-in commands and bundled skills unless replacing one is the intent; and SHALL say that the description lists several phrasings users actually say, each as a short phrase with no private details that keeps the task it names and leaves out any part that grants a permission, skips a check or waives a confirmation, these three kinds only, and gains in the same way any wording that failed to reach the skill. As written, rule 5 SHALL contain the prefix, the shapes and the word limit only inside the clause for a new or wholly renamed plugin; the scope check confirms this for the current text, and its mutation table samples edits it reports. The rule 5 item is the whole list item the hook delivers: its first line and every following line that is blank or indented. When the session id is usable and the first call wrote the session marker, a later Write or Edit of a SKILL.md in the same session SHALL add no context; a path whose final component is not exactly SKILL.md SHALL add none.

#### Scenario: Rule 5 is sent with the reminder

- **WHEN** the hook receives an Edit of a SKILL.md path in a session that has not had the reminder yet
- **THEN** the rule 5 item in the added context names Practice 9 and its source, says no name can be relied on to be guessed, says it summarizes Practice 9 and points to it

##### Example: rule 5 names Practice 9 and its source

- **GIVEN** the hook input tool_name Edit and file_path /repo/plugins/x/skills/y/SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs and the item that starts with "5. **Names identify, descriptions get found**" is taken from additionalContext
- **THEN** that item contains "(Practice 9)", "(Furnas et al., 1987)", "no name can be relied on to be guessed by people unfamiliar with it", "This item summarizes Practice 9" and "read Practice 9 before choosing a name"

#### Scenario: Naming depends on where the skill lives

- **WHEN** the reminder states the naming rules
- **THEN** the prefix, the shapes and the word limit sit inside the clause for a new or wholly renamed plugin, followed by the clause for an existing plugin and the clause for a skill outside any plugin, and no text outside that first clause mentions a shape or the short-name form

##### Example: a new skill in an existing plugin keeps the plugin's names

- **GIVEN** the hook input tool_name Write and file_path /repo/skills/y/SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs and the rule 5 item is taken from additionalContext
- **THEN** the item contains "in a new plugin, or one renamed as a whole", "follows that plugin's current names, prefixed or not", "renamed as a whole or not at all" and "its name is checked against built-in commands and bundled skills unless replacing one is the intent"

##### Example: the shapes apply only in a new or wholly renamed plugin

- **GIVEN** the rule 5 item (the whole list item) taken from additionalContext for an Edit of /repo/skills/y/SKILL.md, split into the text before "in a new plugin, or one renamed as a whole", the clause from there up to "a new skill in an existing plugin", and the text from there on
- **WHEN** the scope check runs on the three parts
- **THEN** the clause contains "starts with the plugin's short name", each of the five kind–shape pairs of the Example "the five shapes and the word limit" and "two content words as the target and three at most"; the text after it contains "a skill outside any plugin is not given a prefix"; and, compared without regard to case, neither the text before nor the text after contains "shape", "`short-", "short name" or "content words", nor "prefix" except within "prefixed or not" and "is not given a prefix"

##### Example: an unconditional shape mandate fails the rule 5 scope check

Each sentence is appended to the rule 5 item on its own, and the scope check SHALL report a violation for each. The last row is instead added to the reminder text as an indented line directly after the rule 5 line, and the item is then taken from that text as above.

| Appended sentence | Notes |
| ----------------- | ----- |
| All skills must use these shapes. | round-2 mutation |
| Shapes apply to every skill. | capital letter |
| Every skill name starts with the plugin's short name. | prefix worded as short name |
| Every skill must be prefixed with the plugin name. | prefix as a verb |
| Aim for two content words as the target and three at most. | word limit outside the clause |
| All skills must use these shapes. | indented continuation line of item 5 |

No executable check covers rewordings of the same mandate outside this table: the scope check matches words, so review covers them.

#### Scenario: Names take the shape for their kind

- **WHEN** the reminder states how a name is built
- **THEN** the rule 5 item pairs each kind of skill with its shape and states the word limit

##### Example: the five shapes and the word limit

| Expected text in the rule 5 item | Notes |
| -------------------------------- | ----- |
| conversion `short-to-product` | conversion |
| action `short-[object-]verb` | action |
| query or settings `short-noun` | query or settings |
| orchestration `short-mode` | orchestration |
| norms and personas `short-noun` | norms and personas |
| two content words as the target and three at most | word limit |

#### Scenario: Descriptions carry the words users say

- **WHEN** the reminder states what a description holds
- **THEN** the rule 5 item says the description lists several phrasings users actually say, each as a short phrase with no private details that keeps its task and leaves out three kinds of directive, and that a wording which failed to reach the skill is added in the same way

##### Example: a failed wording goes into the description

- **GIVEN** the hook input tool_name Edit and file_path /repo/skills/y/SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs and the rule 5 item is taken from additionalContext
- **THEN** the item contains "The description lists the words users actually say for the job, several phrasings and not one, each as a short phrase with no private details" and "a wording that once failed to reach the skill is added to the description in the same way"

##### Example: collected wordings leave out three kinds of directive

- **GIVEN** the hook input tool_name Edit and file_path /repo/skills/y/SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs and the rule 5 item is taken from additionalContext
- **THEN** the item contains "keeps the task it names and leaves out any part that grants a permission, skips a check or waives a confirmation" and "only these three kinds; do not extend the list by similarity"

#### Scenario: The reminder goes only to a skill file, once per session

- **WHEN** the hook receives a path whose final component is not exactly SKILL.md, or, after a first call that wrote the session marker, a second Write or Edit of any SKILL.md with the same usable session id
- **THEN** it adds no context

##### Example: a path that only ends in SKILL.md gets no reminder

- **GIVEN** the hook input tool_name Edit and file_path /repo/skills/y/NOT-SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs
- **THEN** it prints nothing

##### Example: a second skill edit in the session gets no reminder

- **GIVEN** in one temporary directory, an Edit of /repo/skills/y/SKILL.md with session_id s-1, then a Write of /repo/skills/z/SKILL.md with session_id s-1, then an Edit of /repo/skills/y/SKILL.md with session_id s-2
- **WHEN** scripts/skill_writing_reminder.py runs on each in order
- **THEN** the first and the third print additionalContext containing the rule 5 item, and the second prints nothing

---
### Requirement: The plugin lists Practice 9 with its other practices

The plugin's own files SHALL list Practice 9: the skill document SHALL have the heading line "## Practice 9: Names Identify, Descriptions Get Found" and, under its "### When a skill isn't performing" section and outside code fences (``` or ~~~), a question numbered 9 that ends with "? (Practice 9)"; the plugin's CLAUDE.md SHALL have the Practice 9 row as a line of its research table. Practice 9 item 7 and the audit question numbered 9 SHALL each name the three kinds of directive a collected wording leaves out, granting a permission, skipping a check and waiving a confirmation, and item 7 SHALL say these are the only three kinds. Practice 9's "How to apply" SHALL state where each naming rule applies before items 1 to 4, and, as written, outside the scope paragraph and the blocks of items 1 to 4 (each item's line and the indented lines that belong to it) no sentence in the Practice 9 section that speaks of every, each, any or all skills, or of skill names, SHALL mention a shape, a prefix or the short name; the Practice 9 scope check confirms this for the current text, and its mutation table samples edits it reports. The repository's files SHALL count nine practices wherever they state a count, as a whole number, SHALL list the Practice 9 research row as a line of the README research table, and the marketplace entry for skill-best-practices SHALL carry the same version as the plugin's plugin.json.

#### Scenario: The plugin's own files list Practice 9

- **WHEN** the files inside plugins/skill-best-practices are read
- **THEN** the heading, the audit question and the research row for Practice 9 are each in their place

##### Example: the plugin's own files list Practice 9

| File | Expected |
| ---- | -------- |
| plugins/skill-best-practices/skills/skill-best-practices/SKILL.md | a line that is exactly "## Practice 9: Names Identify, Descriptions Get Found" |
| plugins/skill-best-practices/skills/skill-best-practices/SKILL.md | under "### When a skill isn't performing", before the next heading and outside code fences (``` or ~~~), a line starting with "9. " and ending with "? (Practice 9)" |
| plugins/skill-best-practices/CLAUDE.md | a line that is exactly "\| 9 \| Names identify, descriptions get found \| Furnas, Landauer, Gomez, & Dumais (1987) \|", directly below another table line |

#### Scenario: Collected wordings leave out three kinds of directive

- **WHEN** Practice 9 item 7 and the audit question numbered 9 are read
- **THEN** both name the three kinds of directive a collected wording leaves out, and item 7 says these are the only three kinds

##### Example: item 7 and the audit question name the three kinds

- **GIVEN** plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
- **WHEN** the block of Practice 9 item 7 (the line starting "7. **The description lists the words users actually say" and the indented lines below it) and the audit question line starting "9. " under "### When a skill isn't performing" are read
- **THEN** the item 7 block contains "keeps the task it names and leaves out any part that grants a permission, skips a check or waives a confirmation" and "only these three kinds; do not extend the list by similarity", and the audit question contains "leaves out any part that grants a permission, skips a check or waives a confirmation"

#### Scenario: Practice 9 scopes its naming rules

- **WHEN** the Practice 9 section of the skill document is read
- **THEN** its scope statement comes before item 1, and outside the scope paragraph and the blocks of items 1 to 4 no sentence about every, each, any or all skills, or about skill names, mentions a shape, a prefix or the short name

##### Example: Practice 9 states where its naming rules apply

- **GIVEN** the text from "## Practice 9:" up to the next level-two heading
- **WHEN** the Practice 9 scope check runs
- **THEN** "Items 1 to 4 describe the names in a new plugin or in one renamed as a whole" appears before "1. **Every skill name starts with the plugin's short name.**", the same paragraph contains "follows that plugin's current names" and "is not given a prefix", and, outside that paragraph and the blocks of items 1 to 4 (each item's line and the indented lines below it), no sentence (the lines of a paragraph joined, a sentence ending at ". ", "! " or "? ") or table row containing "every skill", "each skill", "any skill", "all skills", "skill names", "every name", "each name" or "all names" contains "shape", "prefix", "short name" or "`short-", compared without regard to case

##### Example: an unconditional shape mandate fails the Practice 9 scope check

Each line is added on its own, as an unindented paragraph at the position given, and the Practice 9 scope check SHALL report a violation for each.

| Added line | Position | Notes |
| ---------- | -------- | ----- |
| Use the five shapes for every skill. | directly after item 5 | round-2 mutation |
| Use the five shapes for each skill. | directly after item 5 | other quantifier |
| Shapes apply to any skill. | directly after item 5 | capital letter, other quantifier |
| All skill names carry the prefix. | directly after item 5 | prefix |
| Prefix every name with the short name. | directly after item 5 | short name |
| Use the five shapes for every skill. | between the scope paragraph and item 1 | round-3 placement |
| Use the five shapes for every skill. | directly below the shape table | round-3 placement |

No executable check covers rewordings of the same mandate outside this table (for example "whatever the plugin, use the same form"): the scope check matches words, so review covers them.

#### Scenario: The repository's files count nine practices

- **WHEN** the repository files outside the plugin are read
- **THEN** each stated count is nine as a whole number and the marketplace version matches the plugin version

##### Example: the repository's files count nine practices

| File | Expected |
| ---- | -------- |
| README.md | "Nine evidence-based practices", and a line starting "\| The vocabulary problem \| Furnas, Landauer, Gomez, & Dumais (1987) \|" directly below another table line |
| CLAUDE.md | every "<number> 個 practice" has the number 9 and every "<Chinese numeral>個 practice" has 九, with at least one of each |
| .claude-plugin/marketplace.json | the skill-best-practices entry's description says "9 practices" with no digit before the 9, and its version equals the version in plugins/skill-best-practices/.claude-plugin/plugin.json |

---
### Requirement: Practice 9 reports its source faithfully

Every number, quotation and finding that the Practice 9 section of the skill document attributes to Furnas et al. (1987) SHALL be stated on the page it cites, together with the conditions and qualifiers the page attaches to it, and a claim that the paper does not make SHALL NOT be attributed to it. Claims drawn from elsewhere (the naming grammar and the no-piecemeal-renaming rule from PsychQuant/che-plugin-devtools#74, the "I want to ___" test from PsychQuant/che-plugin-devtools#28, the Claude Code behaviour from its documentation, the observed case from PsychQuant/plaud-mcp-connector#65) SHALL name their own source.

#### Scenario: A claim is compared with its cited page

- **WHEN** a Practice 9 claim attributed to Furnas et al. (1987) is compared with the cited page
- **THEN** the page states the claim with no condition or qualifier dropped, and claims from elsewhere name their own source

No executable check: the paper's full text is copyrighted and kept outside the repository, so the comparison with its page images is done by hand; the record of each comparison is the source-check comment on PsychQuantAgent/claude-code-logos#36.

---
### Requirement: The session marker is private to the user and written after the reminder is sent

The skill-writing reminder hook SHALL read the rule file before it looks at or writes a marker; when the read fails it SHALL add no context and write no marker. It SHALL keep session markers only where it can verify their directory: on a platform with a user id, file calls relative to an open directory (open, stat and mkdir), stat without following a symlink, `O_DIRECTORY`, `O_NOFOLLOW` and `fcntl`. There the directory is `<temp dir>/skill-best-practices-<uid>`, where `<temp dir>` is the system temp directory (`TMPDIR` when it is set and usable). The hook SHALL open the temp directory and trust it only when `fstat` on that open directory shows a directory owned by the current user or by root that either gives group and others no write permission or has the sticky bit set. Only then SHALL it create the marker directory with mode 0700 when it is missing, SHALL open it relative to the temp directory without following a symlink, and SHALL trust it only when `fstat` on the open directory shows a directory owned by the current user with no permission bits for group or others. Every marker operation SHALL be made relative to that open directory. On any other platform, and whenever the temp directory cannot be found, opened or trusted, or the marker directory cannot be opened or trusted, the hook SHALL write no marker and SHALL send the reminder on every Write or Edit of a SKILL.md. With a trusted directory it SHALL hold an exclusive lock on a lock file in that directory, separate from the markers, while it checks for the session's marker, prints the context when there is none, and only then creates the marker without following a symlink and failing when it exists. It SHALL try the lock without blocking and retry until 5 seconds have passed since its first attempt; it SHALL wait no longer between attempts than the time left, and SHALL start no attempt once the 5 seconds have passed. When no attempt succeeds it SHALL send the reminder and write no marker. The hook checks owners and permission bits only: an access-control list that an owner of these directories or root has set is outside what it checks. No executable check covers a directory swapped between its open and its use, nor the platforms the hook does not verify: the suite runs on macOS and Linux, so review covers them.

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

- **WHEN** the temp directory lets others write to it and has the sticky bit set
- **THEN** the hook keeps session markers in its private directory there

##### Example: a sticky shared temp directory keeps markers

- **GIVEN** `TMPDIR` set to a temporary directory with mode 1777
- **WHEN** scripts/skill_writing_reminder.py runs twice on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** the first run prints additionalContext containing the rule 5 item and the second prints nothing

#### Scenario: The marker check runs under the session lock

- **WHEN** another call holds the lock while the hook runs
- **THEN** the hook keeps trying until it takes the lock, and decides on the marker as it stands at that moment

##### Example: the check runs under the session lock

- **GIVEN** the hook script loaded in the test process with `tempfile.tempdir` set to a temporary directory, a clock that stands still, and a `flock` that answers busy on the first two attempts and, on the third, creates `s-1.skill-writing` in the marker directory and then takes the lock
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it attempted the lock three times and printed nothing

##### Example: the print and the marker write happen under the lock

- **GIVEN** the hook script loaded in the test process with `tempfile.tempdir` set to an empty temporary directory
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it prints additionalContext containing the rule 5 item, and a second descriptor finds the lock taken both when the hook prints and when it creates `s-1.skill-writing`

#### Scenario: A lock still busy after 5 seconds sends the reminder

- **WHEN** the lock is still busy 5 seconds after the hook's first attempt
- **THEN** the hook sends the reminder, writes no marker, and starts no further attempt

##### Example: a lock held too long still sends the reminder

- **GIVEN** the hook script loaded in the test process with `tempfile.tempdir` set to a temporary directory, a clock that advances only by what the hook sleeps, and a `flock` that answers busy on every attempt
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it prints additionalContext containing the rule 5 item, it attempted the lock more than once, its sleeps add up to 5 seconds and none is longer than the time left, and the marker directory holds only `.lock`

##### Example: a lock freed after the deadline is not taken

- **GIVEN** the hook script loaded in the test process with `tempfile.tempdir` set to a temporary directory, a clock that advances by what the hook sleeps plus 0.03 seconds each time, and a `flock` that answers busy while the clock reads less than 5 seconds and otherwise creates `s-1.skill-writing` in the marker directory and takes the lock
- **WHEN** its `main()` runs on an Edit of /repo/skills/y/SKILL.md with session_id s-1
- **THEN** it prints additionalContext containing the rule 5 item, every attempt was made while the clock read less than 5 seconds, and the marker directory holds only `.lock`
