## 1. Tests for the spec Examples

- [x] 1.1 Add a test marked `spec-example: skill-writing-reminder / rule 5 names Practice 9 and its source` to plugins/skill-best-practices/tests/test_hooks.py, covering the requirement "The skill-writing reminder states the naming rule": an Edit of /repo/plugins/x/skills/y/SKILL.md gets additionalContext containing "Names identify, descriptions get found", "(Practice 9)", "(Furnas et al., 1987)" and "no name can be relied on to be guessed". Verified by running the test in a temporary worktree of the commit before dc301f6 (it fails there) and on the branch (it passes).
- [x] 1.2 Add a test marked `spec-example: skill-writing-reminder / a new skill in an existing plugin keeps the plugin's names`: a Write of /repo/skills/y/SKILL.md gets additionalContext containing "in a new plugin, or one renamed as a whole", "follows that plugin's current names, prefixed or not" and "renamed as a whole or not at all". Verified by running it at dc301f6, where the clause was missing (it fails), and on the branch (it passes).
- [x] 1.3 Add a test marked `spec-example: skill-writing-reminder / the five shapes and the word limit`: additionalContext contains each of the six table rows of that Example (short-to-product, short-[object-]verb, query or settings `short-noun`, orchestration `short-mode`, norms and personas `short-noun`, two content words as the target and three at most). Verified by running it before dc301f6 (fails) and on the branch (passes).
- [x] 1.4 Add a test marked `spec-example: skill-writing-reminder / a failed wording goes into the description`: additionalContext contains "lists the words users actually say for the job" and "a wording that once failed to reach the skill is added to the description". Verified by running it before dc301f6 (fails) and on the branch (passes).
- [x] 1.5 Add a test marked `spec-example: skill-writing-reminder / four places list Practice 9`, covering the requirement "The plugin lists Practice 9 with its other practices": SKILL.md has the heading "## Practice 9: Names Identify, Descriptions Get Found" and an audit question ending with "(Practice 9)", the plugin CLAUDE.md has the row for Practice 9 with Furnas, Landauer, Gomez, & Dumais (1987), and README.md says "Nine evidence-based practices". Verified by running it before dc301f6 (fails) and on the branch (passes).

## 2. Implementation (committed before the spec as dc301f6 and 3c5291f)

- [x] 2.1 Rule 5 of plugins/skill-best-practices/rules/skill-writing.md states the naming rule exactly as the requirement "The skill-writing reminder states the naming rule" describes, including the convention clause for existing plugins. Verified by tests 1.1 to 1.4 passing.
- [x] 2.2 The skill document has the Practice 9 section and audit question 9, the plugin CLAUDE.md has the Practice 9 research row, README.md and the root CLAUDE.md count nine practices, and plugin.json and marketplace.json say version 0.4.0. Verified by test 1.5 passing and `claude plugin validate` reporting no new error.

## 3. Source check

- [x] 3.1 Practice 9 reports its source faithfully: every number and quotation in the Practice 9 section is checked against the page images of Furnas et al. (1987), pages 964 to 971, and the renaming and no-piecemeal-renaming claims are attributed to PsychQuant/che-plugin-devtools#74 where they come from there. Verified by a claim-by-claim table (claim, cited page, passage transcribed from the page image) built by the implementer before archive, with every row matching; the verify run for PsychQuantAgent/claude-code-logos#36 re-checks the table.

## 4. Whole suite

- [x] 4.1 The plugin's test suite and the repository's catalogue tests pass after the change. Verified by `python3 -m unittest discover -s plugins/skill-best-practices/tests` and the repository root test run both reporting OK.
