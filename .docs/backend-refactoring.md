# 后端代码重构说明

## 新的目录结构

重构后的后端代码采用更加模块化和清晰的目录结构：

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI 应用入口
│   │
│   ├── core/                      # 核心功能模块
│   │   ├── __init__.py
│   │   ├── config.py             # 应用配置（环境变量）
│   │   ├── database.py           # 数据库连接和会话管理
│   │   ├── security.py           # 安全相关（JWT、认证）
│   │   └── exceptions.py         # 自定义异常类
│   │
│   ├── models/                   # 数据模型
│   │   ├── __init__.py
│   │   ├── database.py           # SQLAlchemy ORM 模型
│   │   └── enums.py              # 枚举类型（待添加）
│   │
│   ├── schemas/                  # API 数据模式
│   │   ├── __init__.py
│   │   ├── event.py              # 事件相关的 API 模式
│   │   ├── source.py             # 数据源相关的 API 模式
│   │   ├── alert.py              # 告警相关的 API 模式
│   │   └── common.py             # 通用 API 模式
│   │
│   ├── api/                      # API 路由层
│   │   ├── __init__.py
│   │   ├── deps.py               # 依赖注入
│   │   └── v1/                   # API v1 版本
│   │       ├── __init__.py
│   │       ├── events.py         # 事件 API
│   │       ├── sources.py        # 数据源 API
│   │       ├── heatmap.py        # 热力图 API
│   │       ├── admin.py          # 管理员 API
│   │       ├── auth.py           # 认证 API
│   │       └── feedback.py       # 反馈 API
│   │
│   ├── services/                 # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── event_service.py      # 事件业务逻辑
│   │   ├── source_service.py     # 数据源业务逻辑
│   │   └── alert_service.py      # 告警业务逻辑
│   │
│   ├── integrations/             # 外部集成
│   │   ├── __init__.py
│   │   ├── llm/                  # LLM 集成
│   │   │   ├── __init__.py
│   │   │   ├── base.py           # LLM 基类
│   │   │   └── deepseek.py       # DeepSeek 实现
│   │   └── sources/              # 数据源集成
│   │       ├── __init__.py
│   │       ├── base.py           # 数据源基类
│   │       ├── gnews.py          # GNews
│   │       ├── newsapi.py        # NewsAPI
│   │       ├── acled.py          # ACLED
│   │       ├── rsshub.py         # RSSHub
│   │       └── firms.py          # NASA FIRMS
│   │
│   ├── tasks/                    # 后台任务
│   │   ├── __init__.py
│   │   ├── scheduler.py          # 任务调度器
│   │   └── ingestion.py          # 数据采集任务
│   │
│   └── utils/                    # 工具函数
│       ├── __init__.py
│       ├── dedup.py              # 去重工具
│       ├── quota.py              # 配额管理
│       └── logger.py             # 日志工具
│
├── tests/                         # 测试目录
│   ├── __init__.py
│   ├── conftest.py               # pytest 配置
│   ├── test_api/                 # API 测试
│   ├── test_services/            # 服务测试
│   └── test_integrations/        # 集成测试
│
├── requirements.txt              # Python 依赖
├── .env.example                  # 环境变量示例
└── README.md                     # 后端文档
```

## 模块说明

### 1. core/ - 核心功能
- **config.py**: 集中管理所有配置，使用 pydantic-settings
- **database.py**: 数据库连接、会话管理、初始化
- **security.py**: JWT 认证、权限管理
- **exceptions.py**: 自定义异常类，统一错误处理

### 2. models/ - 数据模型
- **database.py**: SQLAlchemy ORM 模型定义
  - Source, SourceUsage, RawItem, Event, Alert, Feedback

### 3. schemas/ - API 模式
- **event.py**: 事件相关的请求/响应模式
- **source.py**: 数据源相关的模式
- **alert.py**: 告警相关的模式
- **common.py**: 通用模式（反馈、统计、认证等）

### 4. api/ - API 路由层
- **deps.py**: 依赖注入（数据库会话等）
- **v1/**: API v1 版本的所有路由
  - 按功能和资源组织，而不是按 HTTP 方法

### 5. services/ - 业务逻辑层
- **event_service.py**: 事件相关的业务逻辑
- **source_service.py**: 数据源管理业务逻辑
- **alert_service.py**: 告警发送和管理

### 6. integrations/ - 外部集成
- **llm/**: LLM 服务集成
  - 支持多种 LLM 提供商的统一接口
- **sources/**: 数据源集成
  - 每个数据源一个独立模块
  - 继承自基类，统一接口

### 7. tasks/ - 后台任务
- **scheduler.py**: APScheduler 配置
- **ingestion.py**: 数据采集任务逻辑

### 8. utils/ - 工具函数
- **dedup.py**: 去重算法
- **quota.py**: 配额管理
- **logger.py**: 日志配置

## 重构优势

### 1. 模块化
- 每个模块有明确的职责
- 降低耦合度，便于测试和维护

### 2. 可扩展性
- 添加新的数据源只需在 integrations/sources/ 添加新文件
- 添加新的 LLM 只需在 integrations/llm/ 添加新实现
- API 版本管理清晰（api/v1/, api/v2/）

### 3. 关注点分离
- **API 层**: 处理 HTTP 请求/响应
- **Service 层**: 业务逻辑
- **Integration 层**: 外部服务调用
- **Model 层**: 数据持久化

### 4. 易于测试
- 每个模块可以独立测试
- 依赖注入使 mock 更容易
- 清晰的边界定义测试范围

### 5. 团队协作
- 多人可以并行开发不同模块
- 代码冲突更少
- 更容易代码审查

## 迁移步骤

### 阶段 1: 创建新结构（当前）
- ✅ 创建新的目录结构
- ✅ 创建核心模块

### 阶段 2: 迁移现有代码
- 迁移 models/
- 迁移 schemas/
- 迁移 API 路由
- 迁移 services/
- 迁移 integrations/

### 阶段 3: 更新导入
- 更新所有 import 语句
- 确保没有循环依赖

### 阶段 4: 测试
- 运行现有测试
- 添加新的测试

### 阶段 5: 清理
- 删除旧的文件
- 更新文档

## 依赖关系

```
main.py
  ↓
api/v1/*.py (路由层)
  ↓
services/*.py (业务逻辑层)
  ↓
integrations/*.py (外部集成层)
  ↓
models/ (数据模型)
```

## 配置管理

所有配置集中在 `core/config.py`：
- 使用 pydantic-settings 自动加载环境变量
- 类型安全的配置访问
- 支持配置验证

## 错误处理

统一使用自定义异常（`core/exceptions.py`）：
- DatabaseException
- SourceException
- QuotaException
- LLMException
- AlertException

API 层捕获异常并转换为适当的 HTTP 响应。
