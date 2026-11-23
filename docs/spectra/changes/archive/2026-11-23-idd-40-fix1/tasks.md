## 1. Tests (written first)

- [x] 1.1 For the requirement "Practice 9 judges a name against the names around it", Example "item 9, the audit question and rule 5 flag names that read alike": rewrite the item 9 test in plugins/skill-best-practices/tests/test_hooks.py and mark it `spec-example: skill-writing-reminder / item 9, the audit question and rule 5 flag names that read alike`. It counts the lines starting "9. " in the Practice 9 section outside code fences and asserts every row of the Example's table. Verified by the test failing on the text before 2.1 and 2.2, and passing after them.
- [x] 1.2 For the same requirement, Example "Practice 9 lists the sources for item 9": rewrite the Sources test in the same file and keep its marker. It reads the list entries under "**Sources**:" and asserts one entry per work, starting with the work's author and year and ending with its DOI link. Verified by the test passing after 2.1, and by its failing when an entry's DOI link is removed in a scratch copy of the text.

## 2. Text

- [x] 2.1 Practice 9 in plugins/skill-best-practices/skills/skill-best-practices/SKILL.md:
  - Item 9 is rewritten as a check: it gives the comparison set, flags near-synonyms and general names, and prefers a name that shows the difference.
  - Item 9 uses `idd-test` rather than `idd-check` next to `idd-verify` as the example, and `idd-manage` as the general name.
  - Item 9 sends an overlap between existing names to a whole-plugin rename under item 5.
  - Item 9 says that skills with different arguments, syntax or effects should not differ only by near-synonyms, without splitting a skill or overriding the grammar, and states the limits of its evidence.
  - The research paragraph is rewritten against the pages, with one sentence saying that the two *Human Factors* (1984) papers were not read.
  - Audit question 9 asks the same check with the same comparison set.

  Verified by test 1.1 passing, and by the existing Practice 9 tests passing, including the scope check and its mutation table.
- [x] 2.2 Rule 5 of plugins/skill-best-practices/rules/skill-writing.md: the neighbour sentence becomes a flag with the same comparison set. It cites (Black & Moran, 1982; Rosenberg, 1982; Landauer et al., 1983) and says that Practice 9 item 9 gives how far that evidence goes. Verified by test 1.1 passing, and by the existing rule 5 tests passing, including the rule 5 scope check and its mutation table.

## 3. Source check

- [x] 3.1 For the requirement "Practice 9 reports its source faithfully": each claim in the rewritten research paragraph and item 9 is compared with the cited page, and the record is posted on PsychQuantAgent/claude-code-logos#40. Verified by that comment listing each changed claim with its page and the result.

## 4. Whole suite

- [x] 4.1 Both suites pass: python3 -m pytest -q plugins/skill-best-practices/tests tests reports no failure.
