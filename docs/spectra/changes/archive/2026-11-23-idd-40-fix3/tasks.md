## 1. Tests first

- [x] 1.1 In plugins/skill-best-practices/tests/test_hooks.py, add "check that the names show the difference rather than differing only by near-synonyms" to item 9's phrase list. The test for the Example "item 9, the audit question and rule 5 flag names that read alike" must fail on 6870d33.
- [x] 1.2 Rename the fence test to the Example "a fence closes only at its own closing line" and use that Example's seven lines. It must fail with the helper on 6870d33, which counts "9. Another quoted item" instead of "9. The real item".
- [x] 1.3 Make `source_problems` also require exactly one entry starting with each work's author-year. Add a mutation subtest that copies an entry without its DOI. That mutation must pass the DOI-only check on 6870d33 and fail the new check.

## 2. Text and helper

- [x] 2.1 In plugins/skill-best-practices/skills/skill-best-practices/SKILL.md, make the item 9 edits: the single `idd-check` example, the different-syntax check, and item 6's wording on guessing. Add (p. 10) after "do not report a full analysis", and change "the two roles in the paper" to "the two roles in Furnas et al. (1987)". Verified by test 1.1.
- [x] 2.2 Make `numbered_lines_outside_fences` strip only spaces and tabs from a candidate closing line. Verified by test 1.2.

## 3. Checks

- [x] 3.1 Run python3 -m pytest -q plugins/skill-best-practices/tests tests and spectra validate idd-40-fix3; both pass.
