## Problem

Verify round 2 for PsychQuantAgent/claude-code-logos#36 found that the tests added in idd-36-fix1 would not catch the round-1 contradiction if it came back: the scope test of rule 5 orders only the conversion shape and bans only one old sentence, and nothing checks the scope of the naming rules in the full Practice 9 text, which rule 5 tells the session to read. Several other tests match substrings that a wrong value also contains. The round also found that only failed wordings carry the privacy limit, that a skill outside any plugin is not checked against built-in commands, and that item 6 reads as an action test for every kind of skill.

## Root Cause

The fix1 Examples named example strings rather than the property they stand for (that the prefix and shapes live only inside the clause for a new or wholly renamed plugin), so the tests pinned strings and missed paraphrases of the same defect.

## Proposed Solution

- Rule 5 and Practice 9: a scope check that splits the text at its clauses and requires the prefix, every kind–shape pair and the word limit inside the new-or-renamed clause, and no shape or prefix mandate outside it; a Practice 9 check that the scope paragraph precedes items 1 to 4 and that no sentence about every skill or all skills mentions a shape or a prefix. Each check has a mutation Example that must fail.
- Tests checked whole: the description sentences with their subjects; a second, different SKILL.md in the same session; the practice count as a whole number everywhere it is stated; audit question 9 as the line numbered 9 outside code fences; research rows as table lines.
- Rule 5 and Practice 9 text: every description wording is a short phrase with no private details; a skill outside any plugin is checked against built-in commands and bundled skills; item 6 checks action and conversion names with "I want to ___" and other kinds by their mode or topic; the Practice 9 summary, example label, source wording and frontmatter lead-in follow the round-2 report.

## Non-Goals

- The hook script's path splitting and marker handling (PsychQuantAgent/claude-code-logos#37).
- The open grammar questions in PsychQuant/che-plugin-devtools#74.
- The capability Purpose, which a delta cannot change.

## Success Criteria

- On 70aeb89 the new scope tests fail on their mutation Examples or on the missing clauses; on the fixed tree every Example passes and both mutation Examples report a violation.
- Both test suites pass.

## Impact

- Affected specs: skill-writing-reminder (modified)
- Affected code:
  - Modified: plugins/skill-best-practices/rules/skill-writing.md
  - Modified: plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
  - Modified: tests/test_practice_lists.py
