## Problem

Verify round 1 of PsychQuantAgent/claude-code-logos#40 failed with two HIGH findings against Practice 9 item 9, added by change idd-40-practice-9-neighbour-names.
- **The different-inputs rule is too broad.** Item 9 says "jobs that take different inputs or have different effects get different names". That is broader than its source: Landauer et al. measured a benefit for different syntax (p. 501) and concluded about different constructions or effects (p. 503). Read literally, it conflicts with the conversion grammar.
- **The prohibitions outrun the evidence.** Item 9 states them as categorical ("do not choose"). The evidence is one post hoc analysis of 12 people, one condition without a full analysis, and a null vocabulary result.

The round also found MEDIUM gaps:
- The audit question has no comparison set for a skill outside any plugin.
- Item 9 drops Black & Moran's qualifier "on learning and cued choice".
- Practice 9 does not say that two 1984 papers were not read.
- Several sentences of the research paragraph are loose.
- The examples give no jobs.
- Rule 5 drops the limits of the evidence.
- The tests are weaker than the requirement.

## Root Cause

The first change carried the plan's wording over as a rule without checking each clause's strength against its page. Its Examples pinned a few phrases, not every clause the requirement names.

## Proposed Solution

- **Item 9 becomes a check.** Read the name against the plugin's other skill names, or the same skills directory for a skill outside any plugin. Flag a near-synonym of a neighbour, or a name general enough to fit several. Prefer a name that shows what sets the skill apart when one fits the plugin's naming convention. Record an overlap between existing names for a whole-plugin rename under item 5. Skills with different arguments, syntax or effects should not differ only by near-synonyms; the check does not split a skill or override the naming grammar. Item 9 states the limits of its evidence and forbids no name outright.
- **The research paragraph is rewritten against the pages** and says that the two *Human Factors* (1984) papers were not read. It records the measured results on remembering and typing, and that no rule is drawn from them.
- **Audit question 9 and rule 5** ask the same check with the same comparison set. Rule 5 cites all three works and points to item 9 for how far the evidence goes.
- **Tests.** The Examples pin every clause and count numbered item 9 entries outside code fences. Each source must have its own entry ending with its DOI link.

## Non-Goals

- Editing the archive of idd-40-practice-9-neighbour-names. Its proposal still says "learning" and states the remembering-and-typing conclusion more broadly. This change records the corrections instead.
- The fence handling of the existing audit_question_9 helper. That is pre-existing code and is filed as #43.
- A version bump. 0.5.0 has not been released.

## Success Criteria

- The rewritten test for the Example "item 9, the audit question and rule 5 flag names that read alike" fails on the text before this change and passes after it.
- The Sources test checks one entry per work, each ending with its DOI link.
- python3 -m pytest -q plugins/skill-best-practices/tests tests reports no failure. That includes the existing Practice 9 and rule 5 scope checks with their mutation tables.

## Impact

- Affected specs: skill-writing-reminder (modified)
- Affected code:
  - Modified: plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
  - Modified: plugins/skill-best-practices/rules/skill-writing.md
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
