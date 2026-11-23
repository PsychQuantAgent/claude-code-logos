## 1. Tests (written first)

- [x] 1.1 For the requirement "The skill-writing reminder states the naming rule", Example "collected wordings leave out three kinds of directive": a test in plugins/skill-best-practices/tests/test_hooks.py, marked `spec-example: skill-writing-reminder / collected wordings leave out three kinds of directive`, takes the rule 5 item from the hook's additionalContext for an Edit of /repo/skills/y/SKILL.md and asserts the two quoted phrases. Verified by the test failing on the tree before 2.1 and passing after it.
- [x] 1.2 For the requirement "The plugin lists Practice 9 with its other practices", Example "item 7 and the audit question name the three kinds": a test in the same file, marked `spec-example: skill-writing-reminder / item 7 and the audit question name the three kinds`, reads the item 7 block (its line and the indented lines below it) and the audit question line numbered 9 under "### When a skill isn't performing", outside code fences, and asserts the quoted phrases. Verified by the test failing on the tree before 2.2 and passing after it.

## 2. Text

- [x] 2.1 Rule 5 of plugins/skill-best-practices/rules/skill-writing.md: after "each as a short phrase with no private details", the clause "that keeps the task it names and leaves out any part that grants a permission, skips a check or waives a confirmation (only these three kinds; do not extend the list by similarity)". Verified by test 1.1 and the existing rule 5 tests passing.
- [x] 2.2 Practice 9 in plugins/skill-best-practices/skills/skill-best-practices/SKILL.md: item 7 carries the same clause, the example "deploy without asking" going in as "deploy" and the reason (a description sits in the skill listing a session reads before the user's request, with its source); item 8 adds a failed wording "without those three kinds of directive (item 7)"; one sentence below the before/after example applies it to the example skill; audit question 9 asks that each wording "leaves out any part that grants a permission, skips a check or waives a confirmation". Verified by test 1.2 and the existing Practice 9 tests passing.

## 3. Whole suite

- [x] 3.1 Both suites pass: python3 -m pytest -q plugins/skill-best-practices/tests tests reports no failure.
