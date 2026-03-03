# 会话目录与 INDEX.md 最小规范

## 会话目录命名
- git 项目内：`<git_root>/temp/sessions/YYYY-MM-DD-HHMM-keywords/`
- 非 git 项目：`~/Developer/sessions/YYYY-MM-DD-HHMM-keywords/`
- keywords：2-3 个关键词，使用短横线连接

## INDEX.md 最小模板
```markdown
# 会话主线 INDEX

**创建时间**：YYYY-MM-DD HH:MM
**最后更新**：YYYY-MM-DD HH:MM

## 核心诉求
- 

## 验收标准
- 

## 任务概览
- 

## 需求背景
- 

## 分析主线
- 

## 文档关系图
- [INDEX.md](INDEX.md) - 主线文档
- [requirements-alignment.md](requirements-alignment.md) - 需求对齐
- [comprehensive-discussion.md](comprehensive-discussion.md) - 全面讨论
- [design.md](design.md) - 设计输出
- [impact-analysis.md](impact-analysis.md) - 影响面分析
- [confirmation.md](confirmation.md) - 用户确认
- [implementation-plan.md](implementation-plan.md) - 实现计划
- [error-recovery.md](error-recovery.md) - 错误恢复
- [change-log.md](change-log.md) - 变更记录
- [progress-details.md](progress-details.md) - 详细进度
- [handoff.md](handoff.md) - 交接信息
- [activity-log.md](activity-log.md) - 活动记录

## 当前进度
- 总体进度：
- 关键里程碑：

## 当前状态
- 

## 剩余工作
- 

## 下一步
- 

## 阻塞/风险
- 

## 关键决策
- 

## 图示状态
- 改动前图：
- 改动后图：

## 相关资源
- 
```

## 双向链接规则
- INDEX.md 指向所有会话文档。
- 其他文档开头必须包含：`[← 返回主线文档](INDEX.md)`。

## 内容限制规则
- **任务概览**：最多 5 行
- **需求背景**：最多 3 句话
- **分析主线**：最多 5 个要点
- **文档关系图**：只列出核心文档（最多 10 个）
- **当前进度**：总体进度最多 5 行，关键里程碑最多 5 个
- **关键决策**：最多 5 个，每个 1-2 句话
- **相关资源**：最多 10 个
- 详细信息分离到独立文档（progress-details.md、activity-log.md 等）
