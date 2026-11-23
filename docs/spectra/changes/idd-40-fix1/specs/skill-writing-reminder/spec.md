## MODIFIED Requirements

### Requirement: Practice 9 judges a name against the names around it

Practice 9 SHALL have exactly one numbered item 9. Outside code fences, the Practice 9 section SHALL contain exactly one line starting "9. ". That line SHALL start with "9. **Check the name against the other names in its listing.**" and SHALL come after the line starting "8. ". Item 9 SHALL tell the author:
- to read a name next to the other skill names in its plugin, or, for a skill outside any plugin, next to the other skills in the same skills directory;
- to flag a candidate that is a near-synonym of a neighbour, or general enough to fit several of the neighbouring skills;
- to prefer a name that shows what sets the skill apart, when such a name fits the plugin's naming convention;
- to record an overlap between names a plugin already has for a whole-plugin rename under item 5;
- that skills with different arguments, syntax or effects should not differ only by near-synonyms.

Item 9 SHALL also say that this check does not split a skill or override the naming grammar. Item 9 SHALL state the limits of its evidence: the near-synonym part rests on a post hoc analysis; general words did worst on learning and cued choice in one study; and the studies had people learn or match six to ten text-editor commands, not a model choose from a skill listing. Item 9 SHALL NOT forbid a name outright. The audit question numbered 9 SHALL ask the same check with the same comparison set. Rule 5 of the skill-writing reminder SHALL carry the check as a flag, with the same comparison set; SHALL cite (Black & Moran, 1982; Rosenberg, 1982; Landauer et al., 1983); and SHALL point to Practice 9 item 9 for how far the evidence goes. The Practice 9 Sources list SHALL give each of the three works item 9 rests on as its own entry ending with its DOI link.

#### Scenario: Item 9, the audit question and rule 5 state the check

- **WHEN** Practice 9 item 9, the audit question numbered 9 and the rule 5 item delivered by the hook are read
- **THEN** each asks for the name to be read against the names around it, in the plugin or in the skills directory for a skill outside any plugin, and flags names that read alike or fit several skills without forbidding any; item 9 also states the limits of its evidence, and rule 5 cites its sources and points to item 9

##### Example: item 9, the audit question and rule 5 flag names that read alike

| Text read | Expected |
| --------- | -------- |
| plugins/skill-best-practices/skills/skill-best-practices/SKILL.md, the section from "## Practice 9:" up to the next level-two heading, outside code fences | exactly one line starting "9. ", which starts with "9. **Check the name against the other names in its listing.**" and comes after the line starting "8. " |
| the block of item 9 (its line and the indented lines below it) | contains "next to the other skill names in its plugin", "for a skill outside any plugin, next to the other skills in the same skills directory", "near-synonym", "general enough to fit several", "prefer one that shows what sets this skill apart", "whole-plugin rename under item 5", "different arguments or syntax, or that have different effects", "does not split a skill or override the naming grammar", "post hoc", "on learning and cued choice" and "learn or match six to ten text-editor commands, not a model choose from a skill listing"; and, compared without regard to case, does not contain "do not choose" |
| the audit question line starting "9. " under "### When a skill isn't performing", outside code fences | contains "near-synonym of a neighbouring skill name", "in its plugin, or in its skills directory for a skill outside any plugin" and "general enough to fit several", and ends with "? (Practice 9)" |
| the rule 5 item taken from the hook's additionalContext for an Edit of /repo/skills/y/SKILL.md | contains "near-synonym", "general enough to fit several", "or in its skills directory for a skill outside any plugin", "(Black & Moran, 1982; Rosenberg, 1982; Landauer et al., 1983)" and "Practice 9 item 9" |

#### Scenario: Practice 9 lists the sources of item 9

- **WHEN** the Sources list of Practice 9 is read
- **THEN** each of the three works item 9 rests on has its own entry ending with its DOI link

##### Example: Practice 9 lists the sources for item 9

- **GIVEN** the section of plugins/skill-best-practices/skills/skill-best-practices/SKILL.md from "## Practice 9:" up to the next level-two heading
- **WHEN** the list under "**Sources**:" is read (the lines starting "- " that follow it, up to the first line that does not)
- **THEN** exactly one entry starts with "Black, J. B., & Moran, T. P. (1982)." and ends with "https://doi.org/10.1145/800049.801745"; exactly one starts with "Landauer, T. K., Galotti, K. M., & Hartwell, S. (1983)." and ends with "https://doi.org/10.1145/358150.358157"; and exactly one starts with "Rosenberg, J. (1982)." and ends with "https://doi.org/10.1145/800049.801746"
