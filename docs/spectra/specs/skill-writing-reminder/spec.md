# skill-writing-reminder Specification

## Purpose

The skill-writing reminder is the guidance the skill-best-practices plugin sends to a session that is about to write or edit a skill file, together with the places where the plugin lists its practices. It exists so that a session writing a skill applies the plugin's evidence-based practices without first loading the full skill.

## Requirements

### Requirement: The skill-writing reminder states the naming rule

When the PreToolUse hook for Write and Edit sees a path that ends in SKILL.md, the context it adds SHALL contain rule 5 of plugins/skill-best-practices/rules/skill-writing.md, "Names identify, descriptions get found". Rule 5 SHALL name Practice 9 and its source (Furnas et al., 1987), SHALL say that no name can be relied on to be guessed, SHALL limit the short-name prefix to new plugins and plugins renamed as a whole, SHALL give the name shape for each kind of skill with two content words as the target and three at most, and SHALL say that the description lists the words users actually say and gains any wording that failed to reach the skill.

#### Scenario: Rule 5 is sent with the reminder

- **WHEN** the hook receives an Edit of a SKILL.md path in a session that has not had the reminder yet
- **THEN** the added context names Practice 9, cites Furnas et al. (1987), and says no name can be relied on to be guessed

##### Example: rule 5 names Practice 9 and its source

- **GIVEN** the hook input tool_name Edit and file_path /repo/plugins/x/skills/y/SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs
- **THEN** additionalContext contains "Names identify, descriptions get found", "(Practice 9)", "(Furnas et al., 1987)" and "no name can be relied on to be guessed"

#### Scenario: The prefix applies to new or wholly renamed plugins

- **WHEN** the reminder states the short-name prefix
- **THEN** it limits the prefix to a new plugin or one renamed as a whole, and tells a new skill in an existing plugin to follow that plugin's current names

##### Example: a new skill in an existing plugin keeps the plugin's names

- **GIVEN** the hook input tool_name Write and file_path /repo/skills/y/SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs
- **THEN** additionalContext contains "in a new plugin, or one renamed as a whole", "follows that plugin's current names, prefixed or not" and "renamed as a whole or not at all"

#### Scenario: Names take the shape for their kind

- **WHEN** the reminder states how a name is built
- **THEN** it lists the shape for each kind of skill and the word limit

##### Example: the five shapes and the word limit

| Expected text in additionalContext | Notes |
| ---------------------------------- | ----- |
| short-to-product | conversion |
| short-[object-]verb | action |
| query or settings `short-noun` | query or settings |
| orchestration `short-mode` | orchestration |
| norms and personas `short-noun` | norms and personas |
| two content words as the target and three at most | word limit |

#### Scenario: Descriptions carry the words users say

- **WHEN** the reminder states what a description holds
- **THEN** it says the description lists the words users actually say and that a wording which failed to reach the skill is added to it

##### Example: a failed wording goes into the description

- **GIVEN** the hook input tool_name Edit and file_path /repo/skills/y/SKILL.md
- **WHEN** scripts/skill_writing_reminder.py runs
- **THEN** additionalContext contains "lists the words users actually say for the job" and "a wording that once failed to reach the skill is added to the description"

---
### Requirement: The plugin lists Practice 9 with its other practices

The skill document, its audit checklist, the plugin's research table and the repository README SHALL each list Practice 9, so that the count of practices is the same wherever the plugin states it.

#### Scenario: Every list of practices includes Practice 9

- **WHEN** the plugin's files are read
- **THEN** each place that lists the practices includes Practice 9

##### Example: four places list Practice 9

| File | Expected text |
| ---- | ------------- |
| plugins/skill-best-practices/skills/skill-best-practices/SKILL.md | ## Practice 9: Names Identify, Descriptions Get Found |
| plugins/skill-best-practices/skills/skill-best-practices/SKILL.md | an audit question that ends with "(Practice 9)" |
| plugins/skill-best-practices/CLAUDE.md | \| 9 \| Names identify, descriptions get found \| Furnas, Landauer, Gomez, & Dumais (1987) \| |
| README.md | Nine evidence-based practices |

---
### Requirement: Practice 9 reports its source faithfully

Every number, quotation and finding that the Practice 9 section of the skill document attributes to Furnas et al. (1987) SHALL be stated on the page it cites, and a claim that the paper does not make SHALL NOT be attributed to it.

#### Scenario: A reader checks a claim against the cited page

- **WHEN** a reviewer compares a Practice 9 claim with the cited page of Furnas et al. (1987)
- **THEN** the page states the claim, and claims drawn from elsewhere (such as the PsychQuant/che-plugin-devtools#74 grammar) are attributed to their own source

No executable check: the paper is a scanned PDF held outside the repository (copyrighted full text), so the comparison is made by a reviewer reading the page images, recorded in the verify report for PsychQuantAgent/claude-code-logos#36.
