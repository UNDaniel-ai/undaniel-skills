# Workspace Structure Manager - 知识库索引

本知识库包含 workspace-structure-manager skill 的详细文档,涵盖核心概念、操作流程、模板和最佳实践。

## 📚 知识库结构

### 核心概念与原理

1. **[核心概念](1-core-concepts.md)** (约 200 行)
   - 工作目录分离理念
   - 主线文档系统
   - 自动化执行原则
   - 与其他 skills 的关系

### 操作流程

2. **[Session 管理](2-session-management.md)** (约 300 行)
   - Session 创建流程
   - 命名规则和关键词提取
   - Session 切换和继续
   - Session 生命周期管理

3. **[INDEX.md 结构与管理](3-index-structure.md)** (约 450 行)
   - INDEX.md 标准结构
   - 各章节详细说明
   - 更新规则和时机
   - 内容限制规则

4. **[文档模板库](4-document-templates.md)** (约 550 行)
   - 所有文档模板详细说明
   - 需求分析阶段模板
   - 设计阶段模板
   - 实现阶段模板
   - 错误恢复模板

### 高级功能

5. **[子任务管理](5-sub-task-management.md)** (约 550 行)
   - 子任务触发条件
   - 子任务目录结构
   - 子任务文档模板
   - 子任务进度追踪
   - 子任务切换和完成

6. **[多项目改动追踪](6-multi-project-tracking.md)** (约 420 行)
   - 项目识别机制
   - 改动文件追踪
   - INDEX.md 记录格式
   - 提交前检查清单
   - Submodule 处理

### 维护与优化

7. **[文档清理策略](7-cleanup-strategy.md)** (约 200 行)
   - 清理触发条件
   - 重要 session vs 临时 session
   - 归档策略
   - 用户确认流程
   - 清理清单模板

8. **[最佳实践](8-best-practices.md)** (约 150 行)
   - 常见场景处理
   - 反模式和陷阱
   - 性能优化建议
   - 与用户交互的最佳实践
   - 故障排除指南

## 🎯 快速导航

### 按使用场景导航

**我想了解基本概念**:
→ 阅读 [核心概念](1-core-concepts.md)

**我想开始一个新任务**:
→ 阅读 [Session 管理](2-session-management.md) - Session 创建流程

**我想了解 INDEX.md 如何组织**:
→ 阅读 [INDEX.md 结构与管理](3-index-structure.md)

**我想知道有哪些文档模板**:
→ 阅读 [文档模板库](4-document-templates.md)

**我的任务很复杂,需要分解**:
→ 阅读 [子任务管理](5-sub-task-management.md)

**我改动了多个项目**:
→ 阅读 [多项目改动追踪](6-multi-project-tracking.md)

**我想清理旧的 session**:
→ 阅读 [文档清理策略](7-cleanup-strategy.md)

**我想了解常见场景如何处理**:
→ 阅读 [最佳实践](8-best-practices.md)

### 按角色导航

**如果你是 Agent**:
1. 必读: [核心概念](1-core-concepts.md) - 理解设计理念
2. 必读: [Session 管理](2-session-management.md) - 如何创建和管理 session
3. 必读: [INDEX.md 结构与管理](3-index-structure.md) - 如何维护主线文档
4. 常用: [文档模板库](4-document-templates.md) - 创建文档时参考
5. 按需: [子任务管理](5-sub-task-management.md)、[多项目改动追踪](6-multi-project-tracking.md)、[文档清理策略](7-cleanup-strategy.md)

**如果你是用户**:
1. 推荐: [核心概念](1-core-concepts.md) - 了解这个 skill 做什么
2. 推荐: [最佳实践](8-best-practices.md) - 了解如何更好地与 Agent 协作
3. 按需: 其他文档根据需要查阅

**如果你是 Skill 维护者**:
- 通读所有文档,理解完整设计
- 重点关注 [核心概念](1-core-concepts.md) 和 [最佳实践](8-best-practices.md)

## 📊 文档概览

| 文档 | 行数 | 重要性 | 主要内容 |
|------|------|--------|----------|
| [核心概念](1-core-concepts.md) | ~200 | ⭐⭐⭐⭐⭐ | 设计理念、核心原则 |
| [Session 管理](2-session-management.md) | ~300 | ⭐⭐⭐⭐⭐ | Session 创建、命名、切换 |
| [INDEX.md 结构](3-index-structure.md) | ~450 | ⭐⭐⭐⭐⭐ | INDEX.md 详细结构 |
| [文档模板库](4-document-templates.md) | ~550 | ⭐⭐⭐⭐ | 所有文档模板 |
| [子任务管理](5-sub-task-management.md) | ~550 | ⭐⭐⭐ | 大型任务管理 |
| [多项目追踪](6-multi-project-tracking.md) | ~420 | ⭐⭐⭐ | 多项目改动识别 |
| [清理策略](7-cleanup-strategy.md) | ~200 | ⭐⭐ | 文档清理和归档 |
| [最佳实践](8-best-practices.md) | ~150 | ⭐⭐⭐⭐ | 常见场景和技巧 |

**总计**: 约 2,820 行

## 🔄 文档更新历史

- **2026-03-09**: 初始版本,改编自 Codea workspace-management Rule
  - 创建所有核心文档
  - 适配到 Claude Code 环境

## 💡 如何贡献

如发现文档错误或有改进建议:
1. 提交 Issue 到 lulu-skills-common 仓库
2. 或直接提交 Pull Request
3. 联系 skill 维护者

## 📖 相关资源

- **主 SKILL.md**: [../SKILL.md](../SKILL.md)
- **Codea 原始 Rule**: workspace-management.mdc (参考)
- **其他相关 Skills**: complex-task-solver, miravia-git, skills-manager
