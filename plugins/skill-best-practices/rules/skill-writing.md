# Skill Writing Best Practices

Delivered by the plugin's `PreToolUse` hook on `Write|Edit` when the target is a `SKILL.md` (once per session, when the hook can write its session marker). Plugins have no `rules/` component, so this file is never loaded on its own; `scripts/skill_writing_reminder.py` reads it and adds it as context.

When writing or modifying skills (SKILL.md files), apply these evidence-based principles:

1. **Checklist visibility**: Skills with 3+ steps MUST provide a **fixed task table** for Claude to create with TaskCreate. Skill 給清單，不是讓 Claude 自己決定建什麼。表格中標注每步的類型（機械/創意/驗證）和跳過條件。注意：TaskCreate 是 Claude Code 內部工具，不能從 `!`command`` shell injection 呼叫，但可以用 shell injection 掃描素材讓 Claude 判斷哪些 task 要建。

   **Concrete template — Step 0 Bootstrap**（已在 idd-* / plugin-tools / mcp-tools 60+ skill 驗證）：

   ````markdown
   ## Step 0: Bootstrap Stage Task List（強制）

   **動任何事之前**先用 `TaskCreate` 建 stage-level todo list：

   ```
   TaskCreate(name="phase_1_name", description="做什麼，包含子步驟")
   TaskCreate(name="phase_2_name", description="做什麼")
   TaskCreate(name="phase_n_name", description="做什麼")
   ```

   完成每一步立即 `TaskUpdate → completed`。**靜默完成 = 違規**。

   **為什麼強制**：[此 skill 特定的 silent failure 風險，例如「有 X 個 phase，漏了 Y 會導致 Z」]
   ````

   放在 YAML frontmatter 後、第一個執行步驟前。未提供 "為什麼" 段落的 skill 會被降級——使用者不知道為什麼要遵守就會跳過。
2. **Separate mechanical from creative**: Don't mix rule-based steps (file operations, builds) with judgment-heavy steps (content creation, analysis) in the same phase. Label creative steps with ⚠️ and explicit importance markers.
3. **Concrete examples over abstract rules**: Include at least one before/after example for any non-obvious instruction. Use tables instead of prose for task lists — tables are less likely to be rewritten by Claude.
4. **Search locates, reading decides** (Practice 7): any step that checks something against a source must name the reading action — which file and which section to `Read` — not only a search. Truncated search output (`| head`, `| tail`, `grep -m N`) is never evidence that a source lacks something. When the claim is that a source *decided* or *confirmed* something, the step reads that source's conclusions section in full. Before concluding absence, try other wordings and read the surrounding section.
5. **Names identify, descriptions get found** (Practice 9). This item summarizes Practice 9; read Practice 9 before choosing a name. Which naming rule applies depends on where the skill lives: in a new plugin, or one renamed as a whole (all its skill names migrated together), a skill name starts with the plugin's short name and takes the shape for its kind — conversion `short-to-product`, action `short-[object-]verb`, query or settings `short-noun`, orchestration `short-mode` (`all`, `batch`, `loop`, `chain`, `ensemble`), norms and personas `short-noun` — with two content words as the target and three at most (function words such as `to` do not count; a third word names the object, and only when the plugin handles several kinds of object); a new skill in an existing plugin follows that plugin's current names, prefixed or not, and its skill names are renamed as a whole or not at all; a skill outside any plugin is not given a prefix, and its name is checked against built-in commands and bundled skills unless replacing one is the intent. The name is for calling the skill and telling it apart; no name can be relied on to be guessed by people unfamiliar with it (Furnas et al., 1987). The description lists the words users actually say for the job, several phrasings and not one, each as a short phrase with no private details; a wording that once failed to reach the skill is added to the description in the same way.
