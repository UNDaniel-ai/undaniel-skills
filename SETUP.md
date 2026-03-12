# Team Setup Guide

适用对象：团队内使用 Codex / Claude 的开发同学。

本文档说明如何接入 `lulu-skills-common` 共享流程，包括：

- 拉取共享仓库
- 安装依赖
- 同步 shared skills
- 为具体工作区初始化 `AGENTS.md`
- 验证配置是否生效

## 1. 获取仓库

拉取共享仓库：

```bash
git clone git@gitlab.alibaba-inc.com:miravia-terminal-ai/lulu-skills-common.git
cd lulu-skills-common
```

如果你已经有本地副本，先确保它是最新的：

```bash
git pull --ff-only origin main
```

## 2. 安装依赖

在仓库根目录执行：

```bash
pip install -r requirements.txt
```

## 3. 同步 Shared Skills

将共享 skills 同步到本机 Agent 目录：

```bash
# 同步全部 shared skills
tools/skillctl sync --all --agent all
```

同步后建议检查状态：

```bash
tools/skillctl status --agent all
```

如果你只想同步单个 skill，也可以：

```bash
tools/skillctl sync --skill workspace-structure-manager --agent all
```

## 4. 为具体工作区初始化 AGENTS.md

当你希望某个项目按 `lulu-skills-common` 的共享流程运行时，需要在该项目根目录生成 `AGENTS.md`。

有两种常见方式。

### 方式 A：在 `lulu-skills-common` 仓库里执行

```bash
cd lulu-skills-common
python3 tools/init_workspace.py <target-workspace>
```

示例：

```bash
python3 tools/init_workspace.py ../my-project
```

### 方式 B：在目标项目目录里执行

如果你当前就在目标项目目录，也可以直接调用共享仓库里的脚本。

```bash
python3 ../lulu-skills-common/tools/init_workspace.py . \
  --repo-root ../lulu-skills-common
```

说明：

- `.` 表示“当前工作目录”
- `--repo-root` 用来告诉脚本共享仓库在哪里
- 如果你的目录结构不是同级，请把 `../lulu-skills-common` 改成真实相对路径

### 覆盖规则

如果目标项目已经有 `AGENTS.md`：

- 默认不会覆盖
- 你需要先确认是否保留原文件
- 只有明确要替换时，才使用 `--force`

示例：

```bash
python3 tools/init_workspace.py <target-workspace> --force
```

## 5. 让 Agent 在项目里自助初始化

如果你已经在项目里打开了 Agent 对话框，不想手动敲脚本，可以直接让 Agent 参照短指令文件完成初始化。

短指令文件在：

```text
templates/workspace/INIT_AGENT_PROMPT.md
```

推荐说法：

```text
请参照 `../lulu-skills-common/templates/workspace/INIT_AGENT_PROMPT.md`，为当前工作目录初始化 AGENTS.md。
如果已经存在 AGENTS.md，先不要覆盖，先告诉我。
```

说明：

- 上面的 `../lulu-skills-common/...` 只是“共享仓库与项目目录同级”时的常见写法
- 如果你的目录结构不同，请改成当前项目到 `lulu-skills-common` 的真实相对路径

## 6. 初始化后会得到什么

生成后的 `AGENTS.md` 会包含：

- `und-workflow-entry`
- `und-brainstorming`
- `und-writing-plans`
- `und-test-driven-development`
- `und-systematic-debugging`
- `und-verification-before-completion`
- `complex-task-solver`
- `workspace-structure-manager`
- `skills-manager`
- `und-writing-skills`
- 新开发任务首轮必须评估 `und-workflow-entry`、`complex-task-solver` 和 `workspace-structure-manager`
- `session strategy` 的显式说明要求
- “需求澄清不等于阶段确认”的提醒
- repo-specific 扩展区域

## 7. 如何验证配置是否生效

最直接的验证方式有两步。

### 第一步：检查文件是否生成

确认目标项目根目录已经有 `AGENTS.md`。

### 第二步：开一个新任务验证首轮响应

在该项目里新开一个 Agent 会话，第一条直接给开发任务，例如：

```text
请按当前 AGENTS.md 的流程处理这个开发任务：实现 xxx 功能。
```

如果配置生效，Agent 的首轮回复应该显式说明：

- `und-workflow-entry: use/skip`
- `complex-task-solver: use/skip`
- `workspace-structure-manager: use/skip`
- 显式点名或明显匹配的附加 skill 是否 `use/skip`
- 使用顺序
- `session strategy: new / reuse / skip`

在 Route B / Route C 的编码、调试、验收阶段，还应能根据场景显式路由到：

- `und-test-driven-development`
- `und-systematic-debugging`
- `und-verification-before-completion`

## 8. 常见问题

### Q1: 为什么我看到了 trust 或 `config.toml` 的提示？

`AGENTS.md` 与项目 trust / `config.toml` 是两条不同链路。

- `AGENTS.md` 控制当前工作区的流程说明
- trust / `config.toml` 控制项目级配置是否被 Codex 接受

因此：

- 即使 `AGENTS.md` 已经生成，trust 提示仍可能单独出现
- 这不代表 shared workflow 初始化失败

### Q2: 我一定要手动执行脚本吗？

不一定。

- 你可以自己执行 `tools/init_workspace.py`
- 也可以让 Agent 参照 `templates/workspace/INIT_AGENT_PROMPT.md` 自助完成

### Q3: 这份文档会覆盖项目自己的规则吗？

不会自动覆盖。

- 初始化脚本默认拒绝覆盖已有 `AGENTS.md`
- 如果项目有自己的 repo-specific 规则，可以在生成后的 `AGENTS.md` 扩展区追加

## 9. 推荐团队使用方式

建议团队统一采用下面的节奏：

1. 每位成员先 clone `lulu-skills-common`
2. 每台机器先执行一次 `tools/skillctl sync --all --agent all`
3. 每个新项目在开始前先初始化项目根目录的 `AGENTS.md`
4. 进入项目后，默认先让 Agent 按 `AGENTS.md` 流程响应

这样可以把 shared workflow、session 管理和 skill 治理保持在同一套标准下。

## 10. 维护 shared skills 时的额外验证

如果你在维护 `lulu-skills-common` 本身，除了文档和 bootstrap 初始化外，还建议执行：

```bash
tools/skillctl validate --skill und-workflow-entry
tools/skillctl validate --skill und-test-driven-development
tools/skillctl validate --skill und-systematic-debugging
tools/skillctl validate --skill und-verification-before-completion
tools/skillctl validate --skill und-writing-skills
CODEX_BEHAVIOR_TESTS=1 pytest tests/test_codex_skill_triggering.py
CODEX_BEHAVIOR_TESTS=1 pytest tests/test_codex_multiturn.py
```

说明：

- 行为测试默认是 opt-in，因为它依赖本机 `codex` 环境
- 只有当你修改了 skill 触发、入口协议或共享流程文案时，才建议把这组测试纳入回归
