## Problem

Verify round 4 on #40 (issuecomment-7101056492) passed with three remaining items:

- The Sources test takes the last token with `split()`, which also splits on tabs and non-breaking spaces, while the Example says space-separated.
- The application paragraph says Furnas et al. "kept" execution on the standard name. That was their proposal.
- Item 9's different-syntax sentence asks names to show the difference, which goes further than either study tested.

## Root Cause

Fix round 3 rewrote these sentences and the helper, and did not recheck the new wording against the Example and the sources.

## Proposed Solution

- Split on spaces only in `source_problems`, and add a non-breaking-space mutation.
- Write "proposed keeping".
- Rephrase the different-syntax sentence as a flag on names a reader could confuse, with a preference for a clearer name where the naming rules allow.

## Non-Goals

- No new claim about the sources.
- No version change.
- The #43 helpers are not touched.

## Success Criteria

- The updated tests fail on 5f26b5e and pass after the change.
- The plugin tests, `tests/test_practice_lists.py` and `tests/test_marketplace.py` pass.

## Impact

- Affected specs: skill-writing-reminder
- Affected code:
  - Modified: plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
