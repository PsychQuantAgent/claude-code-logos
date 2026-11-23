## 1. Tests first

- [ ] 1.1 Update the test for the Example "item 9, the audit question and rule 5 flag names that read alike" in plugins/skill-best-practices/tests/test_hooks.py to the Example's new phrases. These include rule 5 not containing "Landauer". The test must fail on 3b46ac3, because the audit, item 9 and rule 5 phrases are missing there.
- [ ] 1.2 Add a test for the Example "a shorter fence line does not close a longer fence", calling `numbered_lines_outside_fences` on the Example's six lines. The test must fail with the old helper, which counts both lines.
- [ ] 1.3 Update the test for the Example "Practice 9 lists the sources for item 9" to count the entries that contain each DOI and to compare each entry's last token with the DOI URL exactly. It must fail when an entry's URL only ends with the DOI URL, checked by a subtest that edits a copy of the list.

## 2. Text and helper

- [ ] 2.1 In plugins/skill-best-practices/skills/skill-best-practices/SKILL.md, reword the last clause of audit question 9. Make four edits to item 9: the naming rules that apply, the `idd-list` example, the conditional item 5 sentence, and the separated support for the different-syntax sentence. Make three edits to the research paragraph: Landauer's conclusion quoted as theirs, Rosenberg's two tasks, and pp. 9–10 for free recall. The wording follows the fix-round-2 plan on #40. Verified by test 1.1.
- [ ] 2.2 In plugins/skill-best-practices/rules/skill-writing.md, remove the different-syntax clause and its Landauer citation from rule 5, and point to Practice 9 item 9 for that case. Verified by test 1.1.
- [ ] 2.3 Make `numbered_lines_outside_fences` track the opening fence's character and length, closing only at a line of that character, at least as long, with nothing after it but spaces. Verified by test 1.2, and test 1.1 still passes.

## 3. Checks

- [ ] 3.1 Compare each changed citation with the page images (Black & Moran pp. 9–10; Landauer et al. pp. 501, 503; Rosenberg pp. 13–15) and post the rows on #40.
- [ ] 3.2 Run python3 -m pytest -q plugins/skill-best-practices/tests tests and spectra validate idd-40-fix2; both pass.
