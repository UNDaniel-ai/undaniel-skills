# Session 管理

> 详解如何创建、命名、切换和管理 Session

[← 上一篇: 核心概念](1-core-concepts.md) | [返回知识库索引](index.md) | [下一篇: INDEX.md 结构 →](3-index-structure.md)

---

## 目录

1. [Session 概念](#session-概念)
2. [Session 创建](#session-创建)
3. [Session 命名规则](#session-命名规则)
4. [Session 切换](#session-切换)
5. [Session 生命周期](#session-生命周期)

---

## Session 概念

### 什么是 Session?

**Session** 是一个独立的工作目录,用于管理特定开发任务的所有临时文档。

**Session 的特点**:
- 每个 session 对应一个具体的开发任务
- 包含该任务的所有临时文档(需求、设计、进度等)
- 有独立的 INDEX.md 作为导航中心
- 按时间戳命名,便于识别和排序

### Session 目录结构

```
temp/sessions/{session-name}/
├── INDEX.md                    # 主线文档(必须)
├── requirements-alignment.md   # 需求对齐
├── design.md                   # 设计文档
├── impact-analysis.md          # 影响面分析
├── implementation-plan.md      # 实现计划
├── progress-details.md         # 详细进度
└── sub-task-01-xxx/            # 子任务目录(可选)
    └── ...
```

### Session vs 项目目录

| 维度 | Session 目录 | 项目目录 |
|------|-------------|----------|
| **位置** | `temp/sessions/{session}/` | 项目根目录 |
| **内容** | 临时工作文档 | 项目源代码和永久文档 |
| **生命周期** | 任务完成后清理或归档 | 长期保留 |
| **Git 跟踪** | 通常不提交(在 .gitignore 中) | 提交到 Git |

---

## Session 创建

### 触发条件

**自动触发**(无需用户指定):
1. 用户描述了一个新的开发任务
2. 当前没有活跃的 session,或之前的 session 已完成
3. 任务内容与当前 session 不相关

**示例触发消息**:
- "帮我添加用户登录功能"
- "我想重构数据库访问层"
- "修复 API 认证的 bug"
- "实现一个新的数据导出功能"

**不触发的情况**:
- 继续之前的任务("继续之前的工作")
- 用户明确指定文档路径("在 docs/ 下创建 xxx.md")
- 简单的代码修改(不需要临时文档)

### 创建流程

```
[用户描述新任务]
    ↓
[检测:是新任务还是继续之前的任务?]
    ↓
[新任务] → [提取关键词]
    ↓
[生成 session 名称]
    ↓
[创建 session 目录]
    ↓
[创建 INDEX.md]
    ↓
[通知用户:Session 已创建]
```

### 创建步骤(详细)

**步骤 1: 提取关键词**

从用户消息中提取 2-3 个关键词:
- 优先提取动作词: add, fix, refactor, update, implement, create
- 再提取主题词: auth, login, api, database, export, user

**步骤 2: 生成 session 名称**

格式: `YYYY-MM-DD-HHMM-{keyword1}-{keyword2}-{keyword3}`

示例:
- "添加用户登录功能" → `2026-03-09-1430-add-user-login`
- "重构数据库访问层" → `2026-03-09-1530-refactor-database-access`
- "修复 API 认证 bug" → `2026-03-09-1630-fix-api-auth`

**步骤 3: 创建目录**

```bash
mkdir -p temp/sessions/2026-03-09-1430-add-user-login
```

**步骤 4: 创建 INDEX.md**

使用标准模板创建 INDEX.md,填充以下内容:
- 任务名称(从用户消息提取)
- 创建时间(当前时间)
- 任务概览(从用户消息提取或总结)
- 需求背景(如果用户提供)

**步骤 5: 通知用户**

```
✅ Session 已创建: temp/sessions/2026-03-09-1430-add-user-login/
📄 INDEX.md 已初始化
```

---

## Session 命名规则

### 命名格式

**标准格式**: `YYYY-MM-DD-HHMM-{keywords}`

**组成部分**:
1. **日期**: YYYY-MM-DD(如 2026-03-09)
2. **时间**: HHMM(如 1430,表示 14:30)
3. **关键词**: 2-3 个关键词,用短横线连接

### 关键词提取规则

**规则 1: 优先提取动作词**

常见动作词:
- add - 添加新功能
- fix - 修复 bug
- refactor - 重构代码
- update - 更新现有功能
- implement - 实现
- create - 创建
- remove - 删除
- optimize - 优化

**规则 2: 再提取主题词**

主题词通常是名词或名词短语:
- 功能名称: login, auth, export, import
- 模块名称: database, api, ui, backend
- 组件名称: button, form, modal, table
- 系统名称: user, order, product, payment

**规则 3: 保持简洁**

- 最多 3 个关键词
- 使用短横线连接
- 全小写
- 避免冗余词汇

### 命名示例

| 用户消息 | Session 名称 | 说明 |
|---------|-------------|------|
| "添加用户登录功能" | `2026-03-09-1430-add-user-login` | 动作词 + 主题词 |
| "重构数据库访问层" | `2026-03-09-1530-refactor-database` | 动作词 + 主题词 |
| "修复 API 认证的 bug" | `2026-03-09-1630-fix-api-auth` | 动作词 + 两个主题词 |
| "实现数据导出功能" | `2026-03-09-1730-implement-data-export` | 动作词 + 两个主题词 |
| "优化查询性能" | `2026-03-09-1830-optimize-query` | 动作词 + 主题词 |
| "创建用户管理界面" | `2026-03-09-1930-create-user-ui` | 动作词 + 两个主题词 |

### 特殊情况处理

**情况 1: 无法提取明确关键词**

用户消息: "帮我改一下这个"

处理方式:
- 使用通用关键词: `update-code`, `modify-file`, `change-logic`
- 或使用时间戳: `2026-03-09-1430-task`

**情况 2: 关键词过长**

用户消息: "添加用户认证和授权管理功能"

处理方式:
- 简化: `add-user-auth`(而不是 `add-user-authentication-authorization-management`)
- 选择最核心的 2-3 个词

**情况 3: 中文关键词**

用户消息: "添加用户登录功能"

处理方式:
- 翻译为英文: `add-user-login`
- 或使用拼音: `add-yonghu-denglu`(不推荐,可读性差)

---

## Session 切换

### 什么时候需要切换 Session?

**场景 1: 继续之前的任务**

用户说:
- "继续之前的工作"
- "继续上次的任务"
- "回到之前的 session"

**场景 2: 在多个任务之间切换**

用户说:
- "先处理另一个任务"
- "切换到 xxx 任务"
- "暂停当前任务,处理 xxx"

**场景 3: 用户明确指定 session**

用户说:
- "打开 session 2026-03-09-1430-add-login"
- "查看之前的登录功能 session"

### 切换流程

```
[用户请求切换 session]
    ↓
[识别目标 session]
    ↓
[读取目标 session 的 INDEX.md]
    ↓
[恢复任务上下文]
    ↓
[更新 INDEX.md 的"最后更新"时间]
    ↓
[通知用户:已切换到 session XXX]
```

### 切换步骤(详细)

**步骤 1: 识别目标 session**

**方式 1: 用户明确指定**
- "打开 session 2026-03-09-1430-add-login"
- 直接使用该 session

**方式 2: 用户说"继续之前的工作"**
- 查找最近的 session(按时间戳排序)
- 选择最新的 session

**方式 3: 用户说"切换到 xxx 任务"**
- 从关键词匹配 session 名称
- 如果找不到,列出所有 session 供用户选择

**步骤 2: 读取 INDEX.md**

```bash
cat temp/sessions/2026-03-09-1430-add-login/INDEX.md
```

**步骤 3: 恢复任务上下文**

从 INDEX.md 中提取:
- 任务概览
- 当前进度
- 关键决策
- 相关文档列表

**步骤 4: 更新 INDEX.md**

更新"最后更新"时间戳:
```markdown
**最后更新**: 2026-03-09 16:30
```

**步骤 5: 通知用户**

```
✅ 已切换到 session: temp/sessions/2026-03-09-1430-add-login/
📄 任务: 添加用户登录功能
📊 进度: 60% (设计完成,开始实现)
```

### 列出所有 Session

**命令**:
```bash
ls -t temp/sessions/
```

**输出格式**:
```
temp/sessions/
├── 2026-03-09-1630-fix-api-auth/       # 最新
├── 2026-03-09-1530-refactor-database/  # 较新
└── 2026-03-09-1430-add-login/          # 较旧
```

**提供给用户的选择界面**(可选):
```
找到以下 sessions:

1. [进行中] 2026-03-09-1630-fix-api-auth - 修复 API 认证 bug (进度: 40%)
2. [已完成] 2026-03-09-1530-refactor-database - 重构数据库访问层 (进度: 100%)
3. [暂停] 2026-03-09-1430-add-login - 添加用户登录功能 (进度: 60%)

请选择要切换到的 session (输入编号或名称):
```

---

## Session 生命周期

### Session 状态

**进行中** (Active):
- 任务正在执行中
- INDEX.md 中的进度 < 100%
- 最后更新时间在最近(如 24 小时内)

**暂停** (Paused):
- 任务暂时搁置
- 可能稍后继续
- 最后更新时间较早(如 1-7 天前)

**已完成** (Completed):
- 任务已完成
- INDEX.md 中的进度 = 100%
- 代码已提交

**已归档** (Archived):
- 任务完成且已归档
- 移动到 `temp/sessions/archive/YYYY-MM/`
- 保留作为参考

**已删除** (Deleted):
- 临时 session,已删除
- 不再需要保留

### 生命周期流程

```
[创建] → [进行中] → [已完成] → [归档或删除]
                ↓
            [暂停] → [继续] → [进行中]
                ↓
            [放弃] → [删除]
```

### 状态转换

**进行中 → 暂停**:
- 用户说"暂停当前任务"
- 切换到其他 session
- 长时间未更新

**暂停 → 进行中**:
- 用户说"继续之前的任务"
- 切换回该 session

**进行中 → 已完成**:
- 任务目标达成
- 代码已提交
- 进度更新为 100%

**已完成 → 归档**:
- 用户确认可以归档
- 或自动归档(根据清理策略)

**已完成 → 删除**:
- 临时 session,不需要保留
- 用户确认删除

### 清理和归档

详见 [knowledge/7-cleanup-strategy.md](7-cleanup-strategy.md)

**归档条件**:
- 任务完成
- 包含重要决策和设计文档
- 任务持续时间 > 1 天

**删除条件**:
- 简单任务(如 bug 修复)
- 任务持续时间 < 1 小时
- 没有重要文档

---

## 最佳实践

### 1. 及时创建 Session

**✅ 好的做法**:
- 检测到新任务立即创建 session
- 不等待用户说"创建 session"

**❌ 不好的做法**:
- 等待用户明确指示
- 在项目根目录创建临时文档

### 2. 合理命名 Session

**✅ 好的命名**:
- `2026-03-09-1430-add-user-login` - 清晰、简洁
- `2026-03-09-1530-fix-api-auth` - 明确任务类型

**❌ 不好的命名**:
- `2026-03-09-1430-task` - 过于笼统
- `2026-03-09-1430-add-user-authentication-and-authorization-management` - 过长

### 3. 保持 Session 独立

**✅ 好的做法**:
- 每个 session 对应一个独立任务
- 不同任务使用不同 session

**❌ 不好的做法**:
- 多个不相关任务共用一个 session
- Session 混杂多个任务的文档

### 4. 及时切换 Session

**✅ 好的做法**:
- 用户说"继续之前的任务"时,立即切换
- 读取 INDEX.md 恢复上下文

**❌ 不好的做法**:
- 不切换,继续使用当前 session
- 不读取 INDEX.md,丢失上下文

---

[← 上一篇: 核心概念](1-core-concepts.md) | [返回知识库索引](index.md) | [下一篇: INDEX.md 结构 →](3-index-structure.md)
