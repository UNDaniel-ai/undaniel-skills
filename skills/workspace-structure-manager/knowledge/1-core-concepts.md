# 核心概念

> 理解 workspace-structure-manager 的设计理念和核心原则

[← 返回知识库索引](index.md) | [下一篇: Session 管理 →](2-session-management.md)

---

## 目录

1. [设计背景](#设计背景)
2. [核心问题](#核心问题)
3. [设计理念](#设计理念)
4. [核心原则](#核心原则)
5. [与其他 Skills 的关系](#与其他-skills-的关系)
6. [改编来源](#改编来源)

---

## 设计背景

### 用户痛点

**问题描述**: Agent 有时会破坏项目内的文件夹结构,感觉有点乱

**典型混乱场景**:
```
project-root/
├── plan.md                    # ❌ 应在 temp/sessions/{session}/
├── requirements.md            # ❌ 应在 temp/sessions/{session}/
├── design-v1.md               # ❌ 应在 temp/sessions/{session}/
├── design-v2.md               # ❌ 应在 temp/sessions/{session}/
├── progress.md                # ❌ 应在 temp/sessions/{session}/
├── TODO.md                    # ❌ 应在 temp/sessions/{session}/
├── temp-notes.md              # ❌ 应在 temp/sessions/{session}/
├── old-design.md              # ❌ 应在 temp/sessions/{session}/
├── src/                       # ✅ 正常项目代码
└── README.md                  # ✅ 正常项目文档
```

**问题分析**:
1. **临时文档散落**: 计划、设计、分析文档等散落在项目根目录
2. **没有主线文档**: 缺少统一的导航文档,不知道哪些文档是核心的
3. **文档版本混乱**: design-v1.md, design-v2.md, old-design.md 混在一起
4. **清理困难**: 任务完成后,不知道哪些文档可以删除
5. **多项目混乱**: 改动了多个项目,没有清晰的追踪

### 用户需求

创建一个新的 skill,让 Agent 能够更加规范地管理文件夹结构:
- 临时文档与永久文档分离
- 有清晰的文档导航系统
- 自动化管理,无需用户手动干预
- 支持复杂任务的结构化管理

---

## 核心问题

### 为什么 Agent 会破坏文件夹结构?

**原因 1: 缺少工作目录管理规范**
- Agent 不知道应该把临时文档放在哪里
- 默认放在当前工作目录(通常是项目根目录)
- 导致临时文档与项目文档混在一起

**原因 2: 没有主线文档系统**
- 缺少 INDEX.md 来维护文档关系
- 不知道哪些文档是核心的、哪些是临时的
- 无法建立清晰的文档导航

**原因 3: 文档清理不规范**
- 旧文档没有及时清理或归档
- 不知道哪些文档可以删除
- 导致文档越来越多、越来越乱

**原因 4: 多项目改动没有追踪**
- 改动了多个项目,没有统一记录
- 提交时容易遗漏某些项目
- 没有清晰的改动清单

### 理想的文件夹结构

```
project-root/
├── temp/                               # 临时文件目录
│   └── sessions/                       # Session 目录
│       ├── 2026-03-09-1430-add-auth/   # Session 1
│       │   ├── INDEX.md                # ✅ 主线文档
│       │   ├── requirements-alignment.md
│       │   ├── design.md
│       │   ├── impact-analysis.md
│       │   └── progress-details.md
│       └── 2026-03-09-1630-fix-bug/    # Session 2
│           └── ...
├── docs/                               # 项目永久文档
│   ├── architecture.md
│   └── api.md
├── src/                                # 项目源代码
│   └── ...
└── README.md                           # 项目说明
```

**关键特点**:
- ✅ 临时文档集中在 `temp/sessions/{session}/` 下
- ✅ 每个 session 有独立的目录,按时间戳命名
- ✅ 每个 session 有 INDEX.md 作为导航中心
- ✅ 项目根目录保持整洁
- ✅ 项目永久文档在 docs/ 下

---

## 设计理念

### 1. 工作目录分离

**核心思想**: 临时工作文档与项目永久文档分离

**临时工作文档** → `temp/sessions/{session}/`
- 需求分析文档
- 设计文档
- 实现计划
- 进度追踪文档
- 错误恢复记录
- 用户确认文档

**项目永久文档** → `docs/`, `README.md` 等
- 项目说明文档
- API 文档
- 架构设计文档
- 用户手册
- 贡献指南

**为什么要分离?**
- 避免临时文档污染项目根目录
- 便于清理和归档
- 清晰区分文档的生命周期
- 便于多任务并行(每个任务一个 session)

### 2. 主线文档中心

**核心思想**: 每个 session 必须有 INDEX.md 作为导航中心

**INDEX.md 的作用**:
- 任务概览 - 目标、背景、成功标准
- 分析主线 - 核心分析思路(最多 5 个要点)
- 文档关系图 - 所有相关文档的导航(带双向链接)
- 当前进度 - 总体进度、关键里程碑
- 关键决策 - 重要技术决策记录

**为什么需要主线文档?**
- 提供统一的文档导航入口
- 快速了解任务整体情况
- 建立文档之间的关系
- 便于恢复任务上下文
- 避免信息过载(保持简洁)

### 3. 自动化执行

**核心思想**: Agent 自动管理文件夹结构,无需用户干预

**自动执行的操作**:
- 检测新任务时自动创建 session 目录
- 创建临时文档时自动保存到当前 session
- 任务进展时自动更新 INDEX.md
- 提交代码前自动识别多项目改动
- Session 完成后提示清理或归档

**为什么要自动化?**
- 减少用户负担(不需要手动管理目录)
- 确保规范统一执行
- 避免人为疏忽导致的混乱
- 提高工作效率

**灵活适配**:
- 尊重用户明确指定的路径
- 不强制覆盖用户创建的文档
- 可以切换或继续之前的 session
- 用户可以禁用自动化行为

### 4. 结构化管理

**核心思想**: 支持复杂任务的结构化管理

**单任务 → 单 session**:
- 简单任务直接在 session 目录下管理
- INDEX.md + 相关文档

**大型任务 → 子任务分解**:
- 触发条件: ≥3 个独立改动点
- 子任务目录: `sub-task-01-{name}/`, `sub-task-02-{name}/`
- 子任务独立文档: design.md, impact-analysis.md, confirmation.md
- INDEX.md 维护子任务列表和状态

**多项目改动 → 改动追踪**:
- 识别所有改动的项目
- 在 INDEX.md 中记录改动清单
- 提交前检查清单

---

## 核心原则

### 原则 1: 分离临时与永久

**定义明确的边界**:
- 临时工作文档 → `temp/sessions/{session}/`
- 项目永久文档 → `docs/`, `README.md` 等

**判断标准**:
- 是否与特定开发任务相关? → 临时文档
- 是否需要长期保留? → 永久文档
- 是否需要提交到 Git? → 通常永久文档需要提交,临时文档不需要

### 原则 2: 主线文档中心

**每个 session 必须有 INDEX.md**:
- 提供统一的文档导航入口
- 维护任务概览和进度
- 建立文档关系网络

**保持简洁**:
- INDEX.md 只包含核心信息
- 详细内容分离到独立文档
- 避免信息过载

**双向链接**:
- INDEX.md 链接到所有相关文档
- 每个文档开头链接回 INDEX.md
- 形成清晰的文档导航网络

### 原则 3: 自动化执行

**Agent 自动执行,无需用户干预**:
- 不要等待用户说"创建 session"
- 检测到新任务就自动创建
- 自动更新 INDEX.md,保持同步

**灵活适配**:
- 尊重用户明确指定的路径
- 不强制覆盖用户创建的文档
- 允许用户禁用自动化行为

### 原则 4: 及时清理

**防止 `temp/sessions/` 膨胀**:
- Session 完成后及时清理
- 重要 session 归档,临时 session 删除
- 定期检查目录大小

**用户确认**:
- 清理前询问用户
- 提供清理清单供用户确认
- 允许用户选择保留特定 session

---

## 与其他 Skills 的关系

### 基础设施 Skill

**workspace-structure-manager** 是一个基础设施 skill,为其他 skills 提供统一的文档组织方式。

### 不重复造轮子

**不替代现有 skills**:
- ✅ 不替代 `complex-task-solver` - 任务分解和编排
- ✅ 不替代 `miravia-git` - Git 分支管理规范
- ✅ 不替代 `skills-manager` - Skill 生命周期管理

### 互补关系

| Skill | 职责 | workspace-structure-manager 的作用 |
|-------|------|------------------------------------|
| `complex-task-solver` | 任务复杂度评估、流程路由、任务分解 | 为其提供规范的文档存放位置 |
| `miravia-git` | Git 分支管理规范、分支命名、合并流程 | 识别多项目改动,配合 Git 提交 |
| `skills-manager` | Skill 生命周期管理、同步、治理 | 确保 skill 文档规范 |

### 协作示例

**场景 1: 复杂任务分解**
1. 用户描述一个复杂任务
2. `complex-task-solver` 评估复杂度,决定是否分解
3. `workspace-structure-manager` 创建 session 目录和 INDEX.md
4. `complex-task-solver` 生成任务分解计划,保存到 session 目录
5. `workspace-structure-manager` 为每个子任务创建子目录
6. 任务执行过程中,`workspace-structure-manager` 更新进度

**场景 2: Git 分支管理**
1. 用户开始新任务
2. `workspace-structure-manager` 创建 session 目录
3. `miravia-git` 按规范创建分支(feature/xxx)
4. 开发过程中改动多个项目
5. `workspace-structure-manager` 识别所有改动的项目
6. 提交前,`workspace-structure-manager` 生成改动清单
7. `miravia-git` 按规范提交和合并

---

## 改编来源

### Codea workspace-management Rule

**原始设计**:
- 来自 Codea 平台的 workspace-management Rule
- 包含 Rule 文件(`.mdc`)和 Skill 文件(`.md`)
- 总计约 2,100 行文档

**核心理念**(保留):
- 工作目录分离
- 主线文档系统(INDEX.md)
- 双向链接
- 文档模板库
- 子任务管理
- 多项目追踪

**适配调整**(针对 Claude Code):
- 格式转换: `.mdc` Rule → `.md` Skill
- 平台适配: Codea → Claude Code
- 工具适配: MCP 工具 → Claude Code 工具
- 依赖调整: 移除对其他 Codea Rules 的依赖

### Codea vs Claude Code

| 维度 | Codea workspace-management | Claude Code workspace-structure-manager |
|------|----------------------------|----------------------------------------|
| **格式** | Rule (`.mdc` 文件) | Skill (`.md` 文件) |
| **平台** | Codea | Claude Code |
| **加载机制** | Rule 引擎 | Skill 引擎(skillctl) |
| **依赖** | 依赖其他 Rules (development-workflow) | 独立 skill,可选配合其他 skills |
| **时间戳** | 使用 MCP 工具 `get_current_timestamp` | 使用系统时间或 Claude Code 工具 |
| **文档量** | 约 2,100 行(rule + skill) | 约 3,200 行(包含扩展和适配) |
| **Agent 配置** | 无 | 可选 `agents/openai.yaml` |

---

## 总结

### 核心价值

✅ **解决 Agent 破坏项目文件夹结构的问题**
- 临时文档与永久文档分离
- 提供统一的文档管理规范

✅ **提供主线文档系统**
- INDEX.md 作为导航中心
- 清晰的文档关系网络

✅ **自动化执行**
- Agent 自动管理,无需用户干预
- 灵活适配,尊重用户指定

✅ **支持复杂任务**
- 子任务分解和管理
- 多项目改动追踪

### 设计特点

✅ **改编自成熟设计**
- 基于 Codea workspace-management Rule
- 保留核心理念,适配到 Claude Code

✅ **完整的文档体系**
- 约 3,200 行详细文档
- 涵盖核心概念、操作流程、模板、最佳实践

✅ **基础设施定位**
- 为其他 skills 提供支撑
- 不重复造轮子,互补而非替代

---

[← 返回知识库索引](index.md) | [下一篇: Session 管理 →](2-session-management.md)
