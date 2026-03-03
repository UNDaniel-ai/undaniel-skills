---
name: dev-workflow-core
description: 开发流程治理核心规则，用于需求分析、设计、代码改动、测试验证、提交/发布相关请求。触发场景包括需求分析、技术方案讨论、架构设计、代码改动、测试验证、提交发布、流程治理。不用于普通闲聊、翻译、摘要等非开发改动类请求。
---

# Dev Workflow Core

## 概览

- 仅在"开发改动类任务"触发并执行流程分级。
- 任何代码改动前必须获得用户明确确认。
- **所有任务强制创建会话目录与记录**（用于跨 Chat 与过程留痕）。
- **实现计划确认后才允许改代码**（硬门禁）。

## 触发范围

- **触发**：需求分析、技术方案、设计、改代码、测试、提交/发布、流程治理类请求。
- **不触发**：纯问答、翻译、摘要、闲聊、与改动无关的解释。

## 复杂度分级

| 级别 | 典型场景 | 预计时间 |
|------|---------|---------|
| **快速（简单）** | 单文件/单函数小改动，影响面可控，低风险 | 30 分钟 |
| **标准（中等）** | 多文件改动、新增模块、跨功能点 | 2 小时 |
| **完整（复杂）** | 架构调整、跨模块/多系统、高风险或多轮协作 | 1 天 |

**判断时机**：在需求对齐阶段判断。详见 [requirements-alignment.md](references/requirements-alignment.md)

## 改动门禁（强制）

**在以下全部完成并确认前，禁止任何代码改动**：

1. 需求对齐 → `requirements-alignment.md`
2. 全面讨论 → `comprehensive-discussion.md`
3. 设计输出 → `design.md`（标准/完整流程须含 Mermaid 图）
4. 影响面分析 → `impact-analysis.md`
5. 用户确认 → `confirmation.md`
6. 实现计划 → `implementation-plan.md`

**只有在"实现计划确认"后，才允许进入改动阶段。**

## 流程执行

### 阶段一：改动前准备

| 步骤 | 目标 | 输出文档 | 详细模板 |
|-----|-----|---------|---------|
| 1. 需求对齐 | 理解核心诉求，判断流程级别 | requirements-alignment.md | [模板](references/requirements-alignment.md) |
| 2. 全面讨论 | 多维度讨论，完整性检查 | comprehensive-discussion.md | [模板](references/comprehensive-discussion.md) |
| 3. 设计输出 | 架构图、流程图（Mermaid） | design.md | [模板](references/design.md) |
| 4. 影响面分析 | 代码/功能/性能/风险分析 | impact-analysis.md | [模板](references/impact-analysis.md) |
| 5. 用户确认 | 用户审查并确认 | confirmation.md | [模板](references/confirmation.md) |
| 6. 实现计划 | 生成详细实现步骤 | implementation-plan.md | [模板](references/implementation-plan.md) |

### 阶段二：代码改动

**前提**：用户已确认实现计划。

执行原则：
1. 严格按实现计划执行
2. 每开始一个步骤，必须读取任务清单，逐项执行
3. 每完成一个任务，必须立即更新任务清单状态
4. 保持 INDEX.md 和 implementation-plan.md 同步更新

### 阶段三：提交前检查

1. `git status` / `git diff` 审核
2. 逐文件深度检查
3. 测试覆盖率检查（目标 90%）
4. 编译检查
5. 改动可视化文档检查
6. 汇总报告与用户确认

## 会话文档规则

### 目录创建

**所有任务**必须创建会话目录：
- git 项目内：`<git_root>/temp/sessions/YYYY-MM-DD-HHMM-keywords/`
- 非 git 项目：`~/Developer/sessions/YYYY-MM-DD-HHMM-keywords/`
- keywords：从用户首条消息提取 2-3 个关键词，短横线连接

### INDEX.md 主线文档

每个会话目录必须包含 `INDEX.md`，作为任务主线。详见 [session-docs.md](references/session-docs.md)

核心规则：
- 创建时间和最后更新时间必须使用命令 `date "+%Y-%m-%d %H:%M"` 获取，禁止手写或推断
- 核心诉求与验收标准必须写入 INDEX，作为完成判定依据
- INDEX.md 保持简洁，详细信息分离到独立文档
- 所有会话文档开头添加返回链接：`[← 返回主线文档](INDEX.md)`
- INDEX.md 指向所有会话文档（双向链接）

### INDEX.md 更新时机

1. 创建新文档时 → 更新文档关系图
2. 重要进展时 → 更新当前进度、关键里程碑
3. 关键决策时 → 记录决策和原因
4. 代码改动时 → 更新相关资源、当前进度
5. 每次对话结束时 → 更新当前状态

### 记录与演进

- 方案/验收变更 → 记录到 `change-log.md`，同步更新 INDEX。模板：[change-log.md](references/change-log.md)
- 任何行动（分析、实验、测试、结论）→ 记录到 `activity-log.md`。模板：[activity-log.md](references/activity-log.md)
- 详细进度与剩余工作 → 记录到 `progress-details.md`，INDEX 只保留摘要。模板：[progress-details.md](references/progress-details.md)
- 跨 Chat 续航 → 维护 `handoff.md`。模板：[handoff.md](references/handoff.md)

### 跨 Chat 续航

**每次新 Chat 开始时（触发开发改动类请求前），主动检查是否有未完成的会话**：

1. 检查 `temp/sessions/`（git 项目内）或 `~/Developer/sessions/`（非 git）下是否有最近 48 小时内的会话目录
2. 如果存在，读取其 `INDEX.md` 的"当前状态"和"剩余工作"
3. 如果任务未完成，向用户提醒：
   - "检测到有未完成的任务：[任务名称]，当前进度 XX%。是否继续？还是开始新任务？"
4. 用户选择继续时：
   - 读取 `INDEX.md` + `handoff.md` 恢复上下文
   - 读取 `implementation-plan.md` 获取精确进度
   - 展示进度摘要，询问从哪个步骤继续
   - 更新 INDEX.md 的最后更新时间
5. 用户选择开始新任务时：正常创建新会话目录

**对话中断/结束时（用户说"先到这"、"明天继续"等）**，必须：

1. 更新 `handoff.md`（当前状态、已完成、下一步、阻塞/风险、重要上下文）
2. 更新 `INDEX.md`（当前状态、当前进度、剩余工作、最后更新时间）
3. 更新 `implementation-plan.md`（确保步骤状态准确）
4. 更新 `activity-log.md`（记录本次对话行动）

## 子任务管理（大型任务）

满足以下任一条件时为大型任务：
- 包含 ≥3 个独立改动点
- 需要逐步分析、逐步改动
- 跨越多次对话
- 用户明确要求"逐一分析"或"一项项来"

子任务目录结构：
```
temp/sessions/{session}/
├── INDEX.md
├── sub-task-01-{short-name}/
│   ├── design.md
│   ├── impact-analysis.md
│   ├── confirmation.md
│   └── implementation-plan.md
├── sub-task-02-{short-name}/
│   └── ...
```

子任务命名：`sub-task-{NN}-{short-name}`（NN 两位数字，short-name 2-3 关键词 kebab-case）

INDEX.md 中必须添加任务分解章节：
```markdown
## 任务分解
1. ✅ [子任务1](sub-task-01-xxx/design.md) - 已完成
2. 🟡 [子任务2](sub-task-02-yyy/design.md) - 进行中
3. ⏸️ [子任务3](sub-task-03-zzz/design.md) - 待开始
```

## 决策点（必须结构化）

在关键决策点必须使用结构化格式，禁止简单询问"可以吗？"。详见 [decision-format.md](references/decision-format.md)

必须使用结构化决策的场景：
1. 确定需求理解时
2. 确定技术方案准备改代码时（必须）
3. 提交前检查完成时
4. 发现矛盾或需用户介入时

## 分支确认机制

改代码前必须记录当前分支，并与预期一致。

## Mermaid 图规则

- **标准/完整流程**必须提供至少 1 张 Mermaid 图
- 优先使用流程图 + 架构图；保持 3-7 个关键节点
- 涉及流程/架构改动时，必须给出"改动前/改动后"图示或差异说明
- 图示以"便于判断"为目标，避免不必要细节
- 模板：[diagram-templates.md](references/diagram-templates.md)

## 错误恢复

遇到阶段失败时：
1. 检测失败类型（技术性 / 业务问题 / 不确定）
2. 技术性问题 → 自动恢复（重试 → 简化 → 跳过）
3. 业务问题 → 用户确认
4. 无法恢复 → 回退机制

详见 [error-recovery.md](references/error-recovery.md)

## 时间戳规则

- 统一使用 `date "+%Y-%m-%d %H:%M"` 获取时间戳
- 禁止手写或推断时间戳

## 完成判定

- 仅当验收标准全部满足时，事项可标记完成
- 验收标准记录在 INDEX.md 中，作为唯一判定依据

## 影响面检查清单

快速参考：[impact-checklist.md](references/impact-checklist.md)

## 参考资料索引

| 文档 | 用途 |
|-----|-----|
| [session-docs.md](references/session-docs.md) | 会话目录与 INDEX 模板 |
| [requirements-alignment.md](references/requirements-alignment.md) | 需求对齐模板 |
| [comprehensive-discussion.md](references/comprehensive-discussion.md) | 全面讨论模板 |
| [design.md](references/design.md) | 设计文档模板 |
| [impact-analysis.md](references/impact-analysis.md) | 影响面分析模板 |
| [confirmation.md](references/confirmation.md) | 确认记录模板 |
| [implementation-plan.md](references/implementation-plan.md) | 实现计划模板 |
| [error-recovery.md](references/error-recovery.md) | 错误恢复模板 |
| [decision-format.md](references/decision-format.md) | 结构化决策模板 |
| [change-log.md](references/change-log.md) | 变更记录模板 |
| [progress-details.md](references/progress-details.md) | 进度清单模板 |
| [handoff.md](references/handoff.md) | 交接模板 |
| [activity-log.md](references/activity-log.md) | 活动日志模板 |
| [diagram-templates.md](references/diagram-templates.md) | Mermaid 图模板 |
| [impact-checklist.md](references/impact-checklist.md) | 影响面检查清单 |
