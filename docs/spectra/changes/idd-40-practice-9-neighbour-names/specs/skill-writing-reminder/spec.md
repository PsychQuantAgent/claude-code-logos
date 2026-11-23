## ADDED Requirements

### Requirement: Practice 9 judges a name against the names around it

Practice 9 SHALL have exactly one item 9, a line starting "9. **Check the name against the other names in its listing.**", placed after item 8. Item 9 SHALL tell the author to read a name next to the other skill names in its plugin, or, for a skill outside any plugin, next to the other skills in the same skills directory; not to choose a near-synonym of a name already there; not to choose a word general enough to fit several of those skills; and to give jobs that take different inputs or have different effects different names. Item 9 SHALL say that the studies behind it had people learn six to ten text-editor commands, not a model choose from a skill listing, and that its near-synonym part rests on a post hoc analysis. The audit question numbered 9 SHALL ask whether the name is a near-synonym of another skill name in its plugin or general enough to fit several of them. Rule 5 of the skill-writing reminder SHALL carry the same check with its sources (Rosenberg, 1982; Landauer et al., 1983). The Practice 9 Sources list SHALL give the three works item 9 rests on with their DOIs.

#### Scenario: Item 9, the audit question and rule 5 state the check

- **WHEN** Practice 9 item 9, the audit question numbered 9 and the rule 5 item delivered by the hook are read
- **THEN** each asks for the name to be read against the other names in its plugin, item 9 states what its sources studied and that the near-synonym part is post hoc, and rule 5 names its sources

##### Example: item 9, the audit question and rule 5 judge a name against its neighbours

| Text read | Expected |
| --------- | -------- |
| plugins/skill-best-practices/skills/skill-best-practices/SKILL.md, the section from "## Practice 9:" up to the next level-two heading | exactly one line starting "9. **Check the name against the other names in its listing.**", after the line starting "8. " |
| the block of item 9 (its line and the indented lines below it) | contains "next to the other skill names in its plugin", "near-synonym", "general enough to fit several", "different inputs or have different effects", "text-editor commands" and "post hoc" |
| the audit question line starting "9. " under "### When a skill isn't performing", outside code fences | contains "near-synonym of another skill name in its plugin" and ends with "? (Practice 9)" |
| the rule 5 item taken from the hook's additionalContext for an Edit of /repo/skills/y/SKILL.md | contains "near-synonym", "general enough to fit several" and "(Rosenberg, 1982; Landauer et al., 1983)" |

#### Scenario: Practice 9 lists the sources of item 9

- **WHEN** the Sources list of Practice 9 is read
- **THEN** it gives the three works item 9 rests on with their DOIs

##### Example: Practice 9 lists the sources for item 9

- **GIVEN** the section of plugins/skill-best-practices/skills/skill-best-practices/SKILL.md from "## Practice 9:" up to the next level-two heading
- **WHEN** the lines after "**Sources**:" are read
- **THEN** they contain "https://doi.org/10.1145/800049.801745", "https://doi.org/10.1145/358150.358157" and "https://doi.org/10.1145/800049.801746"

## MODIFIED Requirements

### Requirement: Practice 9 reports its source faithfully

Every number, quotation and finding that the Practice 9 section of the skill document attributes to Furnas et al. (1987), Black and Moran (1982), Landauer, Galotti and Hartwell (1983) or Rosenberg (1982) SHALL be stated on the page it cites, together with the conditions and qualifiers the page attaches to it, and a claim that a paper does not make SHALL NOT be attributed to it. Claims drawn from elsewhere (the naming grammar and the no-piecemeal-renaming rule from PsychQuant/che-plugin-devtools#74, the "I want to ___" test from PsychQuant/che-plugin-devtools#28, the Claude Code behaviour from its documentation, the observed case from PsychQuant/plaud-mcp-connector#65) SHALL name their own source.

#### Scenario: A claim is compared with its cited page

- **WHEN** a Practice 9 claim attributed to one of these four papers is compared with the cited page
- **THEN** the page states the claim with no condition or qualifier dropped, and claims from elsewhere name their own source

No executable check: the papers' full texts are copyrighted and kept outside the repository, so the comparison with their page images is done by hand; the record of each comparison is the source-check comment on PsychQuantAgent/claude-code-logos#36 for Furnas et al. (1987) and on PsychQuantAgent/claude-code-logos#40 for the other three.
