# Complex Task Solver - 知识索引

## 快速导航

本知识库包含 Complex Task Solver skill 的完整实现细节，所有文档都是自包含的，无需依赖外部 skills。

### 核心机制

- [**1. 复杂度评分详解**](1-complexity-scoring.md) - 5 因子评分系统完整说明
- [**2. 路由决策逻辑**](2-route-decision.md) - 路由决策逻辑和强制规则

### 三层流程完整实现

- [**3. Route A 快速流程**](3-route-a-fast-flow.md) - Route A 完整流程（需求理解 → 实现 → 验证）
- [**4. Route B 标准流程**](4-route-b-standard-flow.md) - Route B 完整流程（需求对齐 → 设计 → 实现）
- [**5. Route C 完整流程**](5-route-c-complete-flow.md) - Route C 完整流程（Brainstorm → 分解 → 并行执行）

### 支撑流程

- [**6. 需求对齐流程**](6-requirements-alignment.md) - 需求对齐详细流程（5 维判断清单）
- [**7. 完整性检查清单**](7-completeness-checklist.md) - 24 项完整性检查清单（6W2H + 风险 + 影响）
- [**8. Brainstorm 协议**](8-brainstorm-protocol.md) - Brainstorm 完整流程（2-3 方案评估）

### 执行支撑

- [**9. 任务分解策略**](9-task-breakdown.md) - 任务分解策略和算法
- [**10. 设计模板库**](10-design-templates.md) - Mermaid 模板库（架构图/数据流图/流程图）
- [**11. 影响面分析**](11-impact-analysis.md) - 影响面分析模板

### 进度和恢复

- [**12. 实现计划文档**](12-implementation-plan.md) - 实现计划文档结构
- [**13. 进度追踪机制**](13-progress-tracking.md) - 进度追踪和跨 Chat 支持
- [**14. 错误恢复协议**](14-error-recovery.md) - 错误恢复协议（4 层机制）

---

## 文档使用指南

### 初学者路径

如果你是第一次使用 Complex Task Solver，建议按以下顺序阅读：

1. **理解评分** → [1. 复杂度评分详解](1-complexity-scoring.md)
2. **理解路由** → [2. 路由决策逻辑](2-route-decision.md)
3. **学习流程** → [3/4/5. Route A/B/C 流程](3-route-a-fast-flow.md)
4. **探索工具** → [9/10/11. 分解/设计/分析](9-task-breakdown.md)

### 问题解决路径

遇到具体问题时的快速查找：

| 问题 | 参考文档 |
|------|----------|
| 不确定用哪个流程？ | [2. 路由决策逻辑](2-route-decision.md) |
| 需求不清晰？ | [6. 需求对齐流程](6-requirements-alignment.md) |
| 不知道如何拆分任务？ | [9. 任务分解策略](9-task-breakdown.md) |
| 需要画架构图？ | [10. 设计模板库](10-design-templates.md) |
| 实施遇到错误？ | [14. 错误恢复协议](14-error-recovery.md) |
| 需要跨 Chat 继续？ | [13. 进度追踪机制](13-progress-tracking.md) |

### 高级用户路径

如果你想深入优化使用方式：

- **完整性保障** → [7. 完整性检查清单](7-completeness-checklist.md)
- **方案评估** → [8. Brainstorm 协议](8-brainstorm-protocol.md)
- **影响评估** → [11. 影响面分析](11-impact-analysis.md)
- **进度管理** → [12. 实现计划文档](12-implementation-plan.md)

---

## 设计原则

所有知识文档遵循以下原则：

1. **自包含性**：每个文档都可独立阅读和使用
2. **完整性**：包含完整的检查清单、模板和示例
3. **可执行性**：提供明确的步骤和判断标准
4. **图文并茂**：使用 Mermaid 图表辅助理解

---

## 版本说明

- **当前版本**：v1.0.0
- **最后更新**：2026-03-09
- **维护者**：Complex Task Solver Team
