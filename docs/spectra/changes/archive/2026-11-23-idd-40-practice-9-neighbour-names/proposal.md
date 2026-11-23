## Why

Practice 9 judges a skill name by its grammar (items 1 to 5) and by whether it says what the skill is (item 6), and leaves open how to tell apart two names that both pass (PsychQuantAgent/claude-code-logos#40). Three studies of text-editor command names, read in full on #40, support one more check: read a name next to the other names it sits with. Black and Moran (1982), Landauer, Galotti and Hartwell (1983) and Rosenberg (1982) found that general names, names that could refer to several operations, and near-synonyms of another name in the set did worse. They found nothing about remembering or typing a name beyond what item 4 already says.

## What Changes

- Practice 9 gains a research paragraph, "Research on names within a set". It reports what the three studies found, with page numbers and their qualifiers, and records that they add nothing on remembering or typing a name beyond item 4.
- Practice 9 gains item 9, "Check the name against the other names in its listing". Read the name next to the other skill names in its plugin, or in the same skills directory for a skill outside any plugin. Do not choose a near-synonym of a name already there, or a word general enough to fit several of those skills. Give jobs with different inputs or effects different names. Item 9 says that its sources studied people learning six to ten text-editor commands, and that the near-synonym part rests on a post hoc analysis.
- The scope line becomes "Items 6 to 9". Audit question 9 asks the same check, and the Sources list gains the three works.
- Rule 5 of the skill-writing reminder carries the check with its sources.
- skill-best-practices goes from 0.4.1 to 0.5.0, in the plugin manifest and in the marketplace entry.
- The spec adds a requirement for item 9 with two Examples and their tests, and extends "Practice 9 reports its source faithfully" to the three new works.

## Non-Goals

- A mechanical near-synonym check. The sources give no way to detect near-synonyms, so a synonym list would be invented and presented as research; the tests pin the text only.
- Renumbering the items of Practice 9. Items 7 and 8 keep their numbers because the spec, the tests and the audit question name item 7.
- Guessability, which Furnas et al. (1987, p. 967) rule out, and the naming grammar of PsychQuant/che-plugin-devtools#74.
- The research rows of the plugin CLAUDE.md and the README, which stay on Furnas et al. (1987). The spec pins both lines.
- The two *Human Factors* (1984) papers, which were not read.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `skill-writing-reminder`: Practice 9 and rule 5 judge a name against the other names in its plugin. The source requirement covers the three new works.

## Impact

- Affected specs: skill-writing-reminder (modified)
- Affected code:
  - Modified: plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
  - Modified: plugins/skill-best-practices/rules/skill-writing.md
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
  - Modified: plugins/skill-best-practices/.claude-plugin/plugin.json
  - Modified: .claude-plugin/marketplace.json
