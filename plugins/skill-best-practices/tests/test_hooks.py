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
DIRECTIVE_CLAUSE = ("keeps the task it names and leaves out any part that grants a permission, "
                    "skips a check or waives a confirmation")
DIRECTIVE_CLOSED_LIST = "only these three kinds; do not extend the list by similarity"
AUDIT_DIRECTIVE_CLAUSE = "leaves out any part that grants a permission, skips a check or waives a confirmation"
ITEM_9_START = "9. **Check the name against the other names in its listing.**"
ITEM_9_PHRASES = ("next to the other skill names in its plugin",
                  "for a skill outside any plugin, next to the other skills in the same skills directory",
                  "Flag a candidate that is a near-synonym", "general enough to fit several",
                  "prefer one that shows what sets this skill apart",
                  "when such a name fits the naming rules that apply to the skill",
                  "if the plugin's skills are renamed, they are renamed together under item 5",
                  "different arguments or syntax, or that have different effects",
                  "check that the names show the difference rather than differing only by near-synonyms",
                  "does not split a skill or override the naming grammar", "post hoc", "on learning and cued choice",
                  "learn or match six to ten text-editor commands, not a model choose from a skill listing")
AUDIT_NEIGHBOUR_PHRASES = ("read next to the neighbouring skill names",
                           "in its plugin, or in its skills directory for a skill outside any plugin",
                           "flagged if it is a near-synonym of one of them or general enough to fit several")
RULE_5_NEIGHBOUR_PHRASES = ("Read the name next to the other skill names in its plugin",
                            "or in its skills directory for a skill outside any plugin",
                            "flag one that is a near-synonym of a neighbour",
                            "general enough to fit several (Black & Moran, 1982; Rosenberg, 1982)",
                            "Practice 9 item 9")
ITEM_9_SOURCES = (("Black, J. B., & Moran, T. P. (1982).", "10.1145/800049.801745"),
                  ("Landauer, T. K., Galotti, K. M., & Hartwell, S. (1983).", "10.1145/358150.358157"),
                  ("Rosenberg, J. (1982).", "10.1145/800049.801746"))


def source_problems(entries):
    """What the Sources list gets wrong for item 9's works: for each DOI, exactly one entry contains it,
    that entry starts with the work's author-year, and its last space-separated token is exactly the DOI URL."""
    problems = []
    for start, doi in ITEM_9_SOURCES:
        starting = [e for e in entries if e.startswith(start)]
        if len(starting) != 1:
            problems.append(f"{start!r}: {len(starting)} entries start with it")
        holding = [e for e in entries if doi in e]
        if len(holding) != 1:
            problems.append(f"{doi}: {len(holding)} entries contain it")
            continue
        if not holding[0].startswith(start):
            problems.append(f"{doi}: the entry does not start with {start!r}")
        if holding[0].split()[-1] != f"https://doi.org/{doi}":
            problems.append(f"{doi}: the last token is not https://doi.org/{doi}")
    return problems


def numbered_lines_outside_fences(lines, number):
    """Indexes of the lines starting "<number>. " outside code fences. A fence opens at a run of three or more
    backticks or tildes; it closes only at a line made of the same character, at least as long as that run,
    with nothing but spaces or tabs after it."""
    found, fence = [], None
    for i, line in enumerate(lines):
        if fence is not None:
            run = line.strip()
            if run and set(run) == {fence[0]} and len(run) >= len(fence):
                fence = None
            continue
        lead = line.lstrip()
        mark = lead[:1]
        if mark in ("`", "~") and len(lead) - len(lead.lstrip(mark)) >= 3:
            fence = mark * (len(lead) - len(lead.lstrip(mark)))
            continue
        if line.startswith(f"{number}. "):
            found.append(i)
    return found


def sources_entries(section_lines):
    """The list under "**Sources**:": the lines starting "- " that follow it, up to the first line that does not."""
    entries = []
    for line in section_lines[section_lines.index("**Sources**:") + 1:]:
        if not line.startswith("- "):
            break
        entries.append(line[2:].rstrip())
    return entries


def rule_5_item(text):
    """The whole rule 5 list item as the hook delivers it: its line and every following blank or indented line."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith(RULE_5_START)]
    assert len(starts) == 1, "the reminder must hold exactly one rule 5 item"
    end = starts[0] + 1
    while end < len(lines) and (lines[end] == "" or lines[end][:1] in (" ", "\t")):
        end += 1
    return "\n".join(lines[starts[0]:end]).rstrip()


def rule_5_scope_violations(item):
    """Ways rule 5 lets the prefix, the shapes or the word limit escape the new-plugin clause.

    A keyword check: it catches the mandates in the spec's mutation table and close
    paraphrases of them, not every possible wording. Review covers the rest.
    """
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
        text = part.lower()
        for allowed in ("prefixed or not", "is not given a prefix"):
            text = text.replace(allowed, "")
        problems += [f"{word!r} appears {where} the new-plugin clause"
                     for word in ("shape", "`short-", "short name", "content words", "prefix") if word in text]
    return problems


def practice_9_section(text):
    lines = text.splitlines()
    start = lines.index("## Practice 9: Names Identify, Descriptions Get Found")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end])


PRACTICE_9_SCOPE = "Items 1 to 4 describe the names in a new plugin or in one renamed as a whole"
PRACTICE_9_ITEM_1 = "1. **Every skill name starts with the plugin's short name.**"
PRACTICE_9_ITEM_5 = "5. **Existing names are not renamed piecemeal.**"
QUANTIFIERS = ("every skill", "each skill", "any skill", "all skills", "skill names",
               "every name", "each name", "all names")
MANDATE_WORDS = ("shape", "prefix", "short name", "`short-")


def _block_end(lines, start):
    """Index after the item starting at `start`: its line plus following blank or indented lines."""
    end = start + 1
    while end < len(lines) and (lines[end] == "" or lines[end][:1] in (" ", "\t")):
        end += 1
    return end


def practice_9_scope_violations(section):
    """Ways Practice 9 lets its naming rules apply beyond the plugins they are for.

    Only the scope paragraph and the blocks of items 1 to 4 (each item's line and the
    indented lines below it) are skipped. Elsewhere, the lines of a paragraph are joined
    and split into sentences at ". ", "! " or "? ", and each table row is one sentence;
    a sentence that speaks of every, each, any or all skills or names may not mention a
    shape, a prefix or the short name. A keyword check: the spec's mutation table is a
    sample of edits it reports, and review covers rewordings outside it.
    """
    import re
    lines = section.splitlines()
    scope = next((i for i, l in enumerate(lines) if PRACTICE_9_SCOPE in l), None)
    item_1 = next((i for i, l in enumerate(lines) if l.startswith(PRACTICE_9_ITEM_1)), None)
    if scope is None or item_1 is None or not scope < item_1:
        return ["the scope statement is missing or does not come before item 1"]
    first = scope
    while first > 0 and lines[first - 1].strip():
        first -= 1
    last = scope
    while last + 1 < len(lines) and lines[last + 1].strip():
        last += 1
    paragraph = " ".join(lines[first:last + 1])
    problems = [f"the scope paragraph lacks {need!r}" for need in
                ("follows that plugin's current names", "is not given a prefix") if need not in paragraph]
    skipped = set(range(first, last + 1))
    for i, line in enumerate(lines):
        if re.match(r"[1-4]\. ", line):
            skipped.update(range(i, _block_end(lines, i)))
    units, prose = [], []
    for i, line in enumerate(lines + [""]):
        text = "" if i in skipped else line.strip()
        if text.startswith("|"):
            units.append(text)
            text = ""
        if text:
            prose.append(text)
        elif prose:
            units += re.split(r"(?<=[.!?])\s+", " ".join(prose))
            prose = []
    for unit in units:
        lowered = unit.lower()
        if any(q in lowered for q in QUANTIFIERS) and any(w in lowered for w in MANDATE_WORDS):
            problems.append(f"a sentence applies a naming rule to every skill: {unit[:80]!r}")
    return problems


def audit_question_9(lines):
    """The audit line numbered 9 under "### When a skill isn't performing", outside code fences."""
    start = lines.index("### When a skill isn't performing")
    found, in_fence = [], False
    for line in lines[start + 1:]:
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.lstrip().startswith("#"):
            break
        if line.startswith("9. "):
            found.append(line)
    return found


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
            code, second, err = run(self.SCRIPT, payload("Write", "/repo/skills/z/SKILL.md", "s-1"), env)
            _, other, _ = run(self.SCRIPT, payload("Edit", "/repo/skills/y/SKILL.md", "s-2"), env)
        self.assertEqual(code, 0, err)
        self.assertEqual(second, "", "a different SKILL.md in the same session must print nothing")
        expected = rule_5_item((PLUGIN / "rules" / "skill-writing.md").read_text(encoding="utf-8"))
        for out in (first, other):
            context = json.loads(out)["hookSpecificOutput"]["additionalContext"]
            self.assertEqual(rule_5_item(context), expected)

    def _two_edits(self, tmp):
        """Run two Edits of one SKILL.md with session s-1 under TMPDIR=tmp; return both outputs."""
        import os
        env = {**os.environ, "TMPDIR": tmp}
        payload = {"hook_event_name": "PreToolUse", "tool_name": "Edit", "session_id": "s-1",
                   "tool_input": {"file_path": "/repo/skills/y/SKILL.md"}}
        outs = []
        for _ in range(2):
            code, out, err = run(self.SCRIPT, payload, env)
            self.assertEqual(code, 0, err)
            outs.append(out)
        return outs

    def _has_rule_5(self, out):
        self.assertTrue(out.strip(), "expected the reminder")
        context = json.loads(out)["hookSpecificOutput"]["additionalContext"]
        expected = rule_5_item((PLUGIN / "rules" / "skill-writing.md").read_text(encoding="utf-8"))
        self.assertEqual(rule_5_item(context), expected)

    @staticmethod
    def _marker_dir_name():
        import os
        return f"skill-best-practices-{os.getuid()}"

    # spec-example: skill-writing-reminder / a symlinked marker directory is refused
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_symlinked_marker_directory_is_refused(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp = os.path.realpath(tmp)
            elsewhere = os.path.join(tmp, "elsewhere")
            os.mkdir(elsewhere)
            os.symlink(elsewhere, os.path.join(tmp, self._marker_dir_name()))
            for out in self._two_edits(tmp):
                self._has_rule_5(out)
            self.assertEqual(os.listdir(elsewhere), [])

    # spec-example: skill-writing-reminder / a marker directory open to others is refused
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_marker_directory_open_to_others_is_refused(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp = os.path.realpath(tmp)
            marker_dir = os.path.join(tmp, self._marker_dir_name())
            os.mkdir(marker_dir)
            os.chmod(marker_dir, 0o777)
            for out in self._two_edits(tmp):
                self._has_rule_5(out)
            self.assertEqual(os.listdir(marker_dir), [])

    # spec-example: skill-writing-reminder / a regular file in place of the marker directory is refused
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_regular_file_in_place_of_the_marker_directory_is_refused(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp = os.path.realpath(tmp)
            in_the_way = os.path.join(tmp, self._marker_dir_name())
            with open(in_the_way, "w", encoding="utf-8") as fh:
                fh.write("not a directory\n")
            for out in self._two_edits(tmp):
                self._has_rule_5(out)
            with open(in_the_way, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "not a directory\n")

    # spec-example: skill-writing-reminder / a temp directory open to others without the sticky bit is refused
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_temp_directory_open_to_others_without_sticky_bit_is_refused(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp = os.path.realpath(tmp)
            os.chmod(tmp, 0o777)
            try:
                for out in self._two_edits(tmp):
                    self._has_rule_5(out)
                self.assertEqual(os.listdir(tmp), [])
            finally:
                os.chmod(tmp, 0o700)

    # spec-example: skill-writing-reminder / a sticky shared temp directory keeps markers
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_sticky_shared_temp_directory_keeps_markers(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp = os.path.realpath(tmp)
            os.chmod(tmp, 0o1777)
            try:
                first, second = self._two_edits(tmp)
            finally:
                os.chmod(tmp, 0o700)
            self._has_rule_5(first)
            self.assertEqual(second, "", "a sticky temp directory must keep the session marker")

    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_marker_directory_and_marker_are_private(self):
        import os
        import stat
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp = os.path.realpath(tmp)
            first, second = self._two_edits(tmp)
            self._has_rule_5(first)
            self.assertEqual(second, "", "a second edit in the session with a trusted directory gets nothing")
            marker_dir = os.path.join(tmp, self._marker_dir_name())
            self.assertEqual(stat.S_IMODE(os.lstat(marker_dir).st_mode) & 0o077, 0)
            markers = [m for m in os.listdir(marker_dir) if m != ".lock"]
            self.assertEqual(len(markers), 1)
            self.assertEqual(stat.S_IMODE(os.lstat(os.path.join(marker_dir, markers[0])).st_mode) & 0o077, 0)

    def _load_hook(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("skill_writing_reminder_under_test", SCRIPTS / self.SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def _run_main(module, payload):
        import contextlib
        import io
        from unittest import mock
        out = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO(json.dumps(payload))), contextlib.redirect_stdout(out):
            code = module.main()
        return code, out.getvalue()

    EDIT_S1 = {"hook_event_name": "PreToolUse", "tool_name": "Edit", "session_id": "s-1",
               "tool_input": {"file_path": "/repo/skills/y/SKILL.md"}}

    # spec-example: skill-writing-reminder / no temp directory still sends the reminder
    def test_no_temp_directory_still_sends_the_reminder(self):
        import tempfile
        from unittest import mock
        module = self._load_hook()
        with mock.patch.object(tempfile, "gettempdir", side_effect=FileNotFoundError("no temp directory")):
            code, out = self._run_main(module, self.EDIT_S1)
        self.assertEqual(code, 0)
        self._has_rule_5(out)

    # spec-example: skill-writing-reminder / a platform that cannot verify the directory writes no marker
    def test_platform_that_cannot_verify_writes_no_marker(self):
        import os
        import tempfile
        from unittest import mock
        module = self._load_hook()
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(tempfile, "tempdir", tmp), \
                mock.patch.object(module, "_can_verify", return_value=False):
            for _ in range(2):
                code, out = self._run_main(module, self.EDIT_S1)
                self.assertEqual(code, 0)
                self._has_rule_5(out)
            self.assertEqual(os.listdir(tmp), [])

    class _Clock:
        """Stands in for the hook's `time`: advances only when the hook sleeps."""

        def __init__(self, still=False, overshoot=0.0):
            self.now = 0.0
            self.slept = 0.0
            self.sleeps = 0
            self.still = still
            self.overshoot = overshoot
            self.naps = []  # (clock reading, seconds) for each sleep

        def monotonic(self):
            return self.now

        def sleep(self, seconds):
            self.sleeps += 1
            if self.sleeps > 10000:
                raise AssertionError("the hook kept waiting")
            self.slept += seconds
            self.naps.append((self.now, seconds))
            if not self.still:
                self.now += seconds + self.overshoot

    def _scripted_lock_run(self, clock, answer):
        """Run main() with the scripted clock and a flock that asks answer(attempt, now, take) per attempt.

        answer returns "busy" to refuse the attempt, or calls take() to get the real lock.
        Returns (exit code, output, the clock reading at each attempt, the marker directory listing).
        """
        import fcntl
        import os
        import tempfile
        import types
        from unittest import mock
        module = self._load_hook()
        attempts = []
        self.taken_at = []  # clock readings at which the scripted flock really took the lock
        with tempfile.TemporaryDirectory() as tmp:
            tmp = os.path.realpath(tmp)
            marker_dir = os.path.join(tmp, self._marker_dir_name())

            def flock(fd, op):
                if not op & fcntl.LOCK_EX:
                    return fcntl.flock(fd, op)
                if not op & fcntl.LOCK_NB:
                    raise AssertionError("an exclusive lock attempt without LOCK_NB would block")
                attempts.append(clock.now)
                if answer(len(attempts), clock.now, marker_dir) == "busy":
                    raise BlockingIOError("busy")
                result = fcntl.flock(fd, op)
                self.taken_at.append(clock.now)
                return result

            fake_fcntl = types.SimpleNamespace(LOCK_EX=fcntl.LOCK_EX, LOCK_NB=fcntl.LOCK_NB,
                                               LOCK_UN=fcntl.LOCK_UN, flock=flock)
            with mock.patch.object(tempfile, "tempdir", tmp), mock.patch.object(module, "fcntl", fake_fcntl), \
                    mock.patch.object(module, "time", clock):
                code, out = self._run_main(module, self.EDIT_S1)
            listing = sorted(os.listdir(marker_dir)) if os.path.isdir(marker_dir) else None
            self.lock_free_after = None
            if listing is not None and ".lock" in listing:
                probe = os.open(os.path.join(marker_dir, ".lock"), os.O_RDWR)
                try:
                    fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self.lock_free_after = True
                except BlockingIOError:
                    self.lock_free_after = False
                finally:
                    os.close(probe)
        return code, out, attempts, listing

    @staticmethod
    def _mark(marker_dir):
        import os
        open(os.path.join(marker_dir, "s-1.skill-writing"), "w").close()

    # spec-example: skill-writing-reminder / the check runs under the session lock
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_check_runs_under_the_session_lock(self):
        def answer(attempt, now, marker_dir):
            if attempt < 3:
                return "busy"
            self._mark(marker_dir)
            return "take"

        code, out, attempts, _ = self._scripted_lock_run(self._Clock(still=True), answer)
        self.assertEqual(code, 0)
        self.assertEqual(len(attempts), 3, "the hook must keep trying while the lock is busy")
        self.assertEqual(out, "", "the marker check must see the marker that appeared before the lock was taken")

    # spec-example: skill-writing-reminder / the print and the marker write happen under the lock
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_print_and_marker_write_happen_under_the_lock(self):
        import fcntl
        import os
        import tempfile
        from unittest import mock
        module = self._load_hook()
        real_open, real_print = os.open, module._print_context
        seen = {}
        with tempfile.TemporaryDirectory() as tmp:
            tmp = os.path.realpath(tmp)
            lock_path = os.path.join(tmp, self._marker_dir_name(), ".lock")

            def lock_is_held():
                try:
                    fd = real_open(lock_path, os.O_RDWR)
                except FileNotFoundError:
                    return False  # no lock file: the hook took no lock
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    return True
                finally:
                    os.close(fd)  # closing also drops a lock taken here
                return False

            events = []

            def watched_print(rule):
                events.append("print")
                seen["print"] = lock_is_held()
                return real_print(rule)

            def watched_open(path, flags, *args, **kwargs):
                fd = real_open(path, flags, *args, **kwargs)
                if isinstance(path, str) and os.path.basename(path) == "s-1.skill-writing" and flags & os.O_CREAT:
                    events.append("marker")  # the creation succeeded
                    seen["marker"] = lock_is_held()
                return fd

            # A mocked os.open is not in os.supports_dir_fd, so the platform check is held at its real answer here.
            with mock.patch.object(tempfile, "tempdir", tmp), \
                    mock.patch.object(module, "_can_verify", return_value=module._can_verify()), \
                    mock.patch.object(module, "_print_context", side_effect=watched_print), \
                    mock.patch.object(module.os, "open", side_effect=watched_open):
                code, out = self._run_main(module, self.EDIT_S1)
            marker_exists = os.path.isfile(os.path.join(tmp, self._marker_dir_name(), "s-1.skill-writing"))
        self.assertEqual(code, 0)
        self._has_rule_5(out)
        self.assertEqual(events, ["print", "marker"], "the hook prints, then creates the session's marker")
        self.assertEqual(seen, {"print": True, "marker": True})
        self.assertTrue(marker_exists, "s-1.skill-writing must exist after the run")

    # spec-example: skill-writing-reminder / who may own the temp directory
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_who_may_own_the_temp_directory(self):
        import os
        import stat
        module = self._load_hook()
        me = os.getuid()
        rows = [  # (owner, mode, trusted)
            (me, 0o700, True),
            (0, 0o1777, True),
            (me + 1, 0o700, False),
            (me + 1, 0o1777, False),
            (me, 0o777, False),
            (me, 0o1777, True),
        ]
        for owner, mode, trusted in rows:
            with self.subTest(owner=owner, mode=oct(mode)):
                info = os.stat_result((stat.S_IFDIR | mode, 0, 0, 2, owner, 0, 0, 0, 0, 0))
                self.assertIs(module._temp_dir_trusted(info), trusted)

    # spec-example: skill-writing-reminder / a lock held too long still sends the reminder
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_lock_held_too_long_still_sends_the_reminder(self):
        clock = self._Clock()
        code, out, attempts, listing = self._scripted_lock_run(clock, lambda attempt, now, d: "busy")
        self.assertEqual(code, 0)
        self._has_rule_5(out)
        self.assertGreater(len(attempts), 1, "the hook must retry before it gives up")
        self.assertEqual([t for t in attempts if t >= 5.0], [], "an attempt started at or after the deadline")
        self.assertAlmostEqual(clock.slept, 5.0, places=6)
        long_naps = [(t, d) for t, d in clock.naps if d > 5.0 - t + 1e-9]
        self.assertEqual(long_naps, [], "no sleep may be longer than the time left")
        self.assertEqual(listing, [".lock"])

    # spec-example: skill-writing-reminder / a lock freed after the deadline is not taken
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_lock_freed_after_the_deadline_is_not_taken(self):
        def answer(attempt, now, marker_dir):
            if now < 5.0:
                return "busy"
            self._mark(marker_dir)
            return "take"

        code, out, attempts, listing = self._scripted_lock_run(self._Clock(overshoot=0.03), answer)
        self.assertEqual(code, 0)
        self._has_rule_5(out)
        self.assertTrue(attempts and all(t < 5.0 for t in attempts),
                        f"an attempt started after the deadline: {[t for t in attempts if t >= 5.0]}")
        self.assertEqual(listing, [".lock"])

    # spec-example: skill-writing-reminder / a lock taken after the deadline is let go
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_lock_taken_after_the_deadline_is_let_go(self):
        for taken_at in (5.0, 5.1):
            with self.subTest(taken_at=taken_at):
                clock = self._Clock()

                def answer(attempt, now, marker_dir):
                    if now < 4.9:
                        return "busy"
                    clock.now = taken_at  # descheduled inside flock until the deadline or past it
                    self._mark(marker_dir)
                    return "take"

                code, out, attempts, _ = self._scripted_lock_run(clock, answer)
                self.assertEqual(code, 0)
                self.assertEqual(self.taken_at, [taken_at], "the scripted flock must have taken the lock late")
                self._has_rule_5(out)
                self.assertTrue(self.lock_free_after, "the late lock must be released")

    # spec-example: skill-writing-reminder / a lock error other than busy sends the reminder at once
    @unittest.skipUnless(hasattr(__import__("os"), "getuid"), "needs a user id")
    def test_lock_error_other_than_busy_sends_the_reminder_at_once(self):
        import errno

        def answer(attempt, now, marker_dir):
            raise OSError(errno.ENOLCK, "no locks available")

        code, out, attempts, listing = self._scripted_lock_run(self._Clock(), answer)
        self.assertEqual(code, 0)
        self._has_rule_5(out)
        self.assertEqual(len(attempts), 1)
        self.assertEqual(listing, [".lock"])

    # spec-example: skill-writing-reminder / a failed read leaves the session unmarked
    def test_failed_read_leaves_the_session_unmarked(self):
        import os
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as plugin, tempfile.TemporaryDirectory() as tmp:
            os.mkdir(os.path.join(plugin, "scripts"))
            copy = os.path.join(plugin, "scripts", self.SCRIPT)
            shutil.copy(PLUGIN / "scripts" / self.SCRIPT, copy)
            env = {**os.environ, "TMPDIR": tmp}
            payload = {"hook_event_name": "PreToolUse", "tool_name": "Edit", "session_id": "s-1",
                       "tool_input": {"file_path": "/repo/skills/y/SKILL.md"}}
            code, first, err = run(copy, payload, env)
            self.assertEqual(code, 0, err)
            self.assertEqual(first, "", "a failed read must add no context")
            os.mkdir(os.path.join(plugin, "rules"))
            shutil.copy(PLUGIN / "rules" / "skill-writing.md", os.path.join(plugin, "rules", "skill-writing.md"))
            code, second, err = run(copy, payload, env)
            self.assertEqual(code, 0, err)
            self._has_rule_5(second)

    # spec-example: skill-writing-reminder / a path that only ends in SKILL.md gets no reminder
    def test_path_that_only_ends_in_skill_md_is_silent(self):
        code, out, err = run(self.SCRIPT, {"hook_event_name": "PreToolUse", "tool_name": "Edit",
                                           "tool_input": {"file_path": "/repo/skills/y/NOT-SKILL.md"}})
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")

    def rule_5(self, tool="Edit", path="/repo/skills/y/SKILL.md"):
        """The rule 5 item of the reminder, so assertions cannot be met by text elsewhere."""
        text = self.context(tool, path)
        self.assertIsNotNone(text)
        return rule_5_item(text)

    # spec-example: skill-writing-reminder / rule 5 names Practice 9 and its source
    def test_rule_5_names_practice_9_and_its_source(self):
        item = self.rule_5("Edit", "/repo/plugins/x/skills/y/SKILL.md")
        for phrase in ("(Practice 9)", "(Furnas et al., 1987)", "no name can be relied on to be guessed by people unfamiliar with it",
                       "This item summarizes Practice 9", "read Practice 9 before choosing a name"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, item)

    # spec-example: skill-writing-reminder / a new skill in an existing plugin keeps the plugin's names
    def test_new_skill_in_existing_plugin_keeps_its_names(self):
        item = self.rule_5("Write", "/repo/skills/y/SKILL.md")
        for phrase in (NEW_PLUGIN_CLAUSE, "follows that plugin's current names, prefixed or not",
                       "renamed as a whole or not at all",
                       "its name is checked against built-in commands and bundled skills unless replacing one is the intent"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, item)

    # spec-example: skill-writing-reminder / the shapes apply only in a new or wholly renamed plugin
    def test_shapes_apply_only_in_new_or_wholly_renamed_plugin(self):
        self.assertEqual(rule_5_scope_violations(self.rule_5()), [])

    # spec-example: skill-writing-reminder / an unconditional shape mandate fails the rule 5 scope check
    def test_unconditional_shape_mandate_fails_the_rule_5_scope_check(self):
        item = self.rule_5()
        for sentence in ("All skills must use these shapes.", "Shapes apply to every skill.",
                         "Every skill name starts with the plugin's short name.",
                         "Every skill must be prefixed with the plugin name.",
                         "Aim for two content words as the target and three at most."):
            with self.subTest(sentence=sentence):
                self.assertNotEqual(rule_5_scope_violations(item + " " + sentence), [])
        # last row: an indented continuation line of item 5, taken through the same extractor
        text = self.context("Edit", "/repo/skills/y/SKILL.md")
        lines = text.splitlines()
        at = next(i for i, line in enumerate(lines) if line.startswith(RULE_5_START)) + 1
        mutated = "\n".join(lines[:at] + ["   All skills must use these shapes."] + lines[at:])
        self.assertNotEqual(rule_5_scope_violations(rule_5_item(mutated)), [])

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

    # spec-example: skill-writing-reminder / collected wordings leave out three kinds of directive
    def test_collected_wordings_leave_out_three_kinds_of_directive(self):
        item = " ".join(self.rule_5().split())
        for phrase in (DIRECTIVE_CLAUSE, DIRECTIVE_CLOSED_LIST):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, item)

    # spec-example: skill-writing-reminder / item 9, the audit question and rule 5 flag names that read alike
    def test_item_9_the_audit_question_and_rule_5_flag_names_that_read_alike(self):
        text = (PLUGIN / "skills" / "skill-best-practices" / "SKILL.md").read_text(encoding="utf-8")
        lines = practice_9_section(text).splitlines()
        nines = numbered_lines_outside_fences(lines, 9)
        self.assertEqual(len(nines), 1, "Practice 9 must hold exactly one line starting '9. ' outside code fences")
        self.assertTrue(lines[nines[0]].startswith(ITEM_9_START))
        eights = numbered_lines_outside_fences(lines, 8)
        self.assertTrue(eights and eights[0] < nines[0], "item 9 must come after the line starting '8. '")
        block = " ".join(" ".join(lines[nines[0]:_block_end(lines, nines[0])]).split())
        for phrase in ITEM_9_PHRASES:
            with self.subTest(where="item 9", phrase=phrase):
                self.assertIn(phrase, block)
        self.assertNotIn("do not choose", block.lower(), "item 9 flags names; it does not forbid them")
        audit = audit_question_9(text.splitlines())
        self.assertEqual(len(audit), 1, "there must be exactly one audit question numbered 9")
        for phrase in AUDIT_NEIGHBOUR_PHRASES:
            with self.subTest(where="audit question 9", phrase=phrase):
                self.assertIn(phrase, audit[0])
        self.assertTrue(audit[0].rstrip().endswith("? (Practice 9)"))
        item = " ".join(self.rule_5().split())
        for phrase in RULE_5_NEIGHBOUR_PHRASES:
            with self.subTest(where="rule 5", phrase=phrase):
                self.assertIn(phrase, item)
        self.assertNotIn("Landauer", item, "rule 5 points to item 9 for the different-syntax case")

    # spec-example: skill-writing-reminder / a fence closes only at its own closing line
    def test_a_fence_closes_only_at_its_own_closing_line(self):
        lines = ["````markdown", "```", "9. A quoted item", "````\u00a0", "9. Another quoted item", "````",
                 "9. The real item"]
        self.assertEqual([lines[i] for i in numbered_lines_outside_fences(lines, 9)], ["9. The real item"])


class PracticeLists(unittest.TestCase):
    SKILL = PLUGIN / "skills" / "skill-best-practices" / "SKILL.md"

    # spec-example: skill-writing-reminder / item 7 and the audit question name the three kinds
    def test_item_7_and_the_audit_question_name_the_three_kinds(self):
        text = self.SKILL.read_text(encoding="utf-8")
        lines = practice_9_section(text).splitlines()
        starts = [i for i, l in enumerate(lines) if l.startswith("7. **The description lists the words users actually say")]
        self.assertEqual(len(starts), 1, "Practice 9 must hold exactly one item 7")
        block = " ".join(" ".join(lines[starts[0]:_block_end(lines, starts[0])]).split())
        for phrase in (DIRECTIVE_CLAUSE, DIRECTIVE_CLOSED_LIST):
            with self.subTest(where="item 7", phrase=phrase):
                self.assertIn(phrase, block)
        audit = audit_question_9(text.splitlines())
        self.assertEqual(len(audit), 1, "there must be exactly one audit question numbered 9")
        self.assertIn(AUDIT_DIRECTIVE_CLAUSE, audit[0])

    # spec-example: skill-writing-reminder / the plugin's own files list Practice 9
    def test_plugins_own_files_list_practice_9(self):
        lines = self.SKILL.read_text(encoding="utf-8").splitlines()
        self.assertIn("## Practice 9: Names Identify, Descriptions Get Found", lines)
        audit = [line for line in audit_question_9(lines) if line.rstrip().endswith("? (Practice 9)")]
        self.assertEqual(len(audit), 1, "the question numbered 9 must end with '? (Practice 9)'")
        research = (PLUGIN / "CLAUDE.md").read_text(encoding="utf-8").splitlines()
        self.assertTrue(table_line_below_table_line(
            research, "| 9 | Names identify, descriptions get found | Furnas, Landauer, Gomez, & Dumais (1987) |"))

    # spec-example: skill-writing-reminder / Practice 9 lists the sources for item 9
    def test_practice_9_lists_the_sources_for_item_9(self):
        entries = sources_entries(practice_9_section(self.SKILL.read_text(encoding="utf-8")).splitlines())
        self.assertEqual(source_problems(entries), [])
        doi = ITEM_9_SOURCES[0][1]
        mutations = {
            "a URL that only ends with the DOI URL": [e.replace(f" https://doi.org/{doi}",
                                                              f" https://example.org/https://doi.org/{doi}")
                                                    for e in entries],
            "a second entry for the same work": entries + [f"Black, J., & Moran, T. (1982). Learning. https://doi.org/{doi}"],
            "a copy of an entry without its DOI": entries + [e.replace(f" https://doi.org/{doi}", "")
                                                           for e in entries if doi in e],
        }
        for name, changed in mutations.items():
            with self.subTest(mutation=name):
                self.assertNotEqual(source_problems(changed), [])

    # spec-example: skill-writing-reminder / Practice 9 states where its naming rules apply
    def test_practice_9_states_where_its_naming_rules_apply(self):
        section = practice_9_section(self.SKILL.read_text(encoding="utf-8"))
        self.assertEqual(practice_9_scope_violations(section), [])

    # spec-example: skill-writing-reminder / an unconditional shape mandate fails the Practice 9 scope check
    def test_unconditional_shape_mandate_fails_the_practice_9_scope_check(self):
        lines = practice_9_section(self.SKILL.read_text(encoding="utf-8")).splitlines()
        item_5 = next(i for i, l in enumerate(lines) if l.startswith(PRACTICE_9_ITEM_5))
        item_1 = next(i for i, l in enumerate(lines) if l.startswith(PRACTICE_9_ITEM_1))
        table_end = next(i for i, l in enumerate(lines) if "| Norms and personas (loaded as guidance) |" in l)
        positions = {"after item 5": _block_end(lines, item_5), "before item 1": item_1,
                     "below the table": table_end + 1}
        rows = (("Use the five shapes for every skill.", "after item 5"),
                ("Use the five shapes for each skill.", "after item 5"),
                ("Shapes apply to any skill.", "after item 5"),
                ("All skill names carry the prefix.", "after item 5"),
                ("Prefix every name with the short name.", "after item 5"),
                ("Use the five shapes for every skill.", "before item 1"),
                ("Use the five shapes for every skill.", "below the table"))
        for line, where in rows:
            with self.subTest(line=line, where=where):
                at = positions[where]
                mutated = "\n".join(lines[:at] + ["", line, ""] + lines[at:])
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
