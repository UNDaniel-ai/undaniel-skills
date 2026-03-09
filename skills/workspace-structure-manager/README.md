# Workspace Structure Manager

> 工作区文件夹结构管理 - 自动管理临时文档、主线文档和工作目录,防止项目根目录混乱

## 概述

Workspace Structure Manager 是一个专门用于管理工作区文件夹结构的 Claude Code Skill,核心能力包括:

- 📁 **自动工作目录管理** - `temp/sessions/{session}/` 自动创建和管理
- 📄 **INDEX.md 主线文档系统** - 任务导航中心,维护任务概览和进度
- 📋 **文档模板库** - requirements、design、impact-analysis 等标准模板
- 🔀 **子任务管理** - 大型任务的结构化管理机制
- 🔍 **多项目改动追踪** - 识别所有改动的项目和文件
- 🗑️ **文档清理和归档策略** - 防止临时文档膨胀

## 快速开始

### 安装

```bash
cd /Users/undaniel/Developer/lulu-skills-common
tools/skillctl sync --skill workspace-structure-manager --agent claude
```

### 验证

```bash
tools/skillctl status --skill workspace-structure-manager --agent claude
```

应该看到:
```
agent    skill                        state        detail
claude   workspace-structure-manager  linked-ok    /path/to/skill
```

## 使用场景

### 场景 1: 新任务自动创建 Session

**用户**: "帮我添加用户登录功能"

**Agent 自动执行**:
1. 创建 session 目录: `temp/sessions/2026-03-09-1430-add-login/`
2. 创建 INDEX.md 主线文档
3. 创建需求对齐文档
4. 开始执行任务

### 场景 2: 继续之前的任务

**用户**: "继续之前的登录功能任务"

**Agent 自动执行**:
1. 识别最近的相关 session
2. 读取 INDEX.md 恢复上下文
3. 继续执行任务

### 场景 3: 复杂任务分解

**用户**: "添加登录、权限管理和审计日志"

**Agent 自动执行**:
1. 创建主 session
2. 分解为 3 个子任务
3. 逐一执行子任务

### 场景 4: 提交前检查

**用户**: "准备提交代码"

**Agent 自动执行**:
1. 检查所有改动的项目
2. 在 INDEX.md 中记录改动清单
3. 提供提交前检查清单

## 文档结构

```
workspace-structure-manager/
├── SKILL.md                          # 主 skill 文档 (527 行)
├── README.md                         # 本文档
├── knowledge/                        # 知识库 (共 3,184 行)
│   ├── index.md                      # 知识索引 (146 行)
│   ├── 1-core-concepts.md           # 核心概念 (373 行)
│   ├── 2-session-management.md      # Session 管理 (448 行)
│   ├── 3-index-structure.md         # INDEX.md 结构 (369 行)
│   ├── 4-document-templates.md      # 文档模板库 (642 行)
│   ├── 5-sub-task-management.md     # 子任务管理 (225 行)
│   ├── 6-multi-project-tracking.md  # 多项目追踪 (243 行)
│   ├── 7-cleanup-strategy.md        # 清理策略 (338 行)
│   └── 8-best-practices.md          # 最佳实践 (400 行)
└── agents/                           # Agent 配置 (可选)
```

**总计**: 约 3,711 行文档

## 核心理念

### 1. 分离临时与永久

- **临时工作文档** → `temp/sessions/{session}/`
- **项目永久文档** → `docs/`, `README.md` 等

### 2. 主线文档中心

- 每个 session 必须有 INDEX.md
- INDEX.md 维护任务概览、进度、决策

### 3. 自动化执行

- Agent 自动管理,无需用户干预
- 灵活适配,尊重用户指定

### 4. 及时清理

- 防止 `temp/sessions/` 膨胀
- 归档重要 session,删除临时 session

## 改编来源

本 skill 改编自 **Codea 平台的 workspace-management Rule**:
- 保留核心理念:工作目录分离、主线文档系统
- 适配到 Claude Code 环境
- 扩展功能:子任务管理、多项目追踪、清理策略

## 与其他 Skills 的关系

**基础设施 Skill**:
- 为其他 skills 提供统一的文档组织方式
- 不替代 `complex-task-solver`(任务分解)
- 不替代 `miravia-git`(Git 管理)
- 配合 `skills-manager`(skill 治理)

## 版本历史

- **v1.0.0** (2026-03-09) - 初始版本
  - 改编自 Codea workspace-management Rule
  - 实现核心功能: Session 管理、INDEX.md、文档模板、子任务管理、多项目追踪、清理策略

## 反馈与改进

如有问题或改进建议,请:
- 提交 Issue 到 lulu-skills-common 仓库
- 或联系 skill 维护者

## 许可证

与 lulu-skills-common 仓库相同
