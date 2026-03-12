# Workspace Init Prompt

让 Agent 参照本仓库为“当前工作目录”初始化 `AGENTS.md`。

执行要求：

1. 先以本仓库根目录为基准，阅读：
   - `README.md`
   - `skills/workspace-structure-manager/SKILL.md`
   - `skills/und-workflow-entry/SKILL.md`
   - `templates/workspace/AGENTS.md.template`
2. 然后为当前工作目录初始化 `AGENTS.md`：
   - 运行 `python3 tools/init_workspace.py .`
3. 如果当前工作目录已经存在 `AGENTS.md`：
   - 默认不要覆盖
   - 先告知用户，并等待明确确认
   - 只有用户明确要求覆盖时，才使用 `--force`
4. 生成后的 `AGENTS.md` 必须包含：
   - `und-workflow-entry`
   - `complex-task-solver`
   - `workspace-structure-manager`
   - `skills-manager`
   - `und-writing-skills`
   - 首轮强制评估 `und-workflow-entry`、`complex-task-solver` 和 `workspace-structure-manager` 的规则
   - “需求澄清不等于阶段确认”的提醒
5. 完成后向用户汇报：
   - 写入了哪个文件
   - 是否新建还是覆盖
   - 写入了哪些关键规则
   - 如果是 shared skill 维护场景，提醒后续任务会额外评估 `skills-manager` 和 `und-writing-skills`

给 Agent 的最短说法：

```text
请参照 `templates/workspace/INIT_AGENT_PROMPT.md`，为当前工作目录初始化 AGENTS.md。
如果已经存在 AGENTS.md，先不要覆盖，先告诉我。
```
