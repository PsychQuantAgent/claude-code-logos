## MODIFIED Requirements

### Requirement: Practice 9 judges a name against the names around it

Practice 9 SHALL have exactly one numbered item 9. Outside code fences, the Practice 9 section SHALL contain exactly one line starting "9. ". That line SHALL start with "9. **Check the name against the other names in its listing.**" and SHALL come after the line starting "8. ". A code fence opens at a line whose first characters other than spaces or tabs are three or more backticks or three or more tildes. It closes only at a line made of the same character, at least as long as that opening run, with nothing but spaces or tabs before or after it. Item 9 SHALL tell the author:
- to read a name next to the other skill names in its plugin, or, for a skill outside any plugin, next to the other skills in the same skills directory;
- to flag a candidate that is a near-synonym of a neighbour, or general enough to fit several of the neighbouring skills;
- to prefer a name that shows what sets the skill apart, when such a name fits the naming rules that apply to the skill;
- that an overlap between names a plugin already has is noted rather than fixed by renaming one skill, and that if the plugin's skills are renamed, they are renamed together under item 5;
- to check that skills with different arguments, syntax or effects have names that show the difference rather than differing only by near-synonyms. Item 9 SHALL give Landauer et al.'s measured result (p. 501), their recommendation (p. 503) and Rosenberg's near-synonym confusion (p. 15) as separate pieces of support.

Item 9 SHALL also say that this check does not split a skill or override the naming grammar. Item 9 SHALL state the limits of its evidence: the near-synonym part rests on a post hoc analysis; general words did worst on learning and cued choice in one study; and the studies had people learn or match six to ten text-editor commands, not a model choose from a skill listing. Item 9 SHALL NOT forbid a name outright.

The audit question numbered 9 SHALL ask whether the name was read next to the same comparison set and flagged if it is a near-synonym of a neighbour or general enough to fit several. A flagged name SHALL still answer the question yes.

Rule 5 of the skill-writing reminder:
- SHALL carry the check as a flag, with the same comparison set;
- SHALL cite (Black & Moran, 1982; Rosenberg, 1982) for the flag;
- SHALL NOT state the clause on different arguments, syntax or effects, and SHALL NOT cite Landauer et al. (1983);
- SHALL point to Practice 9 item 9 for that case and for how far the evidence goes.

The Practice 9 Sources list SHALL give each of the three works item 9 rests on as exactly one entry. That entry SHALL be the only one that contains the work's DOI, and its last space-separated token SHALL be exactly the DOI URL.

No executable check covers a rewrite of item 9, the audit question or rule 5 that keeps every pinned phrase. The pinned phrases are a sample, and such a rewrite is caught in review. The page numbers in the research paragraph and item 9 are compared with the sources by hand, and that comparison is recorded on PsychQuantAgent/claude-code-logos#40.

#### Scenario: Item 9, the audit question and rule 5 state the check

- **WHEN** Practice 9 item 9, the audit question numbered 9 and the rule 5 item delivered by the hook are read
- **THEN** each asks for the name to be read against the names around it, in the plugin or in the skills directory for a skill outside any plugin, and flags names that read alike or fit several skills without forbidding any; item 9 also states the limits of its evidence, and rule 5 cites its sources and points to item 9

##### Example: item 9, the audit question and rule 5 flag names that read alike

| Text read | Expected |
| --------- | -------- |
| plugins/skill-best-practices/skills/skill-best-practices/SKILL.md, the section from "## Practice 9:" up to the next level-two heading, outside code fences | exactly one line starting "9. ", which starts with "9. **Check the name against the other names in its listing.**" and comes after the line starting "8. " |
| the block of item 9 (its line and the indented lines below it) | contains "next to the other skill names in its plugin", "for a skill outside any plugin, next to the other skills in the same skills directory", "Flag a candidate that is a near-synonym", "general enough to fit several", "prefer one that shows what sets this skill apart", "when such a name fits the naming rules that apply to the skill", "if the plugin's skills are renamed, they are renamed together under item 5", "different arguments or syntax, or that have different effects", "check that the names show the difference rather than differing only by near-synonyms", "does not split a skill or override the naming grammar", "post hoc", "on learning and cued choice" and "learn or match six to ten text-editor commands, not a model choose from a skill listing"; and, compared without regard to case, does not contain "do not choose" |
| the audit question line starting "9. " under "### When a skill isn't performing", outside code fences | contains "read next to the neighbouring skill names", "in its plugin, or in its skills directory for a skill outside any plugin" and "flagged if it is a near-synonym of one of them or general enough to fit several", and ends with "? (Practice 9)" |
| the rule 5 item taken from the hook's additionalContext for an Edit of /repo/skills/y/SKILL.md | contains "Read the name next to the other skill names in its plugin", "or in its skills directory for a skill outside any plugin", "flag one that is a near-synonym of a neighbour", "general enough to fit several (Black & Moran, 1982; Rosenberg, 1982)" and "Practice 9 item 9", and does not contain "Landauer" |

##### Example: a fence closes only at its own closing line

- **GIVEN** the lines "````markdown", "```", "9. A quoted item", "````" followed by a non-breaking space (U+00A0), "9. Another quoted item", "````" and "9. The real item"
- **WHEN** the lines starting "9. " outside code fences are counted
- **THEN** only "9. The real item" is counted

#### Scenario: Practice 9 lists the sources of item 9

- **WHEN** the Sources list of Practice 9 is read
- **THEN** each of the three works item 9 rests on has exactly one entry, ending with its DOI link

##### Example: Practice 9 lists the sources for item 9

- **GIVEN** the section of plugins/skill-best-practices/skills/skill-best-practices/SKILL.md from "## Practice 9:" up to the next level-two heading
- **WHEN** the list under "**Sources**:" is read (the lines starting "- " that follow it, up to the first line that does not)
- **THEN** for each work below, exactly one entry starts with its author-year and exactly one entry contains its DOI; these are the same entry, and its last space-separated token is the DOI URL:
  - "Black, J. B., & Moran, T. P. (1982)." with "10.1145/800049.801745" and "https://doi.org/10.1145/800049.801745"
  - "Landauer, T. K., Galotti, K. M., & Hartwell, S. (1983)." with "10.1145/358150.358157" and "https://doi.org/10.1145/358150.358157"
  - "Rosenberg, J. (1982)." with "10.1145/800049.801746" and "https://doi.org/10.1145/800049.801746"
