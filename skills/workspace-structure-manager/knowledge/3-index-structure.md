# INDEX.md 结构与管理

> INDEX.md 是 session 的控制面板。它既是导航入口，也是当前门禁状态的单一事实来源。

[← 上一篇: Session 管理](2-session-management.md) | [返回知识库索引](index.md) | [下一篇: 文档模板库 →](4-document-templates.md)

## 标准模板

```markdown
# {任务名称}

**创建时间**: YYYY-MM-DD HH:mm
**最后更新**: YYYY-MM-DD HH:mm
**当前路由**: Route B / Route C
**当前阶段**: Stage X [名称]

## 📋 任务概览

[最多 5 行，简述目标和范围]

## 🎯 需求理解状态

- **核心目标**：[1-2 句话]
- **范围状态**：已确认 / 待确认
- **验收标准状态**：已确认 / 待确认
- **主文档**：[requirements-alignment.md](requirements-alignment.md)

## 🏗️ 技术方案状态

- **方案状态**：未开始 / 讨论中 / 已确认
- **设计主线**：[1-3 条]
- **主文档**：[design.md](design.md)

## 🧭 阶段状态表

| 阶段 | 状态 | 主文档 | 是否已确认 |
|------|------|--------|------------|
| Requirements Alignment | ✅ / 🚧 / ⏳ | `requirements-alignment.md` | 是 / 否 |
| Technical Design | ✅ / 🚧 / ⏳ | `design.md` | 是 / 否 |
| Implementation Planning | ✅ / 🚧 / ⏳ | `implementation-plan.md` | 是 / 否 |
| TDD Execution | ✅ / 🚧 / ⏳ | `progress-details.md` | 不适用 |
| Acceptance | ✅ / 🚧 / ⏳ | `acceptance.md` | 是 / 否 |
| Session Closeout | ✅ / 🚧 / ⏳ | `session-summary.md` | 是 / 否 |

## 🚦 门禁状态

- **下一步允许动作**：[唯一允许动作]
- **阻塞原因**：[如无则写 无]
- **是否允许编码**：是 / 否
- **是否允许宣告完成**：是 / 否

## 📂 文档关系图

- [INDEX.md](INDEX.md)
- [requirements-alignment.md](requirements-alignment.md)
- [design.md](design.md)
- [implementation-plan.md](implementation-plan.md)
- [progress-details.md](progress-details.md)
- [acceptance.md](acceptance.md)
- [session-summary.md](session-summary.md)

## 📊 实现与进度

- **计划状态**：未开始 / 进行中 / 已确认
- **当前执行步骤**：[步骤名称]
- **详细进度**：见 [progress-details.md](progress-details.md)

## ✅ 关键决策

1. [决策 1]
2. [决策 2]

## 🔚 收尾与治理

- **验收状态**：未开始 / 进行中 / 已确认
- **总结状态**：未开始 / 进行中 / 已完成
- **治理状态**：未评估 / 已询问 / 无需沉淀 / 待确认 / 已完成
```

## 核心规则

### INDEX.md 必须能回答的问题

- 我们现在在哪个阶段？
- 哪些内容已经确认？
- 下一步唯一允许做什么？
- 现在是否允许编码？
- 现在是否允许宣告完成？

### INDEX.md 必须同步更新的时机

- 切换阶段时
- 用户确认需求 / 设计 / 计划时
- 开始编码时
- 完成验收时
- 完成总结和治理询问时

### INDEX.md 不应承载的内容

- 详细设计细节
- 大段讨论记录
- 长篇测试结果

这些内容应放入对应阶段文档，INDEX 只保留状态和入口。

## 最佳实践

1. `当前阶段` 与 `门禁状态` 必须始终同步
2. `下一步允许动作` 最好写成唯一动作，避免并发歧义
3. 任何阶段被打回，都要更新 `阻塞原因`
