---
name: workspace-structure-manager
description: 工作区文件夹结构管理 - 自动管理临时文档、主线文档和工作目录,防止项目根目录混乱
homepage: https://github.com/lulu-skills-common
metadata:
  emoji: "📁"
  category: "workspace-management"
  version: "1.0.0"
  standalone: false
  adapts_from: "Codea workspace-management Rule"
---

# Workspace Structure Manager

> 规范化 Agent 的文件夹结构管理,防止项目目录混乱

## 概述

Workspace Structure Manager 是一个专门用于管理工作区文件夹结构的 skill,核心能力包括:

- **自动工作目录管理** - `temp/sessions/{session}/` 自动创建和管理
- **INDEX.md 主线文档系统** - 任务导航中心,维护任务概览和进度
- **文档模板库** - requirements、design、impact-analysis 等标准模板
- **子任务管理** - 大型任务的结构化管理机制
- **多项目改动追踪** - 识别所有改动的项目和文件
- **文档清理和归档策略** - 防止临时文档膨胀

## 核心原则

### 1. 分离临时与永久

**临时工作文档** → `temp/sessions/{session}/`
- 需求分析文档
- 设计文档
- 实现计划
- 进度追踪文档
- 错误恢复记录

**项目永久文档** → `docs/`, `README.md` 等
- 项目说明文档
- API 文档
- 架构设计文档
- 用户手册

### 2. 主线文档中心

**每个 session 必须有 INDEX.md**:
- 任务概览 - 目标、背景、成功标准
- 分析主线 - 核心分析思路(最多 5 个要点)
- 文档关系图 - 所有相关文档的导航(带双向链接)
- 当前进度 - 总体进度、关键里程碑
- 关键决策 - 重要技术决策记录

**保持简洁**:
- INDEX.md 只包含核心信息
- 详细内容分离到独立文档
- 使用双向链接建立文档关系

### 3. 自动化执行

**Agent 自动执行,无需用户干预**:
- 检测新任务时自动创建 session 目录
- 创建临时文档时自动保存到当前 session
- 任务进展时自动更新 INDEX.md
- 提交代码前自动识别多项目改动

**灵活适配**:
- 尊重用户明确指定的路径
- 不强制覆盖用户创建的文档
- 可以切换或继续之前的 session

## 触发场景

### ✅ 自动触发(无需用户指定)

**场景 1: 新任务开始**
- 用户描述了一个新的开发任务
- 自动创建 session 目录和 INDEX.md
- 示例: "帮我添加用户登录功能"

**场景 2: 创建临时文档**
- 需要创建需求分析、设计文档等临时文档
- 自动保存到当前 session 目录
- 示例: 创建 requirements-alignment.md

**场景 3: 任务进展更新**
- 完成某个里程碑或关键步骤
- 自动更新 INDEX.md 的进度和状态
- 示例: 设计完成,开始实现

**场景 4: 提交代码前**
- 执行 git commit 前
- 自动识别改动的项目和文件
- 在 INDEX.md 中记录改动清单

### ❌ 不触发

**场景 1: 用户明确指定路径**
- 用户说"在 docs/ 下创建 xxx.md"
- 遵循用户指示,不改变路径

**场景 2: 编辑项目源代码**
- 修改 src/ 下的代码文件
- 不干涉正常开发流程

**场景 3: 项目永久文档**
- 编辑 README.md、CONTRIBUTING.md 等
- 这些是项目永久文档,不移动到 temp/

## 核心能力

### 1. Session 管理

#### 自动创建 Session 目录

**命名格式**: `temp/sessions/YYYY-MM-DD-HHMM-{keywords}/`

**关键词提取规则**:
1. 从用户消息中提取 2-3 个关键词
2. 优先提取动作词(add, fix, refactor, update)
3. 再提取主题词(auth, login, api, database)
4. 使用短横线连接,全小写

**示例**:
- "添加用户登录功能" → `temp/sessions/2026-03-09-1430-add-login/`
- "重构数据库访问层" → `temp/sessions/2026-03-09-1530-refactor-database/`
- "修复 API 认证 bug" → `temp/sessions/2026-03-09-1630-fix-api-auth/`

#### 自动创建 INDEX.md

**创建时机**: session 目录创建后立即创建

**初始化内容**:
- 从用户消息提取任务目标
- 记录创建时间和最后更新时间
- 初始化标准结构(见下方)

#### 继续之前的 Session

**触发条件**:
- 用户说"继续之前的工作"
- 用户说"继续上次的任务"
- 用户引用了之前的 session

**执行步骤**:
1. 查找最近的 session 目录(按时间戳排序)
2. 读取该 session 的 INDEX.md
3. 恢复任务上下文
4. 更新 INDEX.md 的"最后更新"时间

### 2. INDEX.md 主线文档

#### 标准结构(保持简洁)

```markdown
# {任务名称}

**创建时间**: YYYY-MM-DD HH:mm
**最后更新**: YYYY-MM-DD HH:mm

## 📋 任务概览

[最多 5 行,简洁描述任务目标]

## 🎯 需求背景

[最多 3 句话,说明为什么做这个任务]

## 🔍 分析主线

1. [核心分析思路 1]
2. [核心分析思路 2]
3. [核心分析思路 3]
...最多 5 个要点

## 📂 文档关系图

- [INDEX.md](INDEX.md) - 主线文档(本文档)
- [requirements-alignment.md](requirements-alignment.md) - 需求对齐
- [design.md](design.md) - 设计文档
- [impact-analysis.md](impact-analysis.md) - 影响面分析
- [implementation-plan.md](implementation-plan.md) - 实现计划
- [progress-details.md](progress-details.md) - 详细进度
...列出核心文档,最多 10 个

## 📊 当前进度

**总体进度**: X% (已完成 Y/Z 项)

**关键里程碑**:
- [x] 需求对齐完成
- [ ] 设计完成
- [ ] 实现完成
- [ ] 测试完成
- [ ] 代码提交完成
...最多 5 个里程碑

**详细进度**: 见 [progress-details.md](progress-details.md)

## ✅ 关键决策

1. **决策 1**: [决策内容](1-2 句话)
2. **决策 2**: [决策内容](1-2 句话)
...最多 5 个关键决策

## 🔗 相关资源

**代码文件**:
- `src/auth/login.ts`
- `src/auth/permissions.ts`
...最多 10 个核心文件

**参考文档**:
- [相关 Issue #123](链接)
- [参考设计文档](链接)
...最多 5 个参考
```

#### 内容限制规则(必须遵守)

**INDEX.md 保持简洁,只包含核心信息**:
- 任务概览: 最多 5 行
- 需求背景: 最多 3 句话
- 分析主线: 最多 5 个要点
- 文档关系图: 最多 10 个文档
- 关键里程碑: 最多 5 个
- 关键决策: 最多 5 个
- 相关资源: 最多 15 个

**详细内容分离到独立文档**:
- 详细进度 → `progress-details.md`
- 详细记录 → `detailed-records.md`
- 改动总结 → `changes-summary.md`
- 错误日志 → `error-recovery.md`

#### 更新规则

**何时更新 INDEX.md**:
1. 完成关键里程碑(需求对齐、设计、实现等)
2. 做出重要技术决策
3. 创建新的文档(更新文档关系图)
4. 任务进度有显著变化(≥10%)

**更新内容**:
- 更新"最后更新"时间戳
- 更新进度百分比和里程碑状态
- 添加新的关键决策
- 更新文档关系图

**不更新 INDEX.md 的情况**:
- 小的代码改动
- 调试和测试过程中的临时改动
- 不影响整体进度的细节调整

### 3. 文档模板库

详见 [knowledge/4-document-templates.md](knowledge/4-document-templates.md)

#### 常用模板

**需求分析阶段**:
- `requirements-alignment.md` - 需求对齐,确保理解用户需求
- `impact-analysis.md` - 影响面分析,评估改动范围

**设计阶段**:
- `design.md` - 设计文档,技术方案和实现思路
- `confirmation.md` - 用户确认,关键决策需要用户确认

**实现阶段**:
- `implementation-plan.md` - 实现计划,分步骤执行
- `progress-details.md` - 详细进度,记录每个步骤的状态

**错误恢复**:
- `error-recovery.md` - 错误恢复,记录遇到的问题和解决方案

#### 模板使用规则

**自动应用模板**:
- 检测到需要创建某类文档时
- 自动使用对应模板
- 填充模板的必填字段

**双向链接**:
- 在 INDEX.md 中添加指向新文档的链接
- 在新文档开头添加指向 INDEX.md 的链接

### 4. 子任务管理(大型任务)

#### 触发条件

**自动检测**:
1. 任务包含 ≥3 个独立改动点
2. 用户明确要求"逐一分析"或"一项项来"
3. 单个改动完成后,用户提出新的改动需求

**示例**:
- "添加登录、权限管理和审计日志" → 3 个子任务
- "重构整个认证系统" → 可能需要多个子任务

#### 子任务目录结构

```
temp/sessions/{session}/
├── INDEX.md                           # 主线文档
├── sub-task-01-add-login/             # 子任务 1
│   ├── design.md                      # 设计文档
│   ├── impact-analysis.md             # 影响面分析
│   └── confirmation.md                # 用户确认
├── sub-task-02-add-permissions/       # 子任务 2
│   ├── design.md
│   ├── impact-analysis.md
│   └── confirmation.md
└── sub-task-03-add-audit/             # 子任务 3
    └── ...
```

#### INDEX.md 的子任务章节

```markdown
## 📦 任务分解

### 子任务列表

1. ✅ [子任务1: 添加登录](sub-task-01-add-login/design.md) - 已完成
2. ⏸️ [子任务2: 添加权限](sub-task-02-add-permissions/design.md) - 进行中
3. ⏳ [子任务3: 添加审计日志](sub-task-03-add-audit/design.md) - 待开始

### 当前子任务

- **编号**: sub-task-02
- **名称**: 添加权限管理
- **状态**: 进行中
- **阶段**: 实现阶段
- **进度**: 60%
```

详见 [knowledge/5-sub-task-management.md](knowledge/5-sub-task-management.md)

### 5. 多项目改动追踪

#### 触发时机

**提交代码前**(执行 `git commit` 前):
- 自动检查当前工作目录
- 识别所有改动的项目
- 在 INDEX.md 中记录改动清单

#### 检查范围

1. **当前项目**: 当前工作目录下的 Git 仓库
2. **Submodules**: 检查是否包含 Git submodules
3. **其他项目**: 用户明确提到的其他项目

#### 在 INDEX.md 中记录

```markdown
## 📦 改动的项目

### ProjectA (当前项目)

- **分支**: feature/add-auth
- **改动文件**:
  - `src/auth/login.ts` - 添加登录功能
  - `src/auth/permissions.ts` - 添加权限管理
  - `tests/auth.test.ts` - 添加测试用例
- **提交状态**: ✅ 已提交

### ProjectB (Submodule)

- **分支**: main
- **改动文件**:
  - `config/auth.yml` - 更新认证配置
- **提交状态**: ⏸️ 待提交

### 提交前检查清单

- [ ] 所有项目都已提交
- [ ] 提交信息符合规范
- [ ] 代码已通过测试
- [ ] 文档已更新
```

详见 [knowledge/6-multi-project-tracking.md](knowledge/6-multi-project-tracking.md)

### 6. 文档清理策略

#### 何时清理

**触发条件**:
1. **Session 完成**: 任务完成、代码已提交
2. **Session 过多**: `temp/sessions/` 下超过 20 个目录
3. **用户请求**: 用户明确要求清理

#### 清理策略

**重要 session** → 归档到 `temp/sessions/archive/YYYY-MM/`
- 任务持续时间 > 1 天
- 包含重要决策和设计文档
- 用户明确标记为重要

**临时 session** → 直接删除
- 任务持续时间 < 1 小时
- 只是简单的 bug 修复或小改动
- 没有重要文档

**用户确认**:
- 清理前询问用户
- 提供清理清单供用户确认
- 允许用户选择保留特定 session

详见 [knowledge/7-cleanup-strategy.md](knowledge/7-cleanup-strategy.md)

## 详细流程说明

详细的流程步骤、检查清单和模板请查阅 `knowledge/` 子目录:

- [知识索引](knowledge/index.md) - 所有知识文档的导航
- [核心概念](knowledge/1-core-concepts.md) - 工作目录分离、主线文档等核心理念
- [Session 管理](knowledge/2-session-management.md) - 创建、命名、切换 session
- [INDEX.md 结构](knowledge/3-index-structure.md) - INDEX.md 的详细结构和更新规则
- [文档模板库](knowledge/4-document-templates.md) - 所有文档模板的详细说明
- [子任务管理](knowledge/5-sub-task-management.md) - 大型任务的分解和管理
- [多项目追踪](knowledge/6-multi-project-tracking.md) - 识别和追踪多项目改动
- [清理策略](knowledge/7-cleanup-strategy.md) - 文档清理和归档机制
- [最佳实践](knowledge/8-best-practices.md) - 常见场景和最佳实践

## 与其他 Skills 的关系

### 基础设施 Skill

**workspace-structure-manager** 是一个基础设施 skill,为其他 skills 提供统一的文档组织方式:

- ✅ 不替代 `complex-task-solver` - 任务分解和编排
- ✅ 不替代 `miravia-git` - Git 分支管理规范
- ✅ 不替代 `skills-manager` - Skill 生命周期管理

### 互补关系

| Skill | 职责 | workspace-structure-manager 的作用 |
|-------|------|------------------------------------|
| `complex-task-solver` | 任务复杂度评估、流程路由、任务分解 | 为其提供规范的文档存放位置 |
| `miravia-git` | Git 分支管理规范 | 识别多项目改动,配合 Git 提交 |
| `skills-manager` | Skill 生命周期管理 | 确保 skill 文档规范 |

### 改编来源

**Codea workspace-management Rule**:
- 原始设计来自 Codea 平台
- 适配到 Claude Code 环境
- 保留核心理念,调整实现细节

## 最佳实践

### 1. 自动化优先

**Agent 自动执行,无需用户手动管理**:
- 不要等待用户说"创建 session"
- 检测到新任务就自动创建
- 自动更新 INDEX.md,保持同步

### 2. 保持简洁

**INDEX.md 只包含核心信息**:
- 每个章节有明确的长度限制
- 详细内容分离到独立文档
- 避免信息过载

### 3. 双向链接

**INDEX.md ↔ 其他文档相互引用**:
- INDEX.md 链接到所有相关文档
- 每个文档开头链接回 INDEX.md
- 形成清晰的文档导航网络

### 4. 灵活适配

**尊重用户指定的路径**:
- 用户明确指定路径时,遵循用户指示
- 不强制覆盖用户创建的文档
- 可以切换或继续之前的 session

### 5. 及时清理

**防止 `temp/sessions/` 膨胀**:
- Session 完成后及时清理
- 重要 session 归档,临时 session 删除
- 定期检查目录大小

## 限制与注意事项

### 适用范围

**✅ 适用于**:
- Claude Code 环境
- 支持 `temp/sessions/` 目录的项目
- 需要规范化文档管理的项目

**❌ 不适用于**:
- 非 Claude Code 环境(如 Codea - 使用原始 Rule)
- 不支持临时目录的项目(罕见)
- 用户明确拒绝使用临时目录

### 用户控制

**用户可以覆盖默认行为**:
- 明确指定文档路径时,遵循用户指示
- 用户说"不要创建 session"时,停止自动创建
- 用户可以手动删除或移动 session 目录

### 与现有文档的兼容

**不破坏现有项目结构**:
- 不移动或删除现有的项目文档
- 不修改 docs/ 目录下的文档
- 只管理 temp/sessions/ 下的临时文档

## 版本历史

- **v1.0.0** (2026-03-09) - 初始版本
  - 改编自 Codea workspace-management Rule
  - 实现核心功能: Session 管理、INDEX.md、文档模板、子任务管理、多项目追踪、清理策略

## 反馈与改进

如有问题或改进建议,请通过以下方式反馈:
- 提交 Issue 到 lulu-skills-common 仓库
- 联系 skill 维护者
