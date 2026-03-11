# 后端项目启动指南

## 数据库配置

✅ **数据库已创建并初始化**

- 数据库名: `mi8`
- 用户: `admin`
- 密码: `Postgres@2026`
- 主机: `localhost`
- 端口: `5432`

## 数据库表结构

已创建以下表：

1. **sources** - 数据源配置和状态
2. **source_usage** - 数据源配额使用情况
3. **raw_items** - 原始数据条目
4. **events** - 结构化事件数据
5. **alerts** - 告警记录
6. **feedback** - 用户反馈

## 后端服务启动

### 方法一：直接启动

```bash
cd /Volumes/dz/code/MI8/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### 方法二：使用启动脚本

```bash
cd /Volumes/dz/code/MI8
./start.sh
```

## 服务地址

启动成功后，可以访问：

- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API 端点测试

### 测试根端点
```bash
curl http://localhost:8000/
```

### 测试事件列表
```bash
curl http://localhost:8000/events
```

### 测试源健康状态
```bash
curl http://localhost:8000/sources/health
```

### 测试系统统计
```bash
curl http://localhost:8000/admin/stats
```

## 数据库连接

### 直接连接 PostgreSQL

```bash
docker exec -it postgresql psql -U admin -d mi8
```

### 查询所有表

```sql
\dt
```

### 查看表结构

```sql
\d events
\d sources
\d raw_items
```

### 查询事件数据

```sql
SELECT COUNT(*) FROM events;
SELECT * FROM events ORDER BY created_at DESC LIMIT 10;
```

## 配置文件

环境变量配置在 `.env` 文件中：

```bash
# 数据库连接
DATABASE_URL=postgresql+asyncpg://admin:Postgres%402026@localhost:5432/mi8

# DeepSeek LLM
DEEPSEEK_API_KEY=your_key_here

# 数据源 API Keys
GNEWS_API_KEY=your_key_here
NEWSAPI_API_KEY=your_key_here
ACLED_API_KEY=your_key_here
```

## 后台服务

后端包含一个定时任务，每 30 分钟自动采集数据：

- 轮询多个数据源
- 使用 DeepSeek LLM 进行结构化
- 自动去重和存储
- 配额管理和保护

查看调度器状态：
```bash
curl http://localhost:8000/sources/health
```

## 停止服务

按 `Ctrl+C` 停止后端服务。

如果使用启动脚本，脚本会自动停止前后端服务。

## 故障排除

### 数据库连接失败

```bash
# 检查 PostgreSQL 容器状态
docker ps | grep postgresql

# 启动 PostgreSQL 容器
docker start postgresql
```

### 端口已被占用

```bash
# 查看端口占用
lsof -i :8000

# 更改端口
uvicorn app.main:app --reload --port 8001
```

### 重新创建数据库

```bash
# 删除数据库
docker exec postgresql psql -U admin -d postgres -c "DROP DATABASE mi8;"

# 重新创建
docker exec postgresql psql -U admin -d postgres -c "CREATE DATABASE mi8;"

# 重新初始化表
cd backend
source venv/bin/activate
python -m app.db
```

## 下一步

1. 配置数据源 API Keys（在 `.env` 文件中）
2. 启动前端服务
3. 访问 http://localhost:3000 查看仪表板
