## Why

The skill-best-practices plugin has no practice on naming skills. The naming grammar decided in PsychQuant/che-plugin-devtools#74 rested on the claim that a well-formed name tells people what a skill does. Furnas, Landauer, Gomez, and Dumais (1987) found that no naming rule makes a name guessable, and that what gets an object found is a list of the words people actually use (PsychQuantAgent/claude-code-logos#36). The plugin's runtime rule, sent to every session that writes a skill file, should carry the grammar with the corrected rationale and the two description rules that follow from the paper.

## What Changes

- The skill-writing reminder (the PreToolUse Write|Edit hook that sends plugins/skill-best-practices/rules/skill-writing.md when a SKILL.md is written) gains rule 5, "Names identify, descriptions get found": the short-name prefix for new or wholly renamed plugins, the existing plugin's convention for a new skill in it, the name shape for each kind of skill with two content words as the target and three at most, the statement that no name can be relied on to be guessed, and the two description rules (list the words users actually say; add a wording that failed to reach the skill).
- The skill document gains a Practice 9 section with the research and page numbers, audit question 9, and new trigger words in its frontmatter description.
- The plugin's research table, the repository README and the repository CLAUDE.md count nine practices; the plugin version goes from 0.3.0 to 0.4.0.

## Non-Goals

- No naming check is added here. Checking names and descriptions when a skill is created belongs to harness-devtools (PsychQuant/che-plugin-devtools#74).
- Existing skills are not renamed; the rule itself says a plugin is renamed as a whole or not at all.
- Practices 1 to 8 get no spec in this change. Only the behaviour this change adds is specified.
- No new hook is added. Rule 5 is delivered by the existing skill-writing reminder.

## Capabilities

### New Capabilities

- `skill-writing-reminder`: what the skill-best-practices plugin tells a session that is writing a skill file, and where the plugin lists its practices

### Modified Capabilities

(none)

## Impact

- Affected specs: skill-writing-reminder (new)
- Affected code:
  - Modified: plugins/skill-best-practices/rules/skill-writing.md
  - Modified: plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
  - Modified: plugins/skill-best-practices/CLAUDE.md
  - Modified: plugins/skill-best-practices/.claude-plugin/plugin.json
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
  - Modified: .claude-plugin/marketplace.json
  - Modified: README.md
  - Modified: CLAUDE.md
