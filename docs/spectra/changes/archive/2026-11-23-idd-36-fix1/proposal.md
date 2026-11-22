## Problem

Verify round 1 for PsychQuantAgent/claude-code-logos#36 found that rule 5 of plugins/skill-best-practices/rules/skill-writing.md contradicts its own exception: it says a new skill in an existing plugin keeps that plugin's names, then says every name takes the shape for its kind, and every shape begins with the plugin's short name. A skill outside any plugin, which has no short name, is given the same shapes. The spec that rule 5 implements did not say where the shapes apply, its trigger was worded as a path suffix, and its tests searched the whole reminder instead of rule 5. Verify also found Practice 9 wording that overstates its sources or its guarantees.

## Root Cause

Rule 5 and the Practice 9 "How to apply" list state the shapes as unconditional and then state the exception as a separate clause, so the two read as competing rules. The spec Examples checked phrases, not their scope, so the contradiction passed every test.

## Proposed Solution

- Rule 5 and Practice 9 state once where each naming rule applies: in a new plugin or one renamed as a whole, the short-name prefix and the shape for each kind; in an existing plugin, that plugin's current names; outside any plugin, no prefix. Rule 5 says it summarizes Practice 9 and points to it.
- Practice 9 wording: a prefix reduces collisions rather than guaranteeing a unique name; failed wordings join the description as short phrases with no private details; the research summary keeps the paper's conditions and qualifiers; audit question 9 asks for several phrasings and any wording that failed; the distinct-mode rule decided on #36 is added; the "I want to ___" test is stated by kind; matching a description does not authorize a skill's consequential steps; the built-in command replacement is limited as the documentation limits it; the Claude Code documentation and PsychQuant/plaud-mcp-connector#65 are cited.
- The spec states the trigger as a final path component exactly SKILL.md, delivered once per session, and splits the practice lists into the plugin's own files and the repository's files. Tests bind to the rule 5 item, to each kind and its shape, and to the located heading and audit question; the repository-level checks move to the repository tests.

## Non-Goals

- Which shape a conversion takes when it runs several steps, and how two conversions in one plugin with the same product are named: both are grammar questions for PsychQuant/che-plugin-devtools#74, not decided here.
- The reminder hook's session-marker directory and its marker-before-read order predate #36 and go to a follow-up issue; the hook script is not changed.
- The archived change idd-36-practice-9-skill-naming is left as it was archived.

## Success Criteria

- Rule 5 contains no sentence that applies the shapes to every skill; the shapes sit inside the clause for a new or wholly renamed plugin, followed by the existing-plugin and outside-plugin clauses. Verified by the Example "the shapes apply only in a new or wholly renamed plugin", which fails on 3581c1b.
- Every Example in the modified requirements has a tagged test, and both test suites pass.

## Impact

- Affected specs: skill-writing-reminder (modified)
- Affected code:
  - Modified: plugins/skill-best-practices/rules/skill-writing.md
  - Modified: plugins/skill-best-practices/skills/skill-best-practices/SKILL.md
  - Modified: plugins/skill-best-practices/tests/test_hooks.py
  - New: tests/test_practice_lists.py
