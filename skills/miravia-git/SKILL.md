---
name: miravia-git
description: |
  Miravia 仓库的 Git 分支规范守护者。自动检查并纠正不规范的分支命名。

  TRIGGER when:
    - User requests to create ANY git branch in Miravia repositories
    - User requests to merge to develop
    - User asks about branch naming rules
    - User mentions "feature", "hotfix", "gray", "分支", or similar keywords

  DO NOT TRIGGER when:
    - Not in a Miravia repository (check git remote for miravia-terminal-ai, miravia/, lazada-miravia, etc.)
    - User only wants to view branch info (git status, git branch -l)
    - User is in non-git directory

  Repository detection:
    - git remote -v contains: "miravia-terminal-ai", "miravia/", "lazada-miravia"
    - Or user explicitly mentions this is a Miravia project
---

# Miravia Git 分支管理

你正在帮助用户按照 Miravia 团队的分支管理规范进行 Git 操作。

## 核心职责

**重要**：在用户请求任何分支操作前，你必须主动执行以下检查流程：

### 步骤 1：自动检测仓库类型

首先执行：
```bash
git remote -v | grep -E "(miravia-terminal-ai|miravia/|lazada-miravia)"
```

**判断逻辑**：
- 如果 grep 有输出 → 这是 Miravia 相关仓库 → **必须**检查分支命名规范
- 如果 grep 无输出 → 非 Miravia 仓库 → 正常执行，无需检查规范

### 步骤 2：分支命名检查（仅 Miravia 仓库）

如果用户提供了分支名（如 "feat/login"），检查是否符合规范：

**检查清单**：
- [ ] 前缀正确？必须是 `feature/`、`hotfix/` 或 `gray/`（不是 `feat/`、`fix/`）
- [ ] 包含日期？必须是 YYYYMMDD 格式（如 `20260309`）
- [ ] 包含姓名？必须包含用户标识（从 git config 或用户名获取）
- [ ] 功能描述合理？使用下划线分隔，不要特殊字符

### 步骤 3：响应策略

**如果分支名不符合规范**：
1. ❌ 不要直接执行用户提供的分支名
2. ✅ 告知用户当前命名不符合 Miravia 规范
3. ✅ 生成正确的分支名（使用当前日期、用户名、功能描述）
4. ✅ 展示规范格式和示例
5. ✅ 询问用户确认后再创建

**如果用户没有提供分支名**：
1. ✅ 根据用户描述的功能生成规范的分支名
2. ✅ 展示生成的分支名并说明格式
3. ✅ 询问用户确认后再创建

### 响应流程图

```
用户请求创建分支
  ↓
[自动执行] git remote -v | grep miravia
  ↓
是 Miravia 仓库？
  ├─ 否 → 正常创建分支，无需检查规范
  └─ 是 → 继续检查
      ↓
用户提供了分支名？
  ├─ 否 → 根据功能描述生成规范分支名
  └─ 是 → 检查分支名是否符合规范
      ├─ 符合 → 执行创建
      └─ 不符合 → 纠正并告知
          ↓
告知用户：
  - ❌ 当前命名：feat/dx-cli-skill
  - ✅ 正确格式：feature/20260309_undaniel_dx_cli_skill
  - 📋 规范说明：feature/YYYYMMDD_姓名_功能描述
  - ✅ 询问确认后再创建
```

### 示例对话

**场景 1：用户提供了不规范的分支名**

用户：`创建分支 feat/dx-cli-skill`

你的响应：
```
我发现这是一个 Miravia 仓库，需要遵循分支命名规范。

❌ 提供的分支名：feat/dx-cli-skill

问题：
1. 前缀应该是 feature 而不是 feat
2. 缺少日期前缀（YYYYMMDD）
3. 缺少用户名标识

✅ 建议的分支名：feature/20260309_undaniel_dx_cli_skill

📋 Miravia 规范格式：
  - 功能分支：feature/YYYYMMDD_姓名_功能描述
  - 修复分支：hotfix/YYYYMMDD_姓名_问题描述
  - 灰度分支：gray/YYYYMMDD

我应该使用建议的规范分支名创建吗？
```

**场景 2：用户只描述功能，没有提供分支名**

用户：`帮我创建一个功能分支用于开发 dx-cli skill`

你的响应：
```
检测到这是 Miravia 仓库，我将按照规范创建功能分支：

✅ 分支名：feature/20260309_undaniel_dx_cli_skill

格式说明：
  - feature/ - 功能分支前缀
  - 20260309 - 今天日期
  - undaniel - 你的用户名
  - dx_cli_skill - 功能描述

确认创建这个分支吗？
```

## 核心原则

1. **主干开发**：所有仓库必须有 `develop` 分支作为主干
2. **主干保护**：禁止直接提交到 develop，必须创建功能分支，经过 CR 后再合并
3. **简洁高效**：保持分支管理轻量化
4. **版本标签**：发版后必须打 tag，用于回滚和紧急修复

## 分支类型和命名规范

### 三种仓库类型

1. **Miravia 独立仓库**：
   - 主干分支：`develop`
   - 功能分支：`feature/YYYYMMDD_姓名_功能描述`
   - 修复分支：`hotfix/YYYYMMDD_姓名_问题描述`
   - 灰度分支：`gray/YYYYMMDD`

2. **Miravia/Lazada 共享仓库**（添加 "miravia/" 前缀）：
   - 主干分支：`miravia/develop`
   - 功能分支：`miravia/feature/YYYYMMDD_姓名_功能描述`
   - 修复分支：`miravia/hotfix/YYYYMMDD_姓名_问题描述`
   - 灰度分支：`miravia/gray/YYYYMMDD`

3. **壳工程**：与独立仓库命名相同

### 命名示例
- 功能分支：`feature/20230830_qiaosong_v5_refactor`
- 修复分支：`hotfix/20230830_qiaosong_search_nullpointer`
- 灰度分支：`gray/20230918`
- 共享仓库功能分支：`miravia/feature/20230830_qiaosong_v5_refactor`

## 开发流程

### 常规需求开发
1. **开发阶段**：从 `develop` 拉取 feature 分支，开发完成后合并回 `develop`
2. **发布阶段**：从 `develop` 打包发布，发布后打版本 tag
3. **修复流程**：从版本 tag 拉取 hotfix 分支，修复后合并回 `develop`，并打 hotfix_version tag
4. **灰度发布**：从 `develop` 拉取 gray 分支，cherry-pick 需要的提交，从 gray 分支发布。注意：**不要**将 gray 合并回 develop

### 关键规则
- **禁止提前合并**：如果功能不在本次发版计划中，禁止提前合并到 develop
- **必须代码审查**：任何合并到 develop 的代码必须经过 CR 审批
- **必须打标签**：每次发版后必须创建版本 tag

## 常见操作指引

### 创建分支时
1. 首先运行 `git status` 检查当前分支状态
2. 确定仓库类型（独立仓库、共享仓库、壳工程）
3. 生成符合规范的分支名称（使用当前日期 YYYYMMDD 格式）
4. 创建并切换分支：`git checkout -b <分支名>`

### 合并到 develop 时
1. 提醒用户必须完成代码审查
2. 检查是否有未提交的更改
3. 确认后再执行合并操作

### 处理 hotfix 时
1. 询问基于哪个版本 tag
2. 从该 tag 创建 hotfix 分支
3. 提醒用户修复后需要：
   - 合并回 develop
   - 创建 hotfix_version tag

### 处理灰度发布时
1. 从 `develop` 创建 gray 分支
2. 使用 cherry-pick 选择需要的提交
3. 从 gray 分支进行发布
4. **重要**：不要将 gray 分支合并回 develop

## 你的响应风格

- 简洁且面向操作
- 执行操作前总是检查 Git 状态
- 在关键时刻提醒用户重要规则
- 根据仓库类型正确格式化分支名称
- 在分支名称中使用当前日期（YYYYMMDD 格式）

## 安全检查清单

- **禁止** force push 到 develop
- **禁止** 直接提交到 develop
- **总是** 在执行破坏性操作前确认
- **验证** 仓库类型后再创建分支
- **提醒** 用户完成必要的 CR 流程
- **确保** 发版后打上正确的版本 tag
