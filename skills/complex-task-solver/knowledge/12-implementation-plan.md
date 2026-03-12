# 12. 实现计划文档

## 概述

`implementation-plan.md` 是 Route B / Route C 在编码前的最后一道门禁文档。Phase 2 起，它默认由 `und-writing-plans` 负责质量约束；Phase 3 起，它还必须能承载 `und-test-driven-development` 的 red/green 纪律；Phase 4 起，Route C 计划还必须表达 subagent execution overlay 是否适用，以及 fallback / review contract 如何落地。

它的作用不是“列 TODO”，而是把设计转成可执行、可确认、可恢复的步骤合同。

## 门禁规则

- 未完成 `implementation-plan.md` 且未获得确认，不得开始代码编写
- 未写测试策略，不得进入实现
- 每个重要步骤都必须有输入、验证方式和输出契约
- 需要严格 TDD 的步骤，必须显式体现 `Verify RED / Verify GREEN`
- 不适合严格 TDD 的步骤，必须显式记录例外原因
- 若步骤可能走 subagent orchestration，必须显式写出 `执行模式`、`Subagent Eligibility` 和 `Review Contract`

## `预期结果` 的定义

`预期结果` 是步骤级 postcondition。

它必须回答：
- 做完这一步后，外部可观察到什么变化
- 新增了什么 artifact、行为、规则或验证能力
- reviewer 通过什么结果能判断“这一步真的完成了”

它不能只是：
- “完成该步骤”
- “实现功能”
- 与 `Step Acceptance` 完全重复的笼统表述

## 文档结构

```markdown
# 实现计划：[任务名称]

[← 返回 INDEX.md](INDEX.md)

**创建时间**: YYYY-MM-DD HH:mm
**当前路由**: Route B / Route C
**当前阶段**: Stage 3 Implementation Planning

## 计划概览

- **目标**：[总体目标]
- **策略**：[总体策略]
- **测试策略**：[如何做 TDD / 哪些例外]
- **总体依赖**：[关键依赖]

## 步骤列表

### 步骤 1: [步骤名称]
- **状态**：⏳ 待开始 / 🚧 进行中 / ✅ 已完成
- **优先级**：P0 / P1 / P2
- **依赖**：[依赖步骤]
- **前置输入**：
  - [输入 1]
  - [输入 2]
- **文件范围**：
  - [文件 1]
  - [文件 2]
- **执行模式**：主会话 / subagent candidate / 强制主会话
- **Subagent Eligibility**：
  - [为何适合 / 不适合 subagent]
- **Review Contract**：spec only / spec + quality / fallback checklist
- **Failing Test**：
  - [ ] 测试 1
  - [ ] 测试 2
- **Verify RED**：
  - [ ] RED 证据 1
- **Minimal Implementation**：
  - [ ] 实现动作 1
  - [ ] 实现动作 2
- **Verify GREEN**：
  - [ ] GREEN 证据 1
- **验证命令**：
  - [ ] 命令 1
  - [ ] 命令 2
- **预期结果**：
  - [ ] 可观察结果 1
  - [ ] 可观察结果 2
- **Refactor**：
  - [ ] 重构动作 1
  - [ ] 重构动作 2
- **Step Acceptance**：
  - [ ] 验收点 1
  - [ ] 验收点 2
- **并行边界**：[可并行 / 必须串行 / 依赖说明]
- **TDD 例外**：[若无则写 无]

## 动态子任务

- **子任务 A**：[描述]
- **子任务 B**：[描述]

## 用户确认

- [ ] 用户已确认步骤顺序
- [ ] 用户已确认测试策略
- [ ] 用户已确认 `预期结果` 作为步骤级输出契约
- [ ] 可以进入编码阶段
```

## 核心字段说明

| 字段 | 说明 |
|------|------|
| 当前路由 | Route B 或 Route C |
| 当前阶段 | 固定为 Implementation Planning |
| 前置输入 | 开始该步骤前必须成立的条件 |
| 文件范围 | 该步骤预计会修改的文件 |
| 执行模式 | 当前步骤是主会话、subagent candidate 还是强制主会话 |
| Subagent Eligibility | 解释为什么适合 / 不适合 subagent orchestration |
| Review Contract | 规定 spec only、spec + quality 或 fallback checklist |
| 验证命令 | 执行完后如何检验 |
| 预期结果 | 该步骤完成后的外部可观察状态 |
| Step Acceptance | 可以关闭该步骤的最终条件 |
| Verify RED | 如何证明目标测试确实先失败 |
| Verify GREEN | 如何证明目标测试已转绿 |
| TDD 例外 | 不适合 TDD 时的显式理由 |

## 示例

```markdown
### 步骤 3: 接入 `und-writing-plans`
- **状态**：⏳ 待开始
- **优先级**：P0
- **依赖**：步骤 2
- **前置输入**：
  - `design.md` 已确认
  - `complex-task-solver` 已明确 Stage 3 需要独立 planning skill
- **文件范围**：
  - `skills/und-writing-plans/SKILL.md`
  - `skills/complex-task-solver/knowledge/12-implementation-plan.md`
- **执行模式**：主会话
- **Subagent Eligibility**：
  - 当前步骤是 planning contract authoring，不适合 subagent dispatch
- **Review Contract**：spec only
- **Failing Test**：
  - [ ] 当前仓不存在 `und-writing-plans`
  - [ ] 现有 implementation plan knowledge 未显式要求 `预期结果`
- **Verify RED**：
  - [ ] 当前模板还不能表达 red proof
- **Minimal Implementation**：
  - [ ] 新建 `und-writing-plans`
  - [ ] 写清 `预期结果` 定义与步骤级约束
- **Verify GREEN**：
  - [ ] 新模板能表达 green proof
- **验证命令**：
  - [ ] `tools/skillctl validate --skill und-writing-plans`
- **预期结果**：
  - [ ] 新 skill 通过校验
  - [ ] 计划文档约束中明确出现 `前置输入 / 验证命令 / 预期结果`
- **Refactor**：
  - [ ] 删除与主 skill 重复的 planning 所有权表述
- **Step Acceptance**：
  - [ ] skill contract 清晰且通过 validator
- **并行边界**：必须在模板升级前完成
- **TDD 例外**：无
```

## 最佳实践

1. 每一步都写成“可测试的最小增量”
2. 优先表达依赖关系，而不是按文件堆叠任务
3. 明确哪些步骤可以并行，哪些必须串行
4. 用 `预期结果` 区分“目标”与“完成后的可观察状态”
5. 用 `Verify RED / Verify GREEN` 区分 TDD 证据与普通验证命令
6. 用 `Step Acceptance` 区分“结果存在”与“步骤可关闭”
7. Route C 的 subagent candidate 步骤必须写清 eligibility 与 review contract，避免 Stage 4 口号化

## 参考资料

- [4. Route B 标准流程](4-route-b-standard-flow.md)
- [5. Route C 完整流程](5-route-c-complete-flow.md)
- [13. 进度追踪机制](13-progress-tracking.md)
