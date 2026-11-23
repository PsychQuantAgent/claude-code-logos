---
name: skill-best-practices
description: |
  Evidence-based practices for writing better Claude Code skills.
  Use when creating new skills, reviewing existing skills, or when a skill
  isn't performing as expected. Relevant requests include "improve skill",
  "skill not working", "why did it skip steps", "audit skill", "name a skill",
  "what should I call this skill", "skill naming", "skill doesn't trigger".
argument-hint: "[skill-path or topic]"
---

# Skill Best Practices

Each practice below is grounded in published research. When auditing or writing a skill, check each practice and apply where relevant.

---

## Practice 1: Checklist Visibility

> Steps not on a checklist get skipped.

**Research**: Gawande (2009) *The Checklist Manifesto* — surgical checklists reduced mortality by 47%. Hales & Pronovost (2006) showed ICU catheter infection rates dropped from 11% to 0% with a 5-item checklist. The mechanism: **making steps visible prevents omission errors**, especially for routine tasks where attention drifts.

**Application to skills**: Claude Code's `TaskCreate` tool makes steps visible in the UI. When a skill has 3+ steps, steps without a corresponding task are significantly more likely to be skipped — especially creative/judgment-heavy steps sandwiched between mechanical ones.

**How to apply**:

Skill 裡直接提供**固定的 task 清單表格**，Claude 只需要照抄建立，不需要自己決定要建什麼。

**技術限制**（來自 Claude Code 源碼驗證）：
- `TaskCreate` 是 Claude Code 的內部工具（`buildTool` 註冊），**不是 shell 命令**
- Skill 的 `!`command`` shell injection **無法呼叫 TaskCreate**，只能跑 shell 命令
- 因此 task 清單只能透過**自然語言指示** Claude 建立，不能自動執行
- 但 shell injection 可以**掃描素材**（`ls`、`find`），讓 Claude 看到具體檔案再決定哪些 task 要建、哪些要跳過

**最佳做法**：shell injection 掃描 + 固定 task 表格

```markdown
## 素材掃描（自動執行）
```!
echo "SRT:"; find lectures/ -name "*.srt" 2>/dev/null || echo "  (無)"
echo "MD:"; find lectures/ -name "*.md" 2>/dev/null || echo "  (無)"
```

## 建立 Checklist
根據掃描結果，用 TaskCreate 工具建立以下 task（一次全部建完）。
沒有素材的步驟直接標 completed（附註「無素材」）。

| # | subject（直接複製） | 類型 | 跳過條件 |
|---|-------------------|------|---------|
| 1 | SRT 基礎校正 | 機械 | 沒有 .srt |
| 2 | ⚠️ 讀逐字稿，充實講義內容 | **創意** | **不可跳過** |
| 3 | 講義結構自檢 | 驗證 | 不可跳過 |
| 4 | HTML build | 機械 | 沒有 .srt |
```

**Before (bad)** — 讓 Claude 自己決定建什麼：
```markdown
## Steps
1. Read the SRT file
2. Correct misheard words
3. Read transcript and enrich lecture content ← SKIPPED
4. Build HTML
5. Update index
```

**After (good)** — skill 直接給出表格，Claude 照建：
```markdown
| # | subject（直接複製到 TaskCreate） | 類型 |
|---|--------------------------------|------|
| 1 | SRT 基礎校正（Speaker + 誤聽詞庫） | 機械 |
| 2 | **⚠️ 讀逐字稿全文，充實講義內容** | **創意** |
| 3 | 講義結構自檢 | 驗證 |
| 4 | HTML build + 影片連結 | 機械 |
```

**三個關鍵原則**：
1. **Skill 給清單，不是 Claude 自己建** — 減少 Claude 的判斷空間，降低遺漏
2. **用表格格式** — subject 欄直接複製，比自然語言段落更不容易被改寫
3. **標注類型（機械/創意/驗證）** — 讓 Claude 知道哪些步驟需要放慢

---

## Practice 2: Separate Mechanical from Creative

> Don't mix assembly-line work with judgment work in the same phase.

**Research**: Sweller (1988) *Cognitive Load Theory* — working memory has limited capacity. Switching between rule-following (mechanical) and open-ended judgment (creative) tasks imposes **extraneous cognitive load**. Monsell (2003) showed task-switching costs increase with task complexity.

**Application to skills**: When a skill mixes `sed` replacements, `make` commands, and "read the full transcript to find missing content" in one linear flow, the mechanical steps create momentum that carries past the creative step. The agent wants to keep "making progress" (completing tasks) rather than slowing down for judgment.

**How to apply**:

Group steps by type, with creative steps explicitly called out:

```markdown
## Phase 1: Mechanical Setup
- [ ] SRT speaker labels
- [ ] Misheard word replacements
- [ ] File organization

## Phase 2: Content Creation (requires judgment)
- [ ] Read full transcript
- [ ] Identify teaching points not in notes
- [ ] Restructure and enrich lecture content
- [ ] Self-check: does the lecture pass the structure template?

## Phase 3: Mechanical Build
- [ ] HTML conversion + CSS
- [ ] Index update
- [ ] Video links
```

---

## Practice 3: Implementation Intentions

> "I will do X when Y happens" doubles the completion rate.

**Research**: Gollwitzer (1999) *Implementation Intentions* — meta-analysis showed that specifying **when, where, and how** to perform an action doubles completion rates (d = 0.65). The mechanism: pre-deciding removes the need for in-the-moment deliberation.

**Application to skills**: Vague instructions like "enrich the content" leave room for the agent to decide "this looks good enough." Specific implementation intentions remove that escape hatch.

**How to apply**:

Replace vague instructions with specific if-then rules:

**Before (vague)**:
```markdown
Read the transcript and improve the lecture notes.
```

**After (implementation intention)**:
```markdown
Read the transcript in 200-line chunks. For each chunk:
1. If a teaching point is explained in the transcript but missing from the lecture → add it
2. If a bullet point is oral/conversational → rewrite as concise written prose
3. If a concept has no example → add one from the transcript discussion
4. If a section has no h2 parent → create one

After all chunks: run the structure self-check (Practice 5).
```

---

## Practice 4: Concrete Examples Over Abstract Rules

> People follow examples more accurately than rules.

**Research**: LeFevre & Dixon (1986) showed that when instructions and examples conflict, people follow the **example** 80% of the time. Chi et al. (1989) *Self-Explanation Effect* — worked examples improve problem-solving transfer significantly more than abstract principles alone.

**Application to skills**: A skill that says "use h2 for major sections" is less effective than one that shows a complete before/after example of a well-structured lecture.

**How to apply**:

For every non-obvious instruction, include a concrete example:

```markdown
### Lecture Structure Rules

Every h3 must be under an h2. Here's what this means:

**Bad** (orphan h3):
```html
<h3>OpenClaw</h3>
<p>可能會偷偷做很多事情</p>
<h3>顯著性</h3>
```

**Good** (h3 under h2):
```html
<h2>AI 工具比較</h2>
<h3>OpenClaw</h3>
<p>可能會偷偷做很多事情</p>
<h2>統計概念</h2>
<h3>顯著性</h3>
```
```

---

## Practice 5: Self-Check Before Completion

> Verification at the end catches errors that execution momentum misses.

**Research**: Reason (1990) *Human Error* — most errors are **slips** (correct intention, wrong action) not **mistakes** (wrong intention). Slips are caught by post-completion checks. The aviation industry's mandatory checklist before landing (GUMPS check) exists because pilots who "feel done" skip critical steps.

**Application to skills**: Claude often marks a task complete and moves on without verifying. A structured self-check at the end of a skill forces a re-scan.

**How to apply**:

Add a verification checklist as the final step of any skill:

```markdown
## Verification (must pass ALL before marking complete)

Run through this checklist. If any item fails, fix it before proceeding.

- [ ] No orphan h3 (every h3 has an h2 parent)
- [ ] Has "重點整理" section
- [ ] Has "課後作業" section
- [ ] No `/Users/` absolute paths in content
- [ ] All links resolve (href targets exist)
```

**Key**: The checklist must be **checkable** (yes/no), not subjective ("content is good enough").

---

## Practice 6: Salient Labeling for Critical Steps

> What you name a step determines whether it gets attention.

**Research**: Tversky & Kahneman (1981) *Framing Effects* — identical choices framed differently produce different decisions. Mayer (2009) *Signaling Principle* in multimedia learning — adding organizational cues (headings, emphasis) improves learning and retention by directing attention.

**Application to skills**: A step named "Process content" gets less attention than one named "**Read full transcript and enrich lecture (most important step — takes 30+ min)**". The label signals importance.

**How to apply**:

For the most critical step in a skill, use explicit importance markers:

```markdown
## Step 3: Read Transcript and Enrich Lecture Content

⚠️ **This is the most important step.** It takes the longest and requires the most judgment.
Do not rush through this. The output quality depends entirely on this step.

...specific instructions...
```

---

## Practice 7: Search Locates, Reading Decides

> A search can show where a passage is. Only reading the passage shows what it says.

**Research**: Simon (1956) described *satisficing*: a decision-maker with limited capacity stops at the first option that meets an aspiration level instead of examining every option. Pirolli & Card (1999) *Information Foraging* modelled information search as foraging, where the searcher decides when to leave a patch of information and move on; leaving early is cheap at the moment and costly when the answer was further in. Klayman & Ha (1987) showed that people test a hypothesis by looking where they expect it to hold (the *positive test strategy*), which can miss the evidence that would disconfirm it.

**Application to skills**: An agent told to "check the document against the source" will usually search the source with a keyword pattern. All three failure modes then line up. It takes the first matching line that fits what it expected (satisficing), it stops at whatever the terminal shows (an early patch exit, made worse when the output is cut by `| head`), and it searches only for wording that would confirm its expectation (positive testing). One observed case: an agent twice declared a source did not support a statement. Both times the search was piped to `head`, and the deciding line matched but fell past the cut. In one of the two, the first match came from a passage restating someone else's position, while the passage where the source stated its own conclusion, never read, said the opposite.

**How to apply**:

Any skill step that verifies something against a source names the reading action, not just a search:

**Before (search only)**:
```markdown
3. Check each claim in the draft against the source document.
```

**After (search locates, reading decides)**:
```markdown
3. For each claim in the draft:
   a. Search the source to locate candidate passages. Search output is for locating only;
      never pipe it to head/tail and then conclude from what is visible.
   b. If the claim says the source *decided*, *concluded* or *confirmed* something, Read in
      full the section where the source states its own conclusion. A passage restating
      someone else's position is not that conclusion.
   c. Before writing "the source does not say X", search again with other wordings and
      Read the surrounding section.
   d. Quote the passage (file and line) that the verdict rests on.
```

**Runtime delivery**: this plugin also delivers Practice 7 while Claude works, not only when this skill is invoked. A `SessionStart` hook injects the short rule, and a `PreToolUse` hook on `Bash` adds a one-line reminder next to the result whenever a search is piped to `head`/`tail` or capped with `-m`. Neither hook blocks the command.

**Sources**:
- Klayman, J., & Ha, Y.-W. (1987). Confirmation, disconfirmation, and information in hypothesis testing. *Psychological Review, 94*(2), 211–228. https://doi.org/10.1037/0033-295X.94.2.211
- Pirolli, P., & Card, S. (1999). Information foraging. *Psychological Review, 106*(4), 643–675. https://doi.org/10.1037/0033-295X.106.4.643
- Simon, H. A. (1956). Rational choice and the structure of the environment. *Psychological Review, 63*(2), 129–138. https://doi.org/10.1037/h0042769

---

## Practice 8: Ask Only When the Answer Changes the Next Step

> Every question stops the user. Ask when the answer would change what happens next and there is no reasonable default.

**Research**: Horvitz (1999) lists *employing dialog to resolve key uncertainties* among the principles of mixed-initiative interfaces: a system that is uncertain about the user's intentions should be able to ask, "considering the costs of potentially bothering a user needlessly." His expected-utility analysis gives a system three options: do nothing, ask, or act. Asking before an action the user wants is worth less than simply taking it, so asking is the best option only in a middle band of uncertainty. Below the band the system does nothing; above it, it acts. The thresholds move with context: the less an unwanted action is worth to the user, the higher the threshold for acting. Interruptions have measured costs for people. Mark, Gudith & Klocke (2008) found that people compensated for interruptions by working faster, at the price of more stress, higher frustration, time pressure and effort. In Altmann & Trafton's (2002) goal-activation model, a suspended goal has to be retrieved against interference from older goals, with the help of cues, and the authors discuss what this implies for the effects of task interruption. Ancker et al. (2017) found that clinicians accepted fewer decision-support alerts as they received more of them, particularly repeated alerts: the likelihood of accepting a reminder fell by 30% for each additional reminder per encounter.

**Application to skills**: A question costs the agent one line and costs the user a stop. Two things push agents to ask too much. Skills say "confirm with the user" without saying which steps need it, and rules written for irreversible actions get applied to cheap, reversible ones. One observed case: an agent treated creating an issue in the user's own repository as an irreversible action and showed a four-item confirmation block. Later the user answered "push" to a block that listed several pending pushes; the agent pushed one repository and asked again, with a full block, about the others. Its status reports listed every option, including ones the user had nothing to decide about. In Horvitz's terms each of these questions was worth less than acting on the default. The other studies concern people at work and clinicians reading alerts, not an agent's questions, so applying them here is an analogy: a confirmation that appears at every step is the frequent, repeated kind of prompt that Ancker et al. found clinicians less likely to act on.

This is not "ask less". The same analysis keeps irreversible actions in the confirmation branch: when acting wrongly is costly, the threshold for acting without asking rises. Pushing code, sending a message, publishing, paying and deleting without a backup are still confirmed. The practice moves questions from where the answer does not matter to where it does.

**How to apply**:

A skill step that asks the user states what the answer changes, and the default to use when there is one. Irreversible steps are grouped so that one confirmation covers them.

**Before (asks at every step)**:
```markdown
4. Ask the user to confirm before each action: creating the issue, adding the label,
   pushing the branch, opening the pull request.
5. Report every check that passed and every option for what to do next.
```

**After (asks where the answer matters)**:
```markdown
4. Create the issue and add the label in the user's repository, then report them in one
   line. These are routine records; do not ask, as long as the user asked for this work,
   the body has no private content (credentials or tokens, third-party verbatim text,
   other people's names or personal data, unpublished work, absolute paths on this
   machine) and it mentions no one with @. Otherwise ask first.
5. Pushing the branch and opening the pull request publish code. Ask once for both: list
   what will be pushed, to which remote, and the pull request title, then wait. One
   approval covers the batch; do not ask again about an item in it.
6. When a decision has a default (a convention, this skill's default, an earlier answer
   in the conversation), use it and say so in one line instead of asking.
7. Report what was done, where, and what is left for the user to decide. Leave out
   options the user has nothing to decide about.
```

Before a skill asks the user anything, check:
- Did the user, their CLAUDE.md or the skill itself say to ask or wait here? Then ask. This practice removes only the questions an agent adds on its own.
- Would any answer change what the agent does next? If not, do not ask.
- Is there a reasonable default for a reversible decision? Use it and state it.
- Is the action irreversible, or does it send private content somewhere? Then ask, once, listing every such action. If it is unclear whether the action can be undone, treat it as irreversible.
- Are there other questions for the user in this step? Ask them in the same message, not over several turns.
- Has the user already approved exactly this item, unchanged? Do not ask again. If the item changed or is new, ask.

**Runtime delivery**: the `SessionStart` hook injects the short Practice 8 rule next to the Practice 7 rule. No hook watches questions. `PreToolUse` context is added alongside the tool result, so a reminder on `AskUserQuestion` would arrive after the user had already been asked, and most of these questions are plain text in a reply, which no tool hook sees.

**Sources**:
- Altmann, E. M., & Trafton, J. G. (2002). Memory for goals: An activation-based model. *Cognitive Science, 26*(1), 39–83. https://doi.org/10.1207/s15516709cog2601_2
- Ancker, J. S., Edwards, A., Nosal, S., Hauser, D., Mauer, E., & Kaushal, R. (2017). Effects of workload, work complexity, and repeated alerts on alert fatigue in a clinical decision support system. *BMC Medical Informatics and Decision Making, 17*, Article 36. https://doi.org/10.1186/s12911-017-0430-8
- Horvitz, E. (1999). Principles of mixed-initiative user interfaces. In *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems* (pp. 159–166). ACM. https://doi.org/10.1145/302979.303030
- Mark, G., Gudith, D., & Klocke, U. (2008). The cost of interrupted work: More speed and stress. In *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems* (pp. 107–110). ACM. https://doi.org/10.1145/1357054.1357072

---

## Practice 9: Names Identify, Descriptions Get Found

> A skill's name is how it is called and told apart. Its description is the main way it is found. No name can be counted on to be guessed by people unfamiliar with it.

**Research**: Furnas, Landauer, Gomez & Dumais (1987) collected the words people spontaneously use for objects in five domains, among them text-editing operations, commands for a hypothetical message decoder and recipes (p. 965). Two people applied the same term to an object with probability .07 to .18 (p. 966). When one person chose the name, which the authors call the "Armchair" design method, other untutored people failed to reach the object on 80 to 90 percent of their attempts (pp. 965–966). In the recipe study the expert cooks' keywords fared no better than average, and the command names for the hypothetical message decoder, chosen by and for experts, had very low agreement (pp. 965–966). Requiring names to be unique lowered the already low success rates by a further 5 to 60 percent of their value (typically about 10 percent), and "constraining names to be multiple word strings, systematic, 'cute,' or even 'mnemonic,' is certain to result in even less likely first-try success" (p. 966). Even the term people used most often failed 65 to 85 percent of the time, from which the authors concluded that "there can exist no rules, guidelines or procedures for choosing a good name, in the sense of 'accessible to the unfamiliar user'" (p. 967). Their remedy was many alternative access words per object: for the service in their naming exercise, one person rarely thought of more than half a dozen names, while people together suggested over a hundred (p. 968). In what they call adaptive indexing, words that failed at first are added to the index, with the user's agreement, once the user finds what they wanted (p. 970). Because many commands are too consequential to run on guessed intent, they proposed using the alias system only as an index into a help facility that leads to the standard name, so that "actual execution would always be via the standard 'name'" (p. 969). In a footnote they add that a factorial task decomposition, where a system's structure supports one, "can lead to predictable patterns of official terminology, perhaps allowing users to predict some terminology from others" (p. 968).

**Research on names within a set**: Three earlier studies of text-editor command names looked at names within small sets of commands. Black and Moran (1982) argue that `move` is more discriminating than `put` because it "discriminates more sharply which operation it refers to within the set of operations", and that a name can also fail by being too general or by having an arbitrary link to its operation (p. 9). Groups of 12 people, one group per naming condition and 84 in all, learned eight command names for an eight-operation editor and were tested again a week later (pp. 9–10). The authors "do not report a full analysis" of the data. Their reported results (p. 10, plotted in Figure 1 on p. 11) are that infrequent, discriminating words did best on learning, free recall and choosing the name for an operation (cued choice); general words did worst on learning and on that choice; overall, discriminating words beat nondiscriminating ones on learning and choice but not on free recall; and nondiscriminating words did worse than nonwords on learning and choice. Landauer, Galotti and Hartwell (1983) taught six commands in one two-hour session and varied the vocabulary of three of them (pp. 499, 502). Which words were chosen made little difference: a post hoc test of their best against their worst vocabulary was not nearly significant, t(62) = 1.0 (p. 501). Giving line-internal and whole-line operations, which took different syntax, different names did save time, F(1, 92) = 12.05, p < .001 (p. 501). They add that "precise semantic distinction and confusability may be more important in larger sets" (p. 502), and conclude: "When varying constructions are required on the part of the user, or varying effects are obtained, different command names should be used" (p. 503). Rosenberg (1982) had 12 people judge the names one at a time, picking the operation each could name, and then pair the whole list of names with the operations one to one; he likens the task to choosing from a list of the commands available (pp. 13–14). His measure of a good name ignores the other names in the set, and on inspecting its prediction errors after the fact he found almost all of them explainable by that set: names fairly similar to many others in the set, or extremely similar to one other, could be picked much less accurately than the measure suggests, `change` being confused with `substitute` or `replace` in all three name sets, while a name unlike the rest, `store`, could be picked much more accurately (p. 15). He leaves a more detailed investigation to a forthcoming report (p. 15). On remembering and typing a name, words did better than nonwords in free recall a week after training (Black & Moran, p. 10), and one-letter commands cut the characters typed without a significant difference in completion time (Landauer et al., p. 501). No study here tested recall after a single use, and this practice draws no rule on remembering or typing from these results beyond item 4. Grudin and Barnard's 1984 paper on command names for text editing and Landauer and Galotti's comment on it, both in *Human Factors*, were not read for this practice.

**Application to skills**: A skill has two parts that match the two roles in the paper. The name is the standard term: it is what a user types after `/` and what Claude calls, and the skill listing always contains every name, while descriptions are dropped to fit the budget when there are many skills, starting with the skills used least (Claude Code skills documentation, read 2026-11-23). The description plays the part of the alias list: it carries the words through which a request reaches the skill. When the listing has dropped a skill's description, only the name is left to match, which is why the name still carries what identifies the skill: its action and, unless the plugin makes it clear, its object; for a conversion, its product; or its mode or topic. Furnas and colleagues studied people guessing names for system objects, not a model matching a request against a skill listing, so applying their findings here is an analogy. What carries over is the division of labour. No naming rule makes a name reliably guessable for people unfamiliar with it, so a name is judged by whether it is unique, precise and consistent with the other names in its plugin; whether people find the skill is mainly the description's job. Finding a skill through its description does not authorize what the skill does: a match picks a candidate, and the skill's consequential steps still need the confirmations they would need otherwise, just as the paper kept execution on the standard name. Two Claude Code behaviours make uniqueness a design problem and not just good manners: plugin skills are namespaced as `plugin-name:skill-name`, so a plugin skill and a skill elsewhere with the same name both load, and the documentation does not say which one runs when two plugins each ship a skill named `search` and the user types only `/search`; in a local terminal session, a personal or project skill with the same name as a built-in command replaces that command, though not its aliases. One observed case shows a failed guess next to a step named after its internal mechanism: a user who wanted the subtitles of a recording typed `/plaud-to-srt`, but the skill was named `plaud-srt`; and the step it depended on was named `plaud-index`, after its indexing mechanism, while its description emphasized searching rather than the subtitle task the user asked for. Both were renamed in PsychQuant/plaud-mcp-connector#65.

**How to apply**:

The name follows one grammar across a collection. Anthropic's skill authoring guide suggests gerund forms and asks a collection to avoid inconsistent patterns; this grammar, decided in PsychQuant/che-plugin-devtools#74, keeps the second point and replaces gerunds with a shape for each kind of skill.

Where a skill lives decides which of these rules apply. Items 1 to 4 describe the names in a new plugin or in one renamed as a whole, meaning all of its skill names are migrated together. A new skill in an existing plugin follows that plugin's current names, prefixed or not (item 5). A skill outside any plugin, such as a personal or project skill, has no short name and is not given a prefix; check its name against bundled skills and built-in commands unless replacing one is the intent, since a personal or project skill with the same name replaces a bundled skill, and a built-in command in a local terminal session.

1. **Every skill name starts with the plugin's short name.** The short name is one word, unique across plugins, and different from every built-in command and bundled skill. Namespacing (`plugin-name:skill-name`) separates two plugins' skills when the namespace is typed; when it is not, the documentation does not say which one runs. A prefix makes such a collision less likely; when it matters which plugin runs, type the namespace.
2. **The shape follows what the skill does.** Five kinds, and only these five:

   | Kind | Shape | Example |
   |---|---|---|
   | Conversion (one source becomes one product) | `short-to-product` | `plaud-to-srt` |
   | Action | `short-[object-]verb` | `idd-close`, `hd-mcp-deploy` |
   | Query or settings | `short-noun` | `codex-status`, `codex-config` |
   | Orchestration (runs several steps or agents) | `short-mode`, a noun naming how it runs (`all`, `batch`, `loop`, `chain`, `ensemble`) | `idd-all`, `codex-batch` |
   | Norms and personas (loaded as guidance) | `short-noun` | `axiom-statistics` (illustrative) |

   When one pipeline can run in more than one way, each way gets its own mode word (`idd-all`, and `idd-chain` as an illustration), as decided on PsychQuantAgent/claude-code-logos#36 on 2026-11-22.

3. **Two content words is the target; three is the maximum.** `to` and similar function words do not count. A third word is allowed only when the plugin handles several kinds of object and the verb alone would not say which; the noun then comes before the verb.
4. **`-to-` is reserved for conversion.** Each product gets its own skill. Other conversion spellings (`X2Y`, `Y-from-X`, `convert-X-Y`, `export-Y`) are not used. Nouns are singular; no invented abbreviations; common format names such as `srt` and `pdf` are fine.
5. **Existing names are not renamed piecemeal.** A new skill follows its plugin's current convention, so one plugin never mixes two naming conventions; when a plugin's skill names are renamed, they are renamed as a whole (PsychQuant/che-plugin-devtools#74).

Items 6 to 9 apply to every skill, wherever it lives.

6. **Check that the name says what the skill is.** Expand an action or conversion name into "I want to ___" (the test from PsychQuant/che-plugin-devtools#28). An action name should give back the main action, and the object either named or clear from the plugin (`idd-close` closes an issue). A conversion name should give back its product. Whatever the name's shape, the description names the source when neither the name nor the plugin makes it clear; the `short-to-product` shape has no slot for the source. An orchestration name should give back how it runs, and a query, settings or guidance name its topic (the checks for kinds other than action are added here). Either way the check is for precision; per Furnas (p. 967) it does not show that others will guess the name.

The description carries the words people use:

7. **The description lists the words users actually say for the job**, several phrasings and not one, including the names of the objects and formats involved. One person usually thinks of only a handful of them (p. 968), so collect wordings from real requests, not only from the author. Write each one as a short phrase with no private details (names, paths, the content of the work), however it was collected. Each phrase keeps the task it names and leaves out any part that grants a permission, skips a check or waives a confirmation (only these three kinds; do not extend the list by similarity): a request to "deploy without asking" goes in as "deploy". A description sits in the skill listing that a session reads before the user's request (Claude Code skills documentation, read 2026-11-23), so a directive copied into it would reach every session that lists it, while a match should only pick a candidate (see the application paragraph above).
8. **When a user's wording fails to reach a skill, add that wording to the description** in the same way, as a short phrase with no private details and without those three kinds of directive (item 7). This adapts adaptive indexing (p. 970): there the user agreed to each addition; here the skill's author decides, in the change that edits the description. Renaming the skill to that one word is not enough on its own: even the word people use most often fails most of the time (p. 967). Whether an existing plugin's skills are renamed at all follows item 5.

The name is also judged against the names around it:

9. **Check the name against the other names in its listing.** Read it next to the other skill names in its plugin, or, for a skill outside any plugin, next to the other skills in the same skills directory, and ask whether a reader could swap it with one of them. Flag a candidate that is a near-synonym of a neighbour or general enough to fit several of the neighbouring skills, and prefer one that shows what sets this skill apart when such a name fits the plugin's naming convention: next to an `idd-verify` that checks an implementation against its issue, a skill that runs the test suite is clearer as `idd-test` than as `idd-check`, and `idd-manage` would fit most skills in that plugin (illustrative). An overlap between names the plugin already has is recorded for a whole-plugin rename under item 5, not fixed by renaming one skill. Skills that need different arguments or syntax, or that have different effects, should not differ only by near-synonyms: Landauer et al. found that different names helped where the syntax differed (1983, pp. 501, 503), and Rosenberg's near-synonyms were confused with each other (1982, p. 15); this check does not split a skill or override the naming grammar. The evidence is limited: the near-synonym part rests on one author's post hoc reading of 12 people's choices (Rosenberg, 1982, p. 15), general words did worst on learning and cued choice in one study (Black & Moran, 1982, p. 10), and the studies had people learn or match six to ten text-editor commands, not a model choose from a skill listing, so applying them here is an analogy, as it is for Furnas. Like item 6, this check is for telling skills apart; it does not make a name guessable (Furnas et al., 1987, p. 967).

The two drafts below are for a skill in a new plugin; in an existing plugin, item 5 applies.

**Before (one name, one phrasing for finding it)**:
```markdown
---
name: srt
description: Export transcript.
---
```

**After (a name that identifies, a description that can be found)**:
```markdown
---
name: plaud-to-srt
description: |
  Turn a Plaud recording into an SRT subtitle file. Use when the user wants the
  subtitles, captions, SRT or a timed transcript of a Plaud recording, or asks
  to "get the subtitles of this Plaud recording".
---
```

The "After" name is unlikely to collide with another plugin's skill because of its prefix, has the conversion shape, and passes the "I want to ___" test ("I want to turn a Plaud recording into SRT"). The description, not the name, carries "subtitles", "captions" and "timed transcript". A request such as "get the subtitles, no need to ask" would go into it as "get the subtitles". The descriptions above are illustrative, not copied from a published skill.

**Runtime delivery**: the existing `PreToolUse` hook on `Write|Edit` adds `rules/skill-writing.md`, which includes the Practice 9 rule, before the first Write or Edit of a `SKILL.md` in a session; once the hook has written its session marker, later ones in the same session get nothing. No hook checks names. Checking names when a skill is created, and auditing existing names, belong to `harness-devtools` (PsychQuant/che-plugin-devtools#74), which cites this practice.

**Sources**:
- Black, J. B., & Moran, T. P. (1982). Learning and remembering command names. In *Proceedings of the 1982 Conference on Human Factors in Computing Systems* (pp. 8–11). Association for Computing Machinery. https://doi.org/10.1145/800049.801745
- Furnas, G. W., Landauer, T. K., Gomez, L. M., & Dumais, S. T. (1987). The vocabulary problem in human-system communication. *Communications of the ACM, 30*(11), 964–971. https://doi.org/10.1145/32206.32212
- Landauer, T. K., Galotti, K. M., & Hartwell, S. (1983). Natural command names and initial learning: A study of text-editing terms. *Communications of the ACM, 26*(7), 495–503. https://doi.org/10.1145/358150.358157
- Rosenberg, J. (1982). Evaluating the suggestiveness of command names. In *Proceedings of the 1982 Conference on Human Factors in Computing Systems* (pp. 12–16). Association for Computing Machinery. https://doi.org/10.1145/800049.801746
- Claude Code skills documentation, read 2026-11-23: https://code.claude.com/docs/en/skills (the skill listing and its budget; which skill runs when names are the same)
- Anthropic, Skill authoring best practices, naming conventions: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

## How to Use This Skill

### Audit an existing skill
```
/skill-best-practices path/to/SKILL.md
```
Reads the skill and checks each practice. Reports which practices are applied and which are missing.

### When writing a new skill
Invoke this skill before writing. Use the practices as a checklist for the skill you're about to create.

### When a skill isn't performing
If Claude keeps skipping steps or producing shallow output, check:
1. Is there a TaskCreate instruction? (Practice 1)
2. Are mechanical and creative steps separated? (Practice 2)
3. Are instructions specific enough? (Practice 3)
4. Are there concrete examples? (Practice 4)
5. Is there a self-check? (Practice 5)
6. Is the critical step labeled as important? (Practice 6)
7. Does every verification step name what to Read, not just what to search? (Practice 7)
8. Does every question the skill asks change what happens next, with irreversible steps confirmed once as a batch? (Practice 8)
9. Does the name follow the convention for where the skill lives (the short-name prefix and the shape for its kind in a new plugin or one migrating all its skill names together, with a third content word only where item 3 allows it; the plugin's current names in an existing one; no prefix for a skill outside any plugin, and no clash with a bundled skill or built-in command unless replacing it is the intent), and does the description list several phrasings users actually say for the job, including any wording that once failed to reach the skill, each as a short phrase with no private details that leaves out any part that grants a permission, skips a check or waives a confirmation, and does the name pass item 6's check for its kind, with the description naming a conversion's source when neither the name nor the plugin makes it clear, and is the name neither a near-synonym of a neighbouring skill name (in its plugin, or in its skills directory for a skill outside any plugin) nor general enough to fit several of them? (Practice 9)
