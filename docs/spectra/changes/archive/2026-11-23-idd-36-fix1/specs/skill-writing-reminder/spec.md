## MODIFIED Requirements

### Requirement: The skill-writing reminder states the naming rule

When the PreToolUse hook for Write and Edit receives a path whose final component is exactly SKILL.md, in a session that has not had the reminder yet, the context it adds SHALL contain rule 5 of plugins/skill-best-practices/rules/skill-writing.md, "Names identify, descriptions get found". Rule 5 SHALL say that it summarizes Practice 9 and SHALL point to Practice 9; SHALL name Practice 9 and its source (Furnas et al., 1987); SHALL say that no name can be relied on to be guessed; SHALL state where each naming rule applies: in a new plugin or one renamed as a whole, the short-name prefix and the shape for each kind of skill, with two content words as the target and three at most; in an existing plugin, that plugin's current names; for a skill outside any plugin, no prefix; and SHALL say that the description lists several phrasings users actually say and gains, as a short phrase with no private details, any wording that failed to reach the skill. Rule 5 SHALL NOT contain a sentence that applies the shapes to every skill. A later Write or Edit of a SKILL.md in the same session SHALL add no context, and a path whose final component is not exactly SKILL.md SHALL add none.

#### Scenario: Rule 5 is sent with the reminder

- **WHEN** the hook receives an Edit of a SKILL.md path in a session that has not had the reminder yet
- **THEN** the rule 5 item in the added context names Practice 9 and its source, says no name can be relied on to be guessed, and points to Practice 9

##### Example: rule 5 names Practice 9 and its source

- **GIVEN** the hook input tool_name Edit and file_path /repo/plugins/x/skills/y/SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs and the item that starts with "5. **Names identify, descriptions get found**" is taken from additionalContext
- **THEN** that item contains "(Practice 9)", "(Furnas et al., 1987)", "no name can be relied on to be guessed", "This item summarizes Practice 9" and "read Practice 9 before choosing a name"

#### Scenario: Naming depends on where the skill lives

- **WHEN** the reminder states the naming rules
- **THEN** the prefix and the shapes sit inside the clause for a new or wholly renamed plugin, followed by the clause for an existing plugin and the clause for a skill outside any plugin

##### Example: a new skill in an existing plugin keeps the plugin's names

- **GIVEN** the hook input tool_name Write and file_path /repo/skills/y/SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs and the rule 5 item is taken from additionalContext
- **THEN** the item contains "in a new plugin, or one renamed as a whole", "follows that plugin's current names, prefixed or not" and "renamed as a whole or not at all"

##### Example: the shapes apply only in a new or wholly renamed plugin

- **GIVEN** the rule 5 item taken from additionalContext for an Edit of /repo/skills/y/SKILL.md
- **WHEN** the positions of its clauses are compared
- **THEN** "in a new plugin, or one renamed as a whole" comes before "conversion `short-to-product`", which comes before "a new skill in an existing plugin", which comes before "a skill outside any plugin is not given a prefix", and the item does not contain "Every name takes the shape for its kind"

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
- **THEN** the rule 5 item says the description lists several phrasings users actually say and that a wording which failed to reach the skill is added to it as a short phrase with no private details

##### Example: a failed wording goes into the description

- **GIVEN** the hook input tool_name Edit and file_path /repo/skills/y/SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs and the rule 5 item is taken from additionalContext
- **THEN** the item contains "lists the words users actually say for the job, several phrasings and not one" and "is added to the description as a short phrase with no private details"

#### Scenario: The reminder goes only to a skill file, once per session

- **WHEN** the hook receives a path whose final component is not exactly SKILL.md, or a second Write or Edit of a SKILL.md with the same session id
- **THEN** it adds no context

##### Example: a path that only ends in SKILL.md gets no reminder

- **GIVEN** the hook input tool_name Edit and file_path /repo/skills/y/NOT-SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs
- **THEN** it prints nothing

##### Example: a second skill edit in the session gets no reminder

- **GIVEN** two hook inputs with tool_name Edit, file_path /repo/skills/y/SKILL.md and session_id s-1, and a third with session_id s-2, all with the same temporary directory
- **WHEN** scripts/skill_writing_reminder.py runs on each in order
- **THEN** the first prints the reminder, the second prints nothing, and the third prints the reminder

### Requirement: The plugin lists Practice 9 with its other practices

The plugin's own files SHALL list Practice 9: the skill document SHALL have the heading line "## Practice 9: Names Identify, Descriptions Get Found" and, under its "### When a skill isn't performing" section, a numbered question that ends with "? (Practice 9)"; the plugin's CLAUDE.md SHALL have the Practice 9 row of its research table. The repository's files SHALL count nine practices wherever they state a count, SHALL list the Practice 9 research row in README.md, and the marketplace entry for skill-best-practices SHALL carry the same version as the plugin's plugin.json.

#### Scenario: The plugin's own files list Practice 9

- **WHEN** the files inside plugins/skill-best-practices are read
- **THEN** the heading, the audit question and the research row for Practice 9 are each in their place

##### Example: the plugin's own files list Practice 9

| File | Expected |
| ---- | -------- |
| plugins/skill-best-practices/skills/skill-best-practices/SKILL.md | a line that is exactly "## Practice 9: Names Identify, Descriptions Get Found" |
| plugins/skill-best-practices/skills/skill-best-practices/SKILL.md | under "### When a skill isn't performing", before the next heading, a line that starts with a number and ends with "? (Practice 9)" |
| plugins/skill-best-practices/CLAUDE.md | \| 9 \| Names identify, descriptions get found \| Furnas, Landauer, Gomez, & Dumais (1987) \| |

#### Scenario: The repository's files count nine practices

- **WHEN** the repository files outside the plugin are read
- **THEN** each stated count is nine and the marketplace version matches the plugin version

##### Example: the repository's files count nine practices

| File | Expected |
| ---- | -------- |
| README.md | "Nine evidence-based practices" and the row starting "\| The vocabulary problem \| Furnas, Landauer, Gomez, & Dumais (1987) \|" |
| CLAUDE.md | "全部 9 個 practice" and "九個 practice", and no "8 個 practice" or "八個 practice" |
| .claude-plugin/marketplace.json | the skill-best-practices entry's description contains "9 practices" and its version equals the version in plugins/skill-best-practices/.claude-plugin/plugin.json |

### Requirement: Practice 9 reports its source faithfully

Every number, quotation and finding that the Practice 9 section of the skill document attributes to Furnas et al. (1987) SHALL be stated on the page it cites, together with the conditions and qualifiers the page attaches to it, and a claim that the paper does not make SHALL NOT be attributed to it. Claims drawn from elsewhere (the naming grammar and the no-piecemeal-renaming rule from PsychQuant/che-plugin-devtools#74, the "I want to ___" test from PsychQuant/che-plugin-devtools#28, the Claude Code behaviour from its documentation, the observed case from PsychQuant/plaud-mcp-connector#65) SHALL name their own source.

#### Scenario: A claim is compared with its cited page

- **WHEN** a Practice 9 claim attributed to Furnas et al. (1987) is compared with the cited page
- **THEN** the page states the claim with no condition or qualifier dropped, and claims from elsewhere name their own source

No executable check: the paper's full text is copyrighted and kept outside the repository, so the comparison with its page images is done by hand; the record of each comparison is the source-check comment on PsychQuantAgent/claude-code-logos#36.
