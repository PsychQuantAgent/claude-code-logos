"""Tests for the skill-best-practices hook scripts.

Each test feeds a synthetic hook payload on stdin, the way Claude Code does,
and checks what the script prints. Run with:

    python3 -m unittest discover -s plugins/skill-best-practices/tests
"""
import json
import pathlib
import subprocess
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = PLUGIN / "scripts"


def run(script, payload, env=None):
    proc = subprocess.run(
        ["python3", str(SCRIPTS / script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
    )
    return proc.returncode, proc.stdout, proc.stderr


def bash_payload(command):
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }


class SearchTruncationReminder(unittest.TestCase):
    SCRIPT = "search_truncation_reminder.py"

    def reminder(self, command):
        code, out, err = run(self.SCRIPT, bash_payload(command))
        self.assertEqual(code, 0, err)
        if not out.strip():
            return None
        data = json.loads(out)
        hso = data["hookSpecificOutput"]
        self.assertEqual(hso["hookEventName"], "PreToolUse")
        # A reminder never decides the call: no permissionDecision of any kind.
        self.assertNotIn("permissionDecision", hso)
        return hso["additionalContext"]

    def test_grep_piped_to_head_gets_reminder(self):
        self.assertIn("evidence", self.reminder("grep -nE 'alpha|beta' notes.txt | head -12"))

    def test_rg_piped_to_head_without_count(self):
        self.assertIsNotNone(self.reminder("rg -n alpha src | head"))

    def test_grep_piped_to_tail(self):
        self.assertIsNotNone(self.reminder("grep -n alpha notes.txt | tail -n 5"))

    def test_grep_max_count_flag(self):
        self.assertIsNotNone(self.reminder("grep -m 3 alpha notes.txt"))
        self.assertIsNotNone(self.reminder("grep --max-count=3 alpha notes.txt"))

    def test_git_grep_piped_to_head(self):
        self.assertIsNotNone(self.reminder("git grep -n alpha origin/main | head -8"))

    def test_search_inside_longer_pipeline(self):
        self.assertIsNotNone(self.reminder("cat notes.txt | grep -v '^#' | grep -n alpha | cut -c1-80 | head -12"))

    def test_redirection_does_not_end_the_pipeline(self):
        self.assertIsNotNone(self.reminder("grep -rn alpha src 2>/dev/null | head -5"))
        self.assertIsNotNone(self.reminder("grep -rn alpha src 2>&1 | head -5"))

    def test_separate_commands_are_not_a_pipeline(self):
        self.assertIsNone(self.reminder("grep -n alpha notes.txt; head -3 other.txt"))
        self.assertIsNone(self.reminder("grep -q alpha notes.txt && tail -n 2 log.txt"))

    def test_untruncated_grep_is_silent(self):
        self.assertIsNone(self.reminder("grep -n alpha notes.txt"))

    def test_counting_is_silent(self):
        self.assertIsNone(self.reminder("grep -c alpha notes.txt"))
        self.assertIsNone(self.reminder("grep alpha notes.txt | wc -l"))

    def test_head_without_search_is_silent(self):
        self.assertIsNone(self.reminder("ls -la | head -5"))
        self.assertIsNone(self.reminder("git log --oneline | head -5"))
        self.assertIsNone(self.reminder("cat notes.txt | head -50"))

    def test_word_containing_grep_is_not_a_search(self):
        self.assertIsNone(self.reminder("echo regrep | head -1"))

    def test_non_bash_tool_is_silent(self):
        code, out, _ = run(self.SCRIPT, {"hook_event_name": "PreToolUse", "tool_name": "Read",
                                         "tool_input": {"file_path": "/tmp/x"}})
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "")

    def test_malformed_input_never_blocks(self):
        proc = subprocess.run(["python3", str(SCRIPTS / self.SCRIPT)], input="not json",
                              capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")


class SessionStartRule(unittest.TestCase):
    def test_injects_runtime_rule(self):
        code, out, err = run("session_start.py", {"hook_event_name": "SessionStart", "source": "startup"})
        self.assertEqual(code, 0, err)
        data = json.loads(out)
        hso = data["hookSpecificOutput"]
        self.assertEqual(hso["hookEventName"], "SessionStart")
        text = hso["additionalContext"]
        self.assertIn("Search locates, reading decides", text)
        self.assertIn("truncated", text)

    def context(self, source="startup"):
        code, out, err = run("session_start.py", {"hook_event_name": "SessionStart", "source": source})
        self.assertEqual(code, 0, err)
        return json.loads(out)["hookSpecificOutput"]["additionalContext"]

    def test_injects_practice_8_rule(self):
        text = self.context()
        self.assertIn("Ask only when the answer changes the next step", text)
        self.assertIn("Practice 8", text)

    def test_practice_8_keeps_irreversible_actions_confirmed(self):
        text = self.context()
        self.assertIn("Irreversible or private actions still need confirmation", text)
        self.assertIn("Do not ask again about an item the user approved", text)

    def test_practice_8_asks_in_one_message(self):
        self.assertIn("in one message, not over several turns", self.context())

    def test_practice_8_when_unsure_treat_as_irreversible(self):
        self.assertIn("When unsure, treat the action as irreversible", self.context())

    def test_practice_8_routine_records_are_a_closed_list(self):
        text = self.context()
        self.assertIn("only these four, never extended by similarity", text)
        self.assertIn("goes back to confirmation", text)
        self.assertIn("absolute paths on this machine", text)

    def test_practice_8_approval_covers_only_listed_items(self):
        text = self.context()
        self.assertIn("One approval covers only the items listed in the message it answers", text)
        self.assertIn("An earlier answer is never approval for an irreversible action it did not list", text)

    def test_practice_8_owner_complaints_are_pinned(self):
        # The three behaviours the issue reported: an issue in the user's own
        # repository was confirmed, an approved batch was re-asked, reports were long.
        text = self.context()
        self.assertIn("(1) creating an issue or a comment", text)
        self.assertIn("say so in one line", text)
        self.assertIn("Keep reports short", text)

    def test_practice_8_routine_records_need_the_users_request(self):
        text = self.context()
        self.assertIn("only for work the user asked for in this conversation", text)
        self.assertIn("is not a request", text)

    def test_practice_8_private_content_is_wide_and_paths_are_absolute(self):
        text = self.context()
        self.assertIn("credentials or tokens", text)
        self.assertIn("absolute paths on this machine", text)
        self.assertIn("when unsure whether content is private, ask", text)

    def test_practice_8_baseline_tag_only_on_the_remote_default_commit(self):
        self.assertIn("the commit the remote default branch already points to", self.context())

    def test_practice_8_named_instruction_and_reply_coverage(self):
        text = self.context()
        self.assertIn("names the action and its target is approval of that item", text)
        self.assertIn("covers every listed push", text)

    def test_practice_8_explicit_instructions_to_ask_still_apply(self):
        self.assertIn(
            "An explicit instruction from the user, their CLAUDE.md or a skill to ask, confirm or wait still applies",
            self.context(),
        )

    def test_both_rules_restored_after_compaction(self):
        text = self.context("compact")
        self.assertIn("Search locates, reading decides", text)
        self.assertIn("Ask only when the answer changes the next step", text)


RULE_5_START = "5. **Names identify, descriptions get found**"
NEW_PLUGIN_CLAUSE = "in a new plugin, or one renamed as a whole"
EXISTING_PLUGIN_CLAUSE = "a new skill in an existing plugin"
SHAPE_PAIRS = ("conversion `short-to-product`", "action `short-[object-]verb`",
               "query or settings `short-noun`", "orchestration `short-mode`",
               "norms and personas `short-noun`")
WORD_LIMIT = "two content words as the target and three at most"


def rule_5_scope_violations(item):
    """Ways rule 5 lets the prefix or the shapes escape the clause for a new or wholly renamed plugin."""
    start, end = item.find(NEW_PLUGIN_CLAUSE), item.find(EXISTING_PLUGIN_CLAUSE)
    if start < 0 or end < 0 or end < start:
        return ["the new-plugin and existing-plugin clauses are missing or out of order"]
    before, clause, after = item[:start], item[start:end], item[end:]
    problems = [f"the new-plugin clause lacks {need!r}"
                for need in ("starts with the plugin's short name", *SHAPE_PAIRS, WORD_LIMIT)
                if need not in clause]
    if "a skill outside any plugin is not given a prefix" not in after:
        problems.append("the clause for a skill outside any plugin is missing after the existing-plugin clause")
    for where, part in (("before", before), ("after", after)):
        problems += [f"{word!r} appears {where} the new-plugin clause" for word in ("shape", "`short-") if word in part]
    return problems


def practice_9_section(text):
    lines = text.splitlines()
    start = lines.index("## Practice 9: Names Identify, Descriptions Get Found")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end])


def practice_9_scope_violations(section):
    """Ways Practice 9 lets its naming rules apply beyond the plugins they are for."""
    problems = []
    scope = "Items 1 to 4 describe the names in a new plugin or in one renamed as a whole"
    first_item = "1. **Every skill name starts with the plugin's short name.**"
    i, j = section.find(scope), section.find(first_item)
    if i < 0 or j < 0 or j < i:
        problems.append("the scope statement is missing or does not come before item 1")
    else:
        paragraph = section[i:section.find("\n\n", i)]
        problems += [f"the scope paragraph lacks {need!r}" for need in
                     ("follows that plugin's current names", "is not given a prefix") if need not in paragraph]
    import re
    for sentence in re.split(r"(?<=[.!?:;])\s+", section):
        lowered = sentence.lower()
        if ("every skill" in lowered or "all skills" in lowered) and ("shape" in lowered or "prefix" in lowered):
            problems.append(f"a sentence applies a shape or prefix to every skill: {sentence.strip()[:80]!r}")
    return problems


def table_line_below_table_line(lines, row):
    """The row is a whole line, directly below another table line."""
    return row in lines and lines.index(row) > 0 and lines[lines.index(row) - 1].startswith("|")


class SkillWritingReminder(unittest.TestCase):
    SCRIPT = "skill_writing_reminder.py"

    def context(self, tool, path):
        code, out, err = run(self.SCRIPT, {"hook_event_name": "PreToolUse", "tool_name": tool,
                                           "tool_input": {"file_path": path}})
        self.assertEqual(code, 0, err)
        if not out.strip():
            return None
        hso = json.loads(out)["hookSpecificOutput"]
        self.assertNotIn("permissionDecision", hso)
        return hso["additionalContext"]

    def test_editing_a_skill_file_gets_the_rule(self):
        text = self.context("Edit", "/repo/plugins/x/skills/y/SKILL.md")
        self.assertIsNotNone(text)
        self.assertIn("Practice 7", text)

    def test_writing_a_skill_file_gets_the_rule(self):
        self.assertIsNotNone(self.context("Write", "/repo/skills/y/SKILL.md"))

    def test_windows_separators(self):
        self.assertIsNotNone(self.context("Edit", "C:\\repo\\skills\\y\\SKILL.md"))

    def test_other_files_are_silent(self):
        self.assertIsNone(self.context("Edit", "/repo/README.md"))
        self.assertIsNone(self.context("Edit", "/repo/skills/y/NOTSKILL.md"))

    # spec-example: skill-writing-reminder / a second skill edit in the session gets no reminder
    def test_injected_once_per_session(self):
        import os
        import tempfile

        def payload(tool, path, session):
            return {"hook_event_name": "PreToolUse", "tool_name": tool, "session_id": session,
                    "tool_input": {"file_path": path}}

        with tempfile.TemporaryDirectory() as tmp:
            env = {**os.environ, "TMPDIR": tmp}
            _, first, _ = run(self.SCRIPT, payload("Edit", "/repo/skills/y/SKILL.md", "s-1"), env)
            _, second, _ = run(self.SCRIPT, payload("Write", "/repo/skills/z/SKILL.md", "s-1"), env)
            _, other, _ = run(self.SCRIPT, payload("Edit", "/repo/skills/y/SKILL.md", "s-2"), env)
        self.assertEqual(second.strip(), "", "a different SKILL.md in the same session must get nothing")
        for out in (first, other):
            context = json.loads(out)["hookSpecificOutput"]["additionalContext"]
            self.assertTrue(any(l.startswith(RULE_5_START) for l in context.splitlines()))

    # spec-example: skill-writing-reminder / a path that only ends in SKILL.md gets no reminder
    def test_path_that_only_ends_in_skill_md_is_silent(self):
        self.assertIsNone(self.context("Edit", "/repo/skills/y/NOT-SKILL.md"))

    def rule_5(self, tool="Edit", path="/repo/skills/y/SKILL.md"):
        """The rule 5 item of the reminder, so assertions cannot be met by text elsewhere."""
        text = self.context(tool, path)
        self.assertIsNotNone(text)
        items = [line for line in text.splitlines() if line.startswith(RULE_5_START)]
        self.assertEqual(len(items), 1, "the reminder must hold exactly one rule 5 item")
        return items[0]

    # spec-example: skill-writing-reminder / rule 5 names Practice 9 and its source
    def test_rule_5_names_practice_9_and_its_source(self):
        item = self.rule_5("Edit", "/repo/plugins/x/skills/y/SKILL.md")
        for phrase in ("(Practice 9)", "(Furnas et al., 1987)", "no name can be relied on to be guessed",
                       "This item summarizes Practice 9", "read Practice 9 before choosing a name"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, item)

    # spec-example: skill-writing-reminder / a new skill in an existing plugin keeps the plugin's names
    def test_new_skill_in_existing_plugin_keeps_its_names(self):
        item = self.rule_5("Write", "/repo/skills/y/SKILL.md")
        for phrase in (NEW_PLUGIN_CLAUSE, "follows that plugin's current names, prefixed or not",
                       "renamed as a whole or not at all"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, item)

    # spec-example: skill-writing-reminder / the shapes apply only in a new or wholly renamed plugin
    def test_shapes_apply_only_in_new_or_wholly_renamed_plugin(self):
        self.assertEqual(rule_5_scope_violations(self.rule_5()), [])

    # spec-example: skill-writing-reminder / an unconditional shape mandate fails the rule 5 scope check
    def test_unconditional_shape_mandate_fails_the_rule_5_scope_check(self):
        mutated = self.rule_5() + " All skills must use these shapes."
        self.assertNotEqual(rule_5_scope_violations(mutated), [])

    # spec-example: skill-writing-reminder / the five shapes and the word limit
    def test_five_shapes_and_the_word_limit(self):
        item = self.rule_5()
        for row in (*SHAPE_PAIRS, WORD_LIMIT):
            with self.subTest(row=row):
                self.assertIn(row, item)

    # spec-example: skill-writing-reminder / a failed wording goes into the description
    def test_failed_wording_goes_into_the_description(self):
        item = self.rule_5()
        self.assertIn("The description lists the words users actually say for the job, several phrasings and not one, "
                      "each as a short phrase with no private details", item)
        self.assertIn("a wording that once failed to reach the skill is added to the description in the same way", item)


class PracticeLists(unittest.TestCase):
    SKILL = PLUGIN / "skills" / "skill-best-practices" / "SKILL.md"

    # spec-example: skill-writing-reminder / the plugin's own files list Practice 9
    def test_plugins_own_files_list_practice_9(self):
        lines = self.SKILL.read_text(encoding="utf-8").splitlines()
        self.assertIn("## Practice 9: Names Identify, Descriptions Get Found", lines)
        start = lines.index("### When a skill isn't performing")
        audit, in_fence = [], False
        for line in lines[start + 1:]:
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if line.lstrip().startswith("#"):
                break
            if line.startswith("9. ") and line.rstrip().endswith("? (Practice 9)"):
                audit.append(line)
        self.assertEqual(len(audit), 1, "the question numbered 9 must end with '? (Practice 9)'")
        research = (PLUGIN / "CLAUDE.md").read_text(encoding="utf-8").splitlines()
        self.assertTrue(table_line_below_table_line(
            research, "| 9 | Names identify, descriptions get found | Furnas, Landauer, Gomez, & Dumais (1987) |"))

    # spec-example: skill-writing-reminder / Practice 9 states where its naming rules apply
    def test_practice_9_states_where_its_naming_rules_apply(self):
        section = practice_9_section(self.SKILL.read_text(encoding="utf-8"))
        self.assertEqual(practice_9_scope_violations(section), [])

    # spec-example: skill-writing-reminder / an unconditional shape mandate fails the Practice 9 scope check
    def test_unconditional_shape_mandate_fails_the_practice_9_scope_check(self):
        section = practice_9_section(self.SKILL.read_text(encoding="utf-8"))
        table_end = "| Norms and personas (loaded as guidance) | `short-noun` | `axiom-statistics` (illustrative) |"
        self.assertIn(table_end, section)
        mutated = section.replace(table_end, table_end + "\n\nUse the five shapes for every skill.")
        self.assertNotEqual(practice_9_scope_violations(mutated), [])


class HooksManifest(unittest.TestCase):
    def test_hooks_json_wires_all_three_scripts(self):
        hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text())["hooks"]
        commands = json.dumps(hooks)
        for name in ("session_start.py", "search_truncation_reminder.py", "skill_writing_reminder.py"):
            self.assertIn(name, commands)
        matchers = {m["matcher"] for m in hooks["PreToolUse"]}
        self.assertIn("Bash", matchers)
        self.assertTrue(any("Write" in m and "Edit" in m for m in matchers))


if __name__ == "__main__":
    unittest.main()
