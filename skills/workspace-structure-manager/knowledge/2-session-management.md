# Session 管理

> 说明如何创建、续用和关闭一个 session。

[← 上一篇: 核心概念](1-core-concepts.md) | [返回知识库索引](index.md) | [下一篇: INDEX.md 结构 →](3-index-structure.md)

## Session 概念

Session 是某个开发任务的临时工作目录。Route B / Route C 的所有主产物都应放在同一个 session 里，保证任务状态可恢复、可审计、可清理。

## 标准目录结构

```text
temp/sessions/{session-name}/
├── INDEX.md
├── requirements-alignment.md
├── design.md
├── impact-analysis.md          # Route C 必备，Route B 视情况
├── implementation-plan.md
├── progress-details.md
├── acceptance.md
├── session-summary.md
├── confirmation.md            # 可选补充
└── sub-task-01-xxx/           # 可选
```

## 创建条件

创建新 session 的典型场景：

- 新开发任务开始
- 当前没有活跃 session
- 当前任务与现有 session 无关

续用已有 session 的典型场景：

- 用户说“继续之前的工作”
- 检测到已有未完成 session
- 用户明确指定某个 session

## 创建步骤

1. 提取 2-3 个关键词
2. 生成 session 名称 `YYYY-MM-DD-HHMM-{keywords}`
3. 创建目录
4. 初始化 `INDEX.md`
5. 按当前阶段创建需要的文档

## 命名建议

| 用户消息 | Session 名称 |
|---------|-------------|
| 添加用户登录功能 | `2026-03-10-1030-add-user-login` |
| 重构数据库访问层 | `2026-03-10-1100-refactor-database` |
| 修复 API 认证 bug | `2026-03-10-1130-fix-api-auth` |

## Route B / Route C 的最小文档集合

### Stage 1 前后

- `INDEX.md`
- `requirements-alignment.md`

### Stage 2 / 3 前后

- `design.md`
- `implementation-plan.md`

### 执行与收尾

- `progress-details.md`
- `acceptance.md`
- `session-summary.md`

## 续用 session 的恢复顺序

1. 读取 `INDEX.md`
2. 判断当前阶段与门禁状态
3. 打开该阶段对应主文档
4. 恢复下一步允许动作

## 关闭 session 前的检查

- `INDEX.md` 是否已更新为最终状态
- `acceptance.md` 是否已完成
- `session-summary.md` 是否已写好
- 是否已经记录治理结论

## 最佳实践

1. Session 名称要反映任务，而不是反映某一次临时动作
2. 同一任务不要分裂成多个并行 session
3. 恢复时先看 `INDEX.md`，不要直接跳进零散文档
