## 1. Tests matched to their Examples (written first)

- [x] 1.1 For the requirement "The skill-writing reminder states the naming rule": a module-level extractor in plugins/skill-best-practices/tests/test_hooks.py returns the whole rule 5 list item (its line and every following blank or indented line); the rule 5 tests use it; the mutation test adds the continuation row by inserting an indented line into the reminder text and extracting the item again; the Example phrases "by people unfamiliar with it" and the full standalone-skill clause are asserted. Verified by the fix2 extraction missing the continuation mutation (its one-line item passes the scope check) and the fix3 extraction reporting it, with all rule 5 tests passing on the unmodified text.
- [x] 1.2 For the requirement "The plugin lists Practice 9 with its other practices": the Practice 9 scope check skips only the scope paragraph and the blocks of items 1 to 4, joins the lines of a paragraph and ends sentences at ". ", "! " or "? "; the mutation test places each row at the position its table gives; the audit-question scan treats ``` and ~~~ as fences. Verified by the fix2 check missing the before-item-1 and below-table placements and the fix3 check reporting all seven rows, with the unmodified text passing.

## 2. Text

- [x] 2.1 Practice 9 in the skill document: "Items 6 to 8 apply to every skill" placed directly before item 6; the "After" routing sentence tied to a Plaud recording; item 6 asks an action name for its action and for an object that is named or clear from the plugin, and the application sentence on what a name carries says the same; the plaud case described as a failed guess plus description wording about the mechanism; the expert results stated without a blanket lead and the decoder called hypothetical (pp. 965–966); runtime delivery says later SKILL.md edits in the session get nothing once the session marker is written. Verified by test 1.2 passing and a reading against the round-3 report.

## 3. Source check

- [x] 3.1 For the requirement "Practice 9 reports its source faithfully", re-check "hypothetical" (p. 965) and the expert sentence (p. 966) against the page images and record the rows on PsychQuantAgent/claude-code-logos#36. Verified by both rows matching their pages.

## 4. Whole suite

- [x] 4.1 Both suites pass: python3 -m pytest -q plugins/skill-best-practices/tests tests reports no failure.
