# 8. Brainstorm 协议

## 概述

Phase 2 起，Brainstorm 不再只是“列 2-3 个方案”。它统一由 `und-brainstorming` 承担，主要有 3 种模式：

1. requirements gap scan
2. option comparison
3. design challenge

## 何时使用 `und-brainstorming`

### 必须使用

- ✅ Route C 的 `requirements-alignment.md` 需要查漏补缺
- ✅ Route C 的 `design.md` 需要候选方案比较
- ✅ Route C 的设计在确认前需要完整度 / 回滚 / 测试性 challenge
- ✅ 用户明确要求 brainstorm、challenge、查漏、方案比较

### 可退化使用

- ☑ 只有明显遗漏风险时，只做 gap scan
- ☑ 方案已经基本确定时，只做 design challenge

### 不需要使用

- ❌ 原子任务且实现路径唯一
- ❌ 已进入已确认的 `implementation-plan.md` 或编码执行阶段
- ❌ 用户明确不需要 alternatives 或 challenge

## 三种模式

### 模式 1：Requirements Gap Scan

目标：
- 检查 `requirements-alignment.md` 是否遗漏关键信息

必须覆盖：
- 目标是否可执行
- 范围是否过宽 / 过窄
- 约束是否缺失
- 验收标准是否可验证
- 未决问题是否被显式记录

输出格式建议：

```markdown
## Requirements Gap Scan

### 已确认
- [确认项 1]

### 可能遗漏
- [遗漏点 1]
- [遗漏点 2]

### 需要补充确认
1. [问题 1]
2. [问题 2]
```

硬规则：
- 输出问题和风险，不直接替用户拍板

### 模式 2：Option Comparison

目标：
- 在设计前比较 2-3 个有意义的候选方案

方案多样性至少覆盖一个维度：
- 风险等级
- 实施时间
- 技术路线
- 兼容性 / 回滚策略

输出格式建议：

```markdown
## Brainstorm 总结

### 方案 1: [名称]
- 思路：[描述]
- 优点：[...]
- 缺点：[...]
- 风险：[高/中/低]
- 成本：[...]

### 方案 2: [名称]
...

## AI 推荐
- 建议选择：[方案]
- 理由：[理由]
```

### 模式 3：Design Challenge

目标：
- 对当前设计做反证式检查，而不是只补正向细节

必须 challenge：
- 是否遗漏备选方案
- 是否遗漏回滚策略
- 是否遗漏兼容性边界
- 是否遗漏验证路径
- 是否遗漏风险关闭动作

输出格式建议：

```markdown
## Design Challenge / Completeness Review

- [检查项 1] -> [结论]
- [检查项 2] -> [结论]

### 仍待解决
- [问题 1]
- [问题 2]
```

## 推荐执行顺序

### 在 Stage 1

```text
requirements-alignment.md
  -> requirements gap scan
  -> 补待确认项
  -> 再请求用户确认
```

### 在 Stage 2

```text
design.md
  -> option comparison
  -> AI recommendation
  -> design challenge
  -> 再请求用户确认
```

## Collaboration Boundaries

- `complex-task-solver` 决定何时必须调用此协议
- `workspace-structure-manager` 决定结果写入哪份门禁文档
- `und-brainstorming` 提供方法，不拥有阶段门禁 owner 身份

## 常见错误

- 把 Brainstorm 等同于“随便发散几个点子”
- requirements 没查漏就直接写设计
- 只做方案推荐，不做 design challenge
- challenge 只写“有风险”，不指出缺什么
- 生成独立 brainstorm 文档，反而绕开正式门禁文档

## 参考资料

- [5. Route C 完整流程](5-route-c-complete-flow.md)
- [6. 需求对齐流程](6-requirements-alignment.md)
- [10. 设计模板库](10-design-templates.md)
