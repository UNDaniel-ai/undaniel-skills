# 13. 进度追踪机制

## 概述

进度追踪用于回答两个问题：

1. 任务现在走到哪个阶段了？
2. 下一步唯一允许做什么？

在硬门禁工作流下，进度追踪不只更新 `implementation-plan.md`，还必须同步 `INDEX.md` 和 `progress-details.md`。Phase 3 起，`progress-details.md` 还承担 debugging evidence 载体，而 `acceptance.md` 需要承载 fresh verification evidence。Phase 4 起，`progress-details.md` 还必须承载 subagent dispatch、review loop 与 fallback 事实。

## 追踪对象

- 当前路由
- 当前阶段
- 当前步骤
- 当前执行模式
- 已确认文档
- 未决问题
- 动态子任务
- subagent dispatch / review 状态
- 是否允许编码
- 是否允许宣告完成

## 文档职责

| 文档 | 职责 |
|------|------|
| `INDEX.md` | 显示当前阶段、门禁状态、下一步允许动作 |
| `implementation-plan.md` | 记录步骤级计划与状态 |
| `progress-details.md` | 记录真实执行、TDD 循环、subagent dispatch / fallback、根因证据与恢复动作 |
| `acceptance.md` | 记录验收进度与 completion claim 对应 evidence |
| `session-summary.md` | 记录收尾与治理状态 |

## 更新时机

### 必须更新 `INDEX.md`

- 进入新阶段
- 完成需求 / 设计 / 计划确认
- 开始编码
- 完成验收
- 进入收尾

### 必须更新 `implementation-plan.md`

- 步骤状态变化
- 新增动态子任务
- 依赖关系调整
- 执行模式或 review contract 变化

### 必须更新 `progress-details.md`

- 执行某个 TDD 步骤
- 发生 subagent dispatch、re-dispatch 或 fallback
- 出现阻塞
- 发生回退或恢复
- 进入系统化 debugging
- 形成新的根因假设或验证结论

### 必须更新 `acceptance.md`

- 开始 Stage 5 验收
- 新增或更新 completion claim
- 运行 fresh verification evidence
- 发现只能做 partial verification

## 跨 Chat 恢复

新 chat 恢复时，按下面顺序读取：

1. `INDEX.md`
2. `implementation-plan.md`
3. `progress-details.md`
4. `acceptance.md` / `session-summary.md`

恢复后必须向用户展示：

- 当前路由
- 当前阶段
- 当前执行模式
- 已确认项
- 当前阻塞
- 下一步允许动作

## 恢复示例

```markdown
我发现你有一个正在进行的任务：用户权限管理功能。

当前状态：
- 路由：Route B
- 当前阶段：Stage 3 Implementation Planning
- 当前执行模式：主会话
- 已确认：requirements-alignment.md、design.md
- 未确认：implementation-plan.md

下一步允许动作：
- 继续细化并确认实现计划

当前不会做什么：
- 在实现计划确认前不会开始编码
```

## 最佳实践

1. 所有关键状态都以文档为准，不以聊天记忆为准
2. 每次恢复都明确说出“当前不会做什么”
3. 若阶段被打回，立即在 `INDEX.md` 更新阻塞原因
4. 动态子任务要写入计划，而不是只写在聊天里
5. 调试证据优先写 `progress-details.md`，不要散落在临时消息里
6. completion claim 的 fresh evidence 优先写 `acceptance.md`
7. 若宣称使用 subagent，必须在 `progress-details.md` 写明 dispatch、status、review 与 fallback 事实

## 参考资料

- [12. 实现计划文档](12-implementation-plan.md)
- [14. 错误恢复协议](14-error-recovery.md)
