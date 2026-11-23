## 1. Tests (written first)

- [ ] 1.1 For the requirement "Practice 9 judges a name against the names around it", Example "item 9, the audit question and rule 5 judge a name against its neighbours": a test in plugins/skill-best-practices/tests/test_hooks.py, marked `spec-example: skill-writing-reminder / item 9, the audit question and rule 5 judge a name against its neighbours`. It reads the Practice 9 section, the item 9 block, the audit question line numbered 9 (outside code fences) and the rule 5 item that the hook adds for an Edit of /repo/skills/y/SKILL.md, and asserts each row of the Example's table. Verified by the test failing on the tree before 2.1 and 2.2, and passing after them.
- [ ] 1.2 For the same requirement, Example "Practice 9 lists the sources for item 9": a test in the same file, marked `spec-example: skill-writing-reminder / Practice 9 lists the sources for item 9`. It reads the lines after "**Sources**:" in the Practice 9 section and asserts the three DOI links. Verified by the test failing on the tree before 2.1 and passing after it.

## 2. Text

- [ ] 2.1 Practice 9 in plugins/skill-best-practices/skills/skill-best-practices/SKILL.md:
  - a paragraph headed "**Research on names within a set**" after the Furnas paragraph, with the findings of Black and Moran (1982, pp. 9–10), Landauer, Galotti and Hartwell (1983, pp. 497–503) and Rosenberg (1982, pp. 12–15), each with its page and qualifiers, and one sentence recording that they add nothing on remembering or typing a name beyond item 4;
  - "Items 6 to 8" changed to "Items 6 to 9";
  - after item 8, the lead-in line "The name is also judged against the names around it:" and item 9 as approved in the #40 Implementation Plan;
  - in audit question 9, before "? (Practice 9)", the clause ", and is the name neither a near-synonym of another skill name in its plugin nor general enough to fit several of them";
  - the three works added to the Sources list in APA 7, with their DOI links.

  Verified by tests 1.1 and 1.2 passing, and by the existing Practice 9 tests passing, including the scope check and its mutation table.
- [ ] 2.2 Rule 5 of plugins/skill-best-practices/rules/skill-writing.md: after the sentence ending "(Furnas et al., 1987).", the sentence "Read the name next to the other skill names in its plugin: not a near-synonym of one of them, not general enough to fit several, and jobs with different inputs or effects get different names (Rosenberg, 1982; Landauer et al., 1983)." Verified by test 1.1 passing, and by the existing rule 5 tests passing, including the rule 5 scope check and its mutation table.
- [ ] 2.3 The version of skill-best-practices changed from 0.4.1 to 0.5.0, in plugins/skill-best-practices/.claude-plugin/plugin.json and in the skill-best-practices entry of .claude-plugin/marketplace.json. Verified by tests/test_marketplace.py passing; its version-match check compares the two.

## 3. Source check

- [ ] 3.1 For the requirement "Practice 9 reports its source faithfully": each number, quotation and finding that the new paragraph and item 9 attribute to the three works is compared by hand with the cited page images, and the record of the comparison is posted on PsychQuantAgent/claude-code-logos#40. Verified by that comment listing each claim with its page and the result of the comparison.

## 4. Whole suite

- [ ] 4.1 Both suites pass: python3 -m pytest -q plugins/skill-best-practices/tests tests reports no failure.
