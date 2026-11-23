## Problem

Verify round 3 on #40 (issuecomment-7100768803) passed with these remaining items:

- The fence counter treats a closing line followed by a non-breaking space as a closer, which the spec does not allow.
- The `idd-list`/`idd-manage` example fails items 2 and 6 before item 9 applies.
- The different-syntax sentence in item 9 is phrased as a separate "should not" rule that neither study establishes.
- The Sources test does not catch a duplicate entry without its DOI.
- One quotation has no page.
- "The two roles in the paper" no longer clearly refers to Furnas.
- Item 9's last clause claims more than Furnas.

## Root Cause

Fix rounds 1 and 2 changed the text around these sentences. Their wording was not rechecked against the items next to them or against the spec's fence rule.

## Proposed Solution

- Strip only spaces and tabs from a candidate closing fence.
- Keep one example (`idd-test` over `idd-check` next to `idd-verify`) and show both flags with it.
- Phrase the different-syntax sentence as a check.
- Count Sources entries by author-year as well as by DOI.
- Add (p. 10) to the quotation.
- Name Furnas et al. (1987) in the application paragraph.
- Use item 6's wording for the guessability limit.

## Non-Goals

- `practice_9_section` and `audit_question_9` remain tracked in #43.
- No new claim about the sources.
- No version change.

## Success Criteria

- The updated tests fail on 6870d33 and pass after the change.
- The plugin tests, `tests/test_practice_lists.py` and `tests/test_marketplace.py` pass.

## Impact

- Affected specs: skill-writing-reminder
- Affected code:
  - Modified: plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
