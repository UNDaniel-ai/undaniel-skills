---
name: workspace-structure-manager
description: 工作区文件夹结构管理 - 负责 session 目录、INDEX 控制面板、阶段文档模板与收尾归档，防止任务过程失控
homepage: https://github.com/lulu-skills-common
metadata:
  emoji: "📁"
  category: "workspace-management"
  version: "1.3.0"
  standalone: false
  adapts_from: "Codea workspace-management Rule"
---

# Workspace Structure Manager

> 负责复杂开发任务的 session 载体、主线文档和阶段产物组织。

## 概述

Workspace Structure Manager 不是流程编排 skill，而是流程产物承载层。它确保：

- 临时文档统一进入 `temp/sessions/{session}/`
- 每个 session 都有 `INDEX.md` 作为控制面板
- 阶段文档有固定模板和固定命名
- 当前阶段、确认状态、可执行动作清晰可见
- 任务完成后有验收与总结，不把工作痕迹散落在根目录

## 核心原则

### 1. 临时与永久分离

**临时任务文档** → `temp/sessions/{session}/`

- 需求对齐
- 技术方案
- 实现计划
- 进度追踪
- 验收
- 收尾总结

**项目永久文档** → `docs/`、`README.md` 等

### 2. INDEX.md 是控制面板，不只是导航页

每个 session 都必须有 `INDEX.md`，并显式展示：

- 当前阶段
- 当前路由
- 阶段状态
- 已确认文档
- 下一步允许动作
- 阻塞原因
- 是否允许编码
- 是否允许宣告完成

### 3. 核心文档固定命名

Route B / Route C 的 session 核心文档固定为：

- `INDEX.md`
- `requirements-alignment.md`
- `design.md`
- `implementation-plan.md`
- `progress-details.md`
- `acceptance.md`
- `session-summary.md`

`confirmation.md` 只作为补充说明文档，不再承担主 gate 职责。

## Workspace AGENTS.md Bootstrap

当用户希望“当前工作区按 `lulu-skills-common` 的方式配置整体流程”时，应先初始化当前工作区的 `AGENTS.md`，再进入具体任务执行。

初始化规则：

- 从 `lulu-skills-common` 仓库根目录运行 `python3 tools/init_workspace.py [target-workspace]`
- 若目标工作区已存在 `AGENTS.md`，默认不得覆盖；只有用户明确要求时才允许追加 `--force`
- 生成的 `AGENTS.md` 必须包含 `complex-task-solver` 与 `workspace-structure-manager` 的首轮强制评估要求
- 模板应保留 repo-specific 扩展区域，避免共享规则覆盖项目专属约束

## 触发场景

### ✅ 自动触发

- 新开发任务开始
- 多阶段任务延续
- 需要创建需求 / 设计 / 计划 / 进度 / 验收文档
- 需要跨 Chat 恢复上下文

### ❌ 不触发

**完全不适用（应明确跳过）**：

- 用户明确指定创建单个永久文档，且与开发任务无关
- 单纯更新现有永久文档
- 原子级代码修改，且确认不需要 session 文档

**仍然适用的场景（常见误判）**：

- ✅ 用户提到 `src/...` 路径，但本质上是多阶段开发任务
- ✅ 用户说“先讨论一下”，但目标最终是落地实现
- ✅ 用户指定了文档路径，但这些文档实际上属于任务临时产物

## 触发前置检查（防漏触发）

### 前置检查清单（强制）

在处理开发任务首轮响应前，必须检查：

1. 是否为“新任务开始”或“多阶段任务延续”。
2. 是否需要创建或续用 `temp/sessions/{session}/INDEX.md`。
3. 用户是否指定路径但任务本质仍是开发任务（若是，仍应触发本 skill）。

### 首轮响应要求（强制）

当本 skill 被命中时，首轮响应必须说明：

1. session 策略（新建 / 续用 / 跳过）。
2. 若跳过 session，必须给出明确跳过理由。
3. 若与其他 skill 协同，说明先后顺序。

## Session 门禁策略（强制）

对于 Route B / Route C，session 必须承载整个阶段门禁链路：

- `requirements-alignment.md` 未确认前，不得进入设计阶段
- `design.md` 未确认前，不得进入实现计划阶段
- `implementation-plan.md` 未确认前，`INDEX.md` 必须标记 `是否允许编码：否`
- `acceptance.md` 与 `session-summary.md` 未完成前，`INDEX.md` 必须标记 `是否允许宣告完成：否`

AI 在更新文档时必须同步更新 `INDEX.md` 的门禁状态，不能只改子文档。

## 门禁确认记录（强制）

对需要用户确认的阶段推进，session 不只要记录“已确认 / 待确认”，还必须记录“确认是怎么发生的”。

强制要求：

- AI 必须先发起一次显式阶段确认，说明当前阶段、待进入阶段、当前主文档和未确认前不会做什么
- 用户必须用带目标阶段名的明确确认语句回复
- `继续`、`好的`、`按这个来`、需求补充或纠偏，都不构成阶段确认
- 收到有效确认后，必须把以下内容写入当前阶段主文档，并同步更新 `INDEX.md`

最小记录字段：

- `AI 发起确认消息`
- `用户确认原话`
- `确认时间`

## 核心能力

### 1. Session 管理

Session 命名格式：

```text
temp/sessions/YYYY-MM-DD-HHMM-{keywords}/
```

命名原则：

- 提取 2-3 个关键词
- 优先动作词：`add`、`fix`、`refactor`、`update`
- 再提取主题词：`auth`、`login`、`api`、`database`

### 2. INDEX.md 控制面板

`INDEX.md` 必须展示用户最关心的 4 类信息：

1. 我们对需求的理解
2. 整体技术方案状态
3. 详细实现步骤与当前进度
4. 任务收尾与经验沉淀状态

### 3. 模板驱动文档

所有阶段文档都必须使用统一模板。模板重点不是“写漂亮文档”，而是把阶段门禁写实：

- `requirements-alignment.md`：范围、约束、验收、未决问题、确认结论
- `design.md`：当前代码事实、方案、图、风险、确认结论
- `implementation-plan.md`：TDD 步骤、依赖、例外、确认结论
- `progress-details.md`：真实执行、根因调查与阻塞恢复
- `acceptance.md`：验收场景、fresh verification evidence 与结果
- `session-summary.md`：总结、遗留项、治理候选

### 4. 收尾与清理

任务完成后，session 至少要保留：

- `acceptance.md`
- `session-summary.md`
- `INDEX.md` 最终状态

清理或归档前，应确保：

- 关键结论已写回 `session-summary.md`
- 治理结论已记录
- `INDEX.md` 可以独立说明本次任务发生了什么

## 与其他 Skills 的关系

- ✅ 不替代 `complex-task-solver`：后者负责路由和阶段控制
- ✅ 不替代 `skills-manager`：后者负责技能治理与同步
- ✅ 为流程型 skill 提供统一的文档载体和恢复入口

## 最佳实践

1. 检测到 Route B / Route C 时，优先创建或续用 session
2. 每次阶段变化都更新 `INDEX.md`
3. 核心门禁状态以 `INDEX.md` 为准
4. 不要把关键确认只留在聊天里，必须落到文档
5. 记录确认时优先保留用户原话，不要只写“已确认”
6. 当工作区尚未接入共享流程时，优先通过 `tools/init_workspace.py` 初始化当前目录的 `AGENTS.md`
7. 完成后保留清晰的 summary，再考虑归档或清理

## 限制与注意事项

- 本 skill 不决定流程是否该走 Route B / Route C，那是 `complex-task-solver` 的职责
- 本 skill 不应挪动或污染项目已有永久文档
- 用户明确拒绝使用 session 时，应说明跳过理由并尊重用户选择

## 版本历史

- **v1.4.0** (2026-03-11) - 升级执行与验收模板承载
  - 强化：`progress-details.md` 需要承载根因证据、假设、验证动作与修复结论
  - 强化：`acceptance.md` 需要承载 fresh verification evidence 与 claim 映射
  - 强化：`implementation-plan.md` 需要显式体现 `Verify RED / Verify GREEN / TDD 例外`

- **v1.3.0** (2026-03-10) - 新增门禁确认记录协议
  - 新增：门禁确认记录（强制）
  - 强化：普通“继续 / 好的”不构成阶段确认
  - 强化：阶段推进后必须记录 `AI 发起确认消息`、`用户确认原话`、`确认时间`

- **v1.2.0** (2026-03-10) - 新增 workspace bootstrap 入口
  - 新增：当前工作区 `AGENTS.md` 初始化规则
  - 新增：`tools/init_workspace.py` 作为共享流程接入入口
  - 强化：首轮强制评估要求可通过 workspace bootstrap 落地

- **v1.1.0** (2026-03-10) - 重构为 session 门禁承载层
  - 新增：核心文档固定集合（含 `acceptance.md`、`session-summary.md`）
  - 新增：`INDEX.md` 控制面板字段
  - 新增：Session 门禁策略（允许编码 / 允许完成）
  - 调整：`confirmation.md` 降级为补充文档

- **v1.0.2** (2026-03-10) - 新增触发前置检查协议
  - 新增：首轮前置检查清单（任务类型、session 策略、路径歧义）
  - 新增：首轮响应要求（session 策略与跳过理由）
  - 强化：用户指定路径但属于开发任务时，必须继续触发

- **v1.0.1** (2026-03-10) - 优化触发条件
  - 精细化排除规则：只排除"永久文档且无 session 需求"
  - 添加"仍然适用的场景"说明，防止误判
  - 修复：用户指定路径的开发任务仍应触发 skill

- **v1.0.0** (2026-03-09) - 初始版本
  - Session 管理、INDEX.md、模板库、子任务管理、多项目追踪、清理策略
