## 1. Tests first

- [ ] 1.1 In plugins/skill-best-practices/tests/test_hooks.py, replace item 9's pinned phrase with "flag names that a reader could confuse with each other". The test for the Example "item 9, the audit question and rule 5 flag names that read alike" must fail on 5f26b5e.
- [ ] 1.2 Add a mutation subtest to the test for the Example "Practice 9 lists the sources for item 9" that puts a non-breaking space (U+00A0) before a DOI URL. It must fail with the `split()` helper of 5f26b5e.

## 2. Text and helper

- [ ] 2.1 In plugins/skill-best-practices/skills/skill-best-practices/SKILL.md, rewrite item 9's different-syntax sentence as in the fix-round-4 plan on #40, and change "Furnas et al. kept execution" to "Furnas et al. proposed keeping execution". Verified by test 1.1.
- [ ] 2.2 Make `source_problems` take the last token by splitting on spaces only. Verified by test 1.2.

## 3. Checks

- [ ] 3.1 Run python3 -m pytest -q plugins/skill-best-practices/tests tests and spectra validate idd-40-fix4; both pass.
