---
name: complex-task-solver
description: 完全自包含的复杂问题解决器 - 集成复杂度评分、三层流程路由、阶段门禁、方法型 skill 调度、验收与收尾治理
homepage: https://github.com/lulu-skills-common
metadata:
  emoji: "🧩"
  category: "problem-solving"
  version: "1.5.0"
  standalone: true
---

# Complex Task Solver - 复杂问题解决器

> 完全自包含。负责复杂任务的路线选择、阶段门禁、执行节奏和收尾闭环。

## 概述

Complex Task Solver 是一个任务编排 skill，核心能力包括：

- 自动评估任务复杂度（5 因子评分模型）
- 智能路由到 Route A / B / C
- 为 Route B / Route C 提供硬门禁阶段协议
- 调度 `und-brainstorming`、`und-writing-plans`、`und-subagent-driven-development`、`und-test-driven-development` 等方法型 skill
- 任务分解、TDD 执行、进度追踪与跨 Chat 恢复
- 错误恢复与动态子任务管理
- 完成后的验收、总结与技能治理闭环

## 触发场景

### ✅ 适用场景

- 用户提出复杂需求或多步骤开发任务
- 任务需要需求对齐、设计、计划、编码、测试多个阶段
- 任务需要跨模块、跨仓、跨 chat 追踪
- 实施过程中可能发现新问题，需要动态建模和恢复

### ❌ 不适用场景

**完全不适用（应明确跳过）**：

- 原子级单文件修改
  - 示例："修改 README.md 第 10 行 typo"
  - 示例："把 config.json 端口从 3000 改为 8080"
  - 关键特征：单文件、单点修改、无依赖、无架构影响

- 纯研究性探索任务，且没有实现意图
  - 示例："帮我分析一下这个项目的架构"
  - 示例："研究一下 GraphQL 的优缺点"
  - 关键特征：只做调研，不落地实现，不需要任务状态追踪

**仍然适用的场景（常见误判）**：

- ✅ 用户先说"先分析一下"、"先讨论一下"，但目标最终指向实现
- ✅ 用户提供了部分步骤，但任务仍然跨模块或多阶段
- ✅ 用户要求"快点做"，但任务客观上仍然需要设计和风险控制
- ✅ 用户指定了部分路径或文件，但本质上仍是开发任务

## 首轮技能识别协议（防漏触发）

### 首轮输出要求（强制）

当本 skill 被命中时，首轮响应必须明确给出：

1. 命中的 skill 列表（至少包含 `complex-task-solver`）。
2. 使用顺序（若有多个 skill，说明先后次序）。
3. 跳过理由（若存在明显相关 skill 未使用，必须说明原因）。

### 复杂度预检清单（强制）

在进入 Route A/B/C 前，先执行以下预检：

1. 用户是否显式点名 skill（点名则必须命中）。
2. 是否存在跨模块 / 跨仓 / 多阶段链路（满足任一项时，不可按原子任务处理）。
3. 是否需要跨 chat 续接或阶段性里程碑（满足时必须进入 Route B 或 Route C）。

### 最小覆盖集原则

优先选择覆盖需求的最小 skill 集合，避免“只命中领域 skill，漏掉流程编排 skill”。

## 核心能力

### 1. 智能复杂度评估

基于 5 因子评分模型自动评估任务复杂度：

| 因子 | 说明 | 分数范围 |
|------|------|----------|
| `fileCount` | 涉及文件数量 | 0-5 |
| `crossModule` | 跨模块影响程度 | 0-5 |
| `archChange` | 架构变更程度 | 0-5 |
| `ambiguity` | 需求模糊程度 | 0-5 |
| `risk` | 技术与交付风险 | 0-5 |

综合评分计算方式：

```text
综合评分 = (fileCount + crossModule + archChange + ambiguity + risk) / 5
```

综合评分范围是 `0.0-5.0`。路由阈值固定为：

- `0.0-1.9`：Route A（快速流程）
- `2.0-3.4`：Route B（标准流程）
- `>= 3.5`：Route C（完整流程）

**强制升级条件**：

- 存在跨模块 / 跨仓 / 多阶段链路时，不得落入 Route A
- 需要阶段性里程碑或跨 chat 恢复时，不得落入 Route A
- 需要多方案评估、全局架构重构或高风险迁移时，必须进入 Route C

### 2. 三层流程路由

#### Route A（快速流程）

适用：简单需求、实现路径明确、无需正式设计

流程：

```text
需求理解 -> 简化实现计划 -> 执行 -> 验证
```

特点：

- 不需要 Brainstorm
- 不需要正式设计文档
- 不需要阶段门禁
- 仍需要最小需求确认和结果验证

#### Route B（标准流程）

适用：中等复杂度任务，需要设计但不需要完整方案竞选

流程：

```text
需求对齐 -> 设计 -> 实现计划 -> TDD 执行 -> 验收 -> 收尾
```

特点：

- 强制需求对齐文档
- 强制整体技术方案文档
- Stage 3 默认调度 `und-writing-plans`
- 强制实现计划确认后才能编码
- Stage 4 默认调度 `und-test-driven-development`
- 完成后必须做验收和 session 总结

#### Route C（完整流程）

适用：复杂需求、全局架构变更、高风险迁移、多阶段长链路任务

流程：

```text
需求对齐(gap scan) -> 设计(brainstorm/challenge) -> 实现计划 -> TDD 执行 -> 验收 -> 收尾
```

特点：

- `und-brainstorming` 必须执行：
  - Stage 1 做 requirements gap scan
  - Stage 2 做方案比较与 design challenge
- 设计阶段必须包含架构图、数据流图、实施流程图
- Stage 3 默认由 `und-writing-plans` 生成高可执行计划
- Stage 4 对 subagent candidate 优先评估 `und-subagent-driven-development`
- Stage 4 的默认 / fallback 路径仍由 `und-test-driven-development` 约束 red/green/refactor 执行
- 异常执行场景显式调度 `und-systematic-debugging`
- Stage 5 / completion claim 前显式调度 `und-verification-before-completion`
- 任务拆分为 10+ 可执行单元，支持并行
- 收尾阶段必须检查是否值得沉淀到 skill

### 3. 阶段门禁协议（Route B / Route C 强制）

Route B / Route C 都使用统一阶段状态机：

| 阶段 | 名称 | 必需产物 | 是否需要用户确认 |
|------|------|----------|------------------|
| Stage 0 | Repo Grounding | 当前代码事实记录 | 否 |
| Stage 1 | Requirements Alignment | `requirements-alignment.md` | 是 |
| Stage 2 | Technical Design | `design.md` | 是 |
| Stage 3 | Implementation Planning | `implementation-plan.md` | 是 |
| Stage 4 | TDD Execution | `progress-details.md` | 否 |
| Stage 5 | Acceptance | `acceptance.md` | 是 |
| Stage 6 | Session Closeout | `session-summary.md` | 是（治理询问） |

**方法型 skill 调度规则**：

- Route C 的 Stage 1：若需求存在遗漏风险、用户要求查漏、或后续设计需要多方案评估，调用 `und-brainstorming` 做 requirements gap scan
- Route C 的 Stage 2：调用 `und-brainstorming` 做候选方案比较与 design challenge，并把结果写入 `design.md`
- Route B / Route C 的 Stage 3：调用 `und-writing-plans` 生成 `implementation-plan.md`
- Route C 的 Stage 4：若 confirmed implementation step 已标记 `执行模式: subagent candidate`，且 capability detection / task eligibility / review contract 具备，先调用 `und-subagent-driven-development`
- Route B / Route C 的 Stage 4：默认调用 `und-test-driven-development` 执行 confirmed implementation step；若 `und-subagent-driven-development` 判定 fallback，也回到该默认路径
- Route B / Route C 的调试场景：出现 bug、flaky、回归或未知异常时，调用 `und-systematic-debugging`，并把证据写入 `progress-details.md`
- Route B / Route C 的 Stage 5 / completion claim 前：调用 `und-verification-before-completion`，确保 `acceptance.md` 记录 fresh verification evidence

**禁止越级规则**：

- 未完成 `requirements-alignment.md` 且未获得确认，不得创建 `design.md`。
- 未完成 `design.md` 且未获得确认，不得创建 `implementation-plan.md`。
- 未完成 `implementation-plan.md` 且未获得确认，不得开始代码编写。
- 未建立测试策略，不得进入实现。
- 未完成验收与总结，不得宣告任务完成。

### 3.1 显式确认信号协议（双重确定）

对 Stage 1 / Stage 2 / Stage 3 / Stage 5 / Stage 6 的推进，默认采用“双重确定”：

1. AI 必须先显式发起阶段确认，明确写出：
   - 当前阶段
   - 待进入阶段
   - 当前主文档
   - 等待用户确认的事项
   - 未确认前不会做什么
2. 用户必须使用带目标阶段名的明确确认语句回复，例如：
   - `确认进入设计阶段`
   - `确认进入实现计划阶段`
   - `确认开始编码`

以下表达不构成阶段确认：

- `继续`
- `好的`
- `按这个来`
- `先这样`
- 需求补充、约束纠偏、答疑澄清

收到有效确认后，AI 仍必须把确认证据写入当前阶段主文档或 `INDEX.md`，再推进到下一阶段。

### 4. Repo Grounding（设计前强制）

Route B / Route C 在出整体方案前，必须先结合当前代码做 grounding：

- 识别现有模块、入口、边界与关键约束
- 列出现状行为和计划改动点
- 将设计建立在真实代码结构上，而不是通用模板上

设计文档必须显式回答：

- 当前代码事实是什么
- 哪些模块会受影响
- 为什么选该方案而不是备选方案
- `und-brainstorming` 的 gap scan / challenge 结论是否已被吸收

### 5. Stage 4 执行协议

Route B / Route C 进入 Stage 4 后，默认调度 `und-test-driven-development`：

- 先写失败测试
- `Verify RED`
- 再写最小实现
- `Verify GREEN`
- 然后重构

Route C 在以下条件同时满足时，可先调度 `und-subagent-driven-development` 作为执行编排层：

- 当前步骤已在 `implementation-plan.md` 中标记 `执行模式: subagent candidate`
- 步骤边界、文件范围、`预期结果` 与 `Review Contract` 已写清
- 当前环境真实支持 child-agent / collab / review 能力

`und-subagent-driven-development` 只决定：

- 是否真的 dispatch subagent
- implementer status 如何处理
- spec compliance review 与 code quality review 如何排序
- 何时必须诚实 fallback 到主会话

它不替代默认执行方法：

- 若 capability detection 失败或步骤不适合 subagent，仍回到 `und-test-driven-development`
- 若执行过程中暴露未知异常，仍切到 `und-systematic-debugging`
- completion claim 前仍需 `und-verification-before-completion`

若某个步骤不适合严格 TDD，必须在 `implementation-plan.md` 中写明 `TDD 例外` 和替代验证，不能静默跳过。

出现以下信号时，不应继续盲修，而应显式调度 `und-systematic-debugging`：

- bug 原因未知
- flaky test 或间歇性失败
- 回归来源不清楚
- 多次修复尝试没有稳定收敛

### 6. Stage 5 验收与完成声明协议

在 Stage 5 或任何“任务已完成 / 已修复 / 已通过”的声明前，显式调度 `und-verification-before-completion`：

- 把 claim 映射到实际验证命令
- 读取完整输出和 exit code
- 用当前阶段 fresh verification evidence 支撑结论
- 若只能做 partial verification，必须明确写出缺口

### 7. 文档驱动进度追踪

跨 Chat 续接时，优先读取：

1. `INDEX.md`
2. `implementation-plan.md`
3. `progress-details.md`
4. `acceptance.md` / `session-summary.md`（若已存在）

恢复时必须向用户展示：

- 当前路由
- 当前阶段
- 已确认内容
- 未决问题
- 下一步唯一允许动作

### 8. 收尾与技能治理闭环

任务完成后，必须进入 Stage 6：

1. 生成 `session-summary.md`
2. 总结结果、偏差、遗留项和可复用经验
3. 识别是否存在值得沉淀的流程、失败模式或 checklist
4. 按 `skills-manager` 协议询问：`是否需要沉淀这次经验？`

若用户不确认更新 skill，也必须在 `session-summary.md` 记录治理结论。

## 详细流程说明

详细步骤、模板与检查清单请查阅 `knowledge/`：

- [知识索引](knowledge/index.md)
- [1. 复杂度评分详解](knowledge/1-complexity-scoring.md)
- [2. 路由决策逻辑](knowledge/2-route-decision.md)
- [4. Route B 标准流程](knowledge/4-route-b-standard-flow.md)
- [5. Route C 完整流程](knowledge/5-route-c-complete-flow.md)
- [6. 需求对齐流程](knowledge/6-requirements-alignment.md)
- [8. Brainstorm 协议](knowledge/8-brainstorm-protocol.md)
- [9. 任务分解策略](knowledge/9-task-breakdown.md)
- [10. 设计模板库](knowledge/10-design-templates.md)
- [11. 影响面分析](knowledge/11-impact-analysis.md)
- [12. 实现计划文档](knowledge/12-implementation-plan.md)
- [13. 进度追踪机制](knowledge/13-progress-tracking.md)
- [14. 错误恢复协议](knowledge/14-error-recovery.md)

## 与其他 Skills 的关系

- ✅ 与 `workspace-structure-manager` 互补：本 skill 管流程，后者管 session 载体
- ✅ 与 `skills-manager` 协作：任务完成后进入治理询问
- ✅ 调度 `und-brainstorming`：本 skill 决定何时需要查漏、方案比较或 design challenge
- ✅ 调度 `und-writing-plans`：本 skill 决定何时进入高可执行计划编写
- ✅ 调度 `und-subagent-driven-development`：本 skill 决定 Route C Stage 4 何时先进入 capability-aware orchestration
- ✅ 调度 `und-test-driven-development`：本 skill 决定何时进入 red/green/refactor 执行
- ✅ 调度 `und-systematic-debugging`：本 skill 决定何时从实现切到根因调查
- ✅ 调度 `und-verification-before-completion`：本 skill 决定何时提高 completion claim 的证据门槛
- ✅ 可选调用 `miravia-git`，但不依赖
- ❌ 不接管 `und-brainstorming` / `und-writing-plans` / `und-subagent-driven-development` / `und-test-driven-development` / `und-systematic-debugging` / `und-verification-before-completion` 的方法细节

## 最佳实践

1. 评分透明化：向用户展示评分、路由和阶段
2. 关键阶段必须确认：需求、设计、计划、验收、治理询问
3. 阶段推进默认使用双重确定，不把普通认可语句解释为 gate approval
4. 明确说出当前不会做什么，例如“在设计未确认前不会开始编码”
5. 所有重大决策都落进 session 文档，而不是只停留在聊天中
6. 发现复杂度变化时，显式升级或降级流程

## 限制与注意事项

- 评分模型仍是经验规则，需要人工校准
- Route B / Route C 会显著增加流程成本，不适合简单任务
- 跨 Chat 恢复依赖 `INDEX.md` 与实现文档的完整性
- TDD 是默认协议，不代表所有步骤都必须机械套用；但任何例外都必须显式记录
- 调试与 completion verification 是方法型 skill，不替代 Stage 5 / Stage 6 的确认门禁
- Route C 不代表必须新增独立 brainstorm 阶段文档；Phase 2 兼容方案下，brainstorm 结果默认写入 `requirements-alignment.md` / `design.md`

## 版本历史

- **v1.5.0** (2026-03-11)：接入 Phase 4 subagent orchestration 调度
  - 新增：Route C Stage 4 对 `und-subagent-driven-development` 的调度条件
  - 新增：`执行模式: subagent candidate`、capability detection、fallback 与 review contract 的主 skill 门禁语义
  - 调整：Stage 4 明确区分 orchestration layer 与默认 TDD 执行路径

- **v1.4.0** (2026-03-11)：接入 Phase 3 执行与验证层方法型 skill
  - 新增：Stage 4 的 `und-test-driven-development` 调度规则
  - 新增：异常执行场景的 `und-systematic-debugging` 调度规则
  - 新增：Stage 5 / completion claim 前的 `und-verification-before-completion` 调度规则
  - 调整：主 skill 只保留 dispatch / gate，不再拥有完整 TDD / debugging / verification 方法细节

- **v1.3.0** (2026-03-11)：接入 Phase 2 方法型 skill 调度
  - 新增：Route C 的 `und-brainstorming` 调度规则（gap scan / design challenge）
  - 新增：Stage 3 的 `und-writing-plans` 调度规则
  - 强化：主 skill 只负责“何时调用”，不再拥有完整 brainstorming / planning 方法细节

- **v1.2.0** (2026-03-10)：新增双重确定门禁协议
  - 新增：显式确认信号协议（双重确定）
  - 强化：只有带目标阶段名的明确确认语句才允许推进阶段
  - 强化：确认通过后必须补记确认证据到主文档或 `INDEX.md`

- **v1.1.0** (2026-03-10)：重构为硬门禁工作流
  - 修正：复杂度评分区间与 Route 阈值的数学错误
  - 新增：Route B / Route C 阶段门禁协议
  - 新增：Repo Grounding、TDD、Acceptance、Session Closeout
  - 新增：与 `skills-manager` 的收尾治理闭环

- **v1.0.2** (2026-03-10)：新增技能识别防漏协议
  - 新增：首轮技能识别协议（命中 skill / 使用顺序 / 跳过理由）
  - 新增：复杂度预检清单（显式点名 + 多阶段链路 + 续接需求）
  - 新增：最小覆盖集原则，降低漏触发

- **v1.0.1** (2026-03-10)：优化触发条件
  - 精细化排除规则：只排除"原子级单文件修改"
  - 添加"仍然适用的场景"说明，防止误判
  - 修复：用户提供详细计划时仍应触发 skill

- **v1.0.0** (2026-03-09)：初始版本
  - 5 因子复杂度评分模型
  - 三层流程路由（Route A/B/C）
  - Brainstorm 方案评估
  - 任务分解与进度追踪
  - 错误恢复机制（4 层策略）
