## 1. Tests (written first, run on 70aeb89)

- [x] 1.1 For the requirement "The skill-writing reminder states the naming rule", add a scope-check helper to plugins/skill-best-practices/tests/test_hooks.py and the tests marked `spec-example: skill-writing-reminder / the shapes apply only in a new or wholly renamed plugin` (the three parts as the Example gives) and `spec-example: skill-writing-reminder / an unconditional shape mandate fails the rule 5 scope check` (the helper reports a violation on the mutated item). Verified on the mutated rule 5 item: the fix1 scope test still passes on it (it did not catch the contradiction), while the new check reports a violation; both new tests pass on 70aeb89 and on the fixed tree for the unmutated item.
- [x] 1.2 Update the tests marked "a failed wording goes into the description" (both whole sentences) and "a second skill edit in the session gets no reminder" (a different SKILL.md path in the same session; rule 5 in the first and third outputs). Verified by running them on 70aeb89 (the failed-wording test fails: the sentences changed) and on the fixed tree (both pass).
- [x] 1.3 For the requirement "The plugin lists Practice 9 with its other practices", update the test marked "the plugin's own files list Practice 9" (audit line starts with "9. ", code fences tracked, research row as a table line) and add the tests marked `spec-example: skill-writing-reminder / Practice 9 states where its naming rules apply` and `spec-example: skill-writing-reminder / an unconditional shape mandate fails the Practice 9 scope check`. Verified by running them on 70aeb89 and on the fixed tree (pass on both: the text already had the scope paragraph), and by the mutation Example failing.
- [x] 1.4 Update tests/test_practice_lists.py for "the repository's files count nine practices": count with no digit before the 9, every numeric and Chinese count in CLAUDE.md, the README row as a table line. Verified by passing on 70aeb89 and on the fixed tree, and by failing on a scratch copy whose marketplace description says "19 practices".

- [x] 1.5 Widen the two scope checks as the updated Examples say (case-insensitive; prefix, short name and word limit outside the clause; more quantifiers; table rows as sentences; the region from the scope paragraph to item 5 exempt) and run every row of both mutation tables, each of which must be reported. Verified by the spectra-verify probes of 2026-11-23 being caught, and by the unmutated texts of 70aeb89 and HEAD passing.

## 2. Text

- [x] 2.1 Rule 5 of plugins/skill-best-practices/rules/skill-writing.md: the clause for a new or wholly renamed plugin says a name "starts with the plugin's short name"; a skill outside any plugin is checked against built-in commands and bundled skills; every description wording is a short phrase with no private details, and a failed wording is added in the same way. Verified by tests 1.1 and 1.2 passing.
- [x] 2.2 Practice 9 in the skill document: summary with "main" and "unfamiliar"; what a name carries by kind; the outside-plugin check against built-in commands; item 6 by kind; item 7 short phrases with no private details for every wording; audit question 9 with the privacy limit and the built-in check; example labelled as two drafts in a new plugin; experts and help-index proposal worded as the pages state; "Armchair" quoted as printed; frontmatter "Relevant requests include". Verified by test 1.3 and a reading against the round-2 report.

- [x] 2.3 The exception for a skill outside any plugin that is meant to replace a bundled skill or built-in command: "unless replacing one is the intent" in rule 5, the Practice 9 scope paragraph and audit question 9. Verified by the updated test "a new skill in an existing plugin keeps the plugin's names" failing before the change and passing after.

## 3. Source check

- [x] 3.2 Record on the source-check comment of PsychQuantAgent/claude-code-logos#36 the bundled-skill replacement claim and the date the documentation was read. Verified by the record listing it.
- [x] 3.1 For the requirement "Practice 9 reports its source faithfully", re-check the changed source sentences (experts on p. 966, the help-index proposal on p. 969, "Armchair" on p. 965) against the page images and record the rows on PsychQuantAgent/claude-code-logos#36. Verified by every changed row matching its page.

## 4. Whole suite

- [x] 4.1 Both suites pass: python3 -m pytest -q plugins/skill-best-practices/tests tests reports no failure.
