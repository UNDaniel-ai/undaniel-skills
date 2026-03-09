# 10. 设计模板库

## 概述

本文档提供 Mermaid 设计模板，用于 Route B 和 Route C 的设计输出阶段。

## 模板 1: 系统架构图

### 用途
展示系统整体架构和模块关系。

### 模板
\`\`\`mermaid
graph TB
    User[用户] --> Frontend[前端]
    Frontend --> API[API 层]
    API --> Service[服务层]
    Service --> DB[(数据库)]

    subgraph 前端模块
        Frontend --> UI[UI 组件]
        Frontend --> State[状态管理]
    end

    subgraph 后端模块
        Service --> UserService[用户服务]
        Service --> OrderService[订单服务]
    end
\`\`\`

---

## 模板 2: 数据流图

### 用途
展示数据如何在系统中流动。

### 模板
\`\`\`mermaid
sequenceDiagram
    User->>Frontend: 发起请求
    Frontend->>API: 调用 API
    API->>Service: 业务处理
    Service->>DB: 查询数据
    DB-->>Service: 返回数据
    Service-->>API: 返回结果
    API-->>Frontend: 返回响应
    Frontend-->>User: 显示结果
\`\`\`

---

## 模板 3: 流程图

### 用途
展示实施流程和步骤顺序。

### 模板
\`\`\`mermaid
graph TD
    A[开始] --> B[步骤1]
    B --> C[步骤2]
    C --> D{是否成功?}
    D -->|是| E[步骤3]
    D -->|否| F[错误处理]
    F --> C
    E --> G[完成]
\`\`\`

---

## 模板 4: 组件关系图

### 用途
展示前端组件的层级关系。

### 模板
\`\`\`mermaid
graph TD
    App[App] --> Header[Header]
    App --> Main[Main]
    App --> Footer[Footer]

    Main --> UserList[UserList]
    Main --> UserDetail[UserDetail]

    UserList --> UserCard[UserCard]
\`\`\`

---

## 模板 5: 数据库 ER 图

### 用途
展示数据库表结构和关系。

### 模板
\`\`\`mermaid
erDiagram
    User ||--o{ Order : places
    User {
        int id PK
        string name
        string email
    }
    Order {
        int id PK
        int user_id FK
        float total
    }
\`\`\`

---

## 模板 6: 状态机图

### 用途
展示状态转换逻辑。

### 模板
\`\`\`mermaid
stateDiagram-v2
    [*] --> 待处理
    待处理 --> 进行中: 开始处理
    进行中 --> 已完成: 处理成功
    进行中 --> 失败: 处理失败
    失败 --> 待处理: 重试
    已完成 --> [*]
\`\`\`

---

## 使用建议

### Route A（快速流程）
- 不需要设计图

### Route B（标准流程）
- 必需：系统架构图
- 可选：数据流图

### Route C（完整流程）
- 必需：系统架构图 + 数据流图 + 流程图
- 可选：组件关系图、ER 图、状态机图

---

## 参考资料

- [4. Route B 标准流程](4-route-b-standard-flow.md) - Route B 的设计输出要求
- [5. Route C 完整流程](5-route-c-complete-flow.md) - Route C 的设计输出要求
