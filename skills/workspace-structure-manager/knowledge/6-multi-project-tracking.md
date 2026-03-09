# 多项目改动追踪

> 识别和追踪多项目改动,确保提交完整

[← 上一篇: 子任务管理](5-sub-task-management.md) | [返回知识库索引](index.md) | [下一篇: 清理策略 →](7-cleanup-strategy.md)

---

## 什么时候需要多项目追踪?

### 触发时机

**提交代码前**(执行 `git commit` 前):
- 自动检查当前工作目录
- 识别所有改动的项目
- 在 INDEX.md 中记录改动清单

### 典型场景

**场景 1: 主项目 + Submodules**
```
project-root/
├── backend/          # 主项目
│   └── src/
├── frontend/         # Submodule
│   └── src/
└── config/           # Submodule
    └── yml/
```

**场景 2: Monorepo**
```
monorepo/
├── packages/
│   ├── api/          # 项目 A
│   ├── web/          # 项目 B
│   └── mobile/       # 项目 C
```

---

## 项目识别机制

### 检查范围

1. **当前项目**: 当前工作目录下的 Git 仓库
2. **Submodules**: 检查是否包含 Git submodules
3. **其他项目**: 用户明确提到的其他项目

### 识别步骤

```
[检查 git status] → [检查 submodules] → [识别改动的项目] → [记录到 INDEX.md]
```

---

## INDEX.md 记录格式

### 标准格式

```markdown
## 📦 改动的项目

### ProjectA (当前项目)

- **仓库路径**: /path/to/projectA
- **分支**: feature/add-auth
- **改动文件**:
  - `src/auth/login.ts` - 添加登录功能
  - `src/auth/permissions.ts` - 添加权限管理
  - `tests/auth.test.ts` - 添加测试用例
- **提交状态**: ✅ 已提交 / ⏸️ 待提交

### ProjectB (Submodule)

- **仓库路径**: /path/to/projectB
- **分支**: main
- **改动文件**:
  - `config/auth.yml` - 更新认证配置
- **提交状态**: ⏸️ 待提交

### 提交前检查清单

- [ ] 所有项目都已提交
- [ ] 提交信息符合规范
- [ ] 代码已通过测试
- [ ] 文档已更新
- [ ] 已通知相关人员
```

### 详细记录

**改动文件格式**:
- `file/path.ts` - 简短说明(不超过 10 个字)

**提交状态**:
- ✅ 已提交
- ⏸️ 待提交
- ⏹️ 不需要提交(临时改动)

---

## 改动文件追踪

### 追踪内容

**必须追踪**:
- 新增的文件
- 修改的文件
- 删除的文件

**不追踪**:
- 临时文件(*.tmp, *.log 等)
- 编译产物(*.o, *.class 等)
- 依赖目录(node_modules/, vendor/ 等)

### 改动说明

**简短说明**(每个文件 1 行):
- 新增: "添加 xxx 功能"
- 修改: "更新 xxx 逻辑"
- 删除: "移除 xxx 功能"

**不要过于详细**:
- ✅ 好: "添加登录功能"
- ❌ 不好: "添加登录功能,包括用户名密码验证、JWT token 生成、错误处理和单元测试"

---

## 提交前检查清单

### 标准检查清单

```markdown
### 提交前检查清单

**代码质量**:
- [ ] 代码已通过 lint 检查
- [ ] 代码已通过测试
- [ ] 没有 console.log 或调试代码
- [ ] 没有注释掉的代码

**提交规范**:
- [ ] 提交信息符合规范
- [ ] 每个项目都已提交
- [ ] 提交信息清晰描述改动

**文档和通知**:
- [ ] README 或文档已更新
- [ ] 相关人员已通知
- [ ] 破坏性改动已说明

**测试**:
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试完成
```

### 自定义检查清单

根据项目需求添加特定检查项:
- [ ] 数据库迁移脚本已准备
- [ ] 配置文件已更新
- [ ] API 文档已更新
- [ ] 用户已确认改动

---

## Submodule 处理

### 识别 Submodules

```bash
git submodule status
```

### 检查 Submodule 改动

```bash
cd submodule-path
git status
```

### 提交 Submodule

```bash
# 1. 提交 submodule
cd submodule-path
git add .
git commit -m "commit message"
git push

# 2. 提交主项目(更新 submodule 引用)
cd ..
git add submodule-path
git commit -m "update submodule"
git push
```

---

## 最佳实践

### 1. 自动识别

**✅ 好的做法**:
- 提交前自动检查所有项目
- 自动记录到 INDEX.md
- 提示用户确认

**❌ 不好的做法**:
- 等待用户手动列出改动的项目
- 不检查 submodules
- 不记录改动清单

### 2. 清晰记录

**✅ 好的做法**:
- 每个项目单独列出
- 改动文件带简短说明
- 标记提交状态

**❌ 不好的做法**:
- 所有项目混在一起
- 只列文件名,不说明改动
- 不标记提交状态

### 3. 提交前确认

**✅ 好的做法**:
- 提供完整的检查清单
- 询问用户是否都已检查
- 确认后再提交

**❌ 不好的做法**:
- 不检查就直接提交
- 遗漏某些项目
- 不通知用户

---

[← 上一篇: 子任务管理](5-sub-task-management.md) | [返回知识库索引](index.md) | [下一篇: 清理策略 →](7-cleanup-strategy.md)
