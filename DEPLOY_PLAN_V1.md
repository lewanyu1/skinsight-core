# skinsight-core 开发计划 & 云服务器部署分析

## Context

项目当前状态：**脚手架已搭建，代码 0% 实现**。目录结构、依赖声明、Docker 配置、API 文档爬取均已完成，但所有 `app/` 下的 Python 文件都是空的。需要从 Phase 1 开始逐步实现。

---

## 一、云服务器部署可行性分析

### 服务器配置

| 资源 | 配置 | 评估 |
|------|------|------|
| CPU | 2 核 | ⚠️ 够用，但并发计算受限 |
| 内存 | 4 GB | ⚠️ 紧张，需要精细控制 |
| 系统盘 | 60 GB SSD | ✅ 足够 |
| 流量 | 500 GB/月 | ✅ 充裕 |
| 带宽 | 5 Mbps | ⚠️ 够用，但批量数据传输慢 |

### 内存预算分析

| 组件 | 预估内存 | 说明 |
|------|----------|------|
| TimescaleDB | ~800 MB | PostgreSQL 基础 + TimescaleDB 扩展 |
| FastAPI (uvicorn) | ~150 MB | 2 worker 进程 |
| Redis (任务队列) | ~100 MB | arq 需要 |
| Polars 计算 | ~500 MB | DataFrame 峰值，取决于数据量 |
| 系统开销 | ~500 MB | OS + 缓冲 |
| **总计** | **~2 GB** | **剩余 ~2 GB 余量** |

### 结论：**可行，但需要优化**

**可行的理由：**
- 数据量可控：CS2 饰品约 5-10 万个，价格快照单次 ~2MB JSON
- 计算不密集：Polars 本身就是 Rust 引擎，CPU 利用率高
- 网络需求低：API 调用频率有限，5Mbps 足够

**需要做的优化：**
1. TimescaleDB 内存限制：`shared_buffers=256MB`, `work_mem=16MB`
2. uvicorn worker 数量：设为 2（匹配 CPU 核数）
3. Polars 数据分批处理，避免一次性加载全量
4. 定时清理旧数据，控制磁盘占用
5. 添加 swap 分区（2GB）作为内存安全网

---

## 二、开发路线图

### Phase 1：核心基础设施（预计 2-3 小时）

**目标：应用能启动，数据库能连接**

1. **`app/core/config.py`** - Pydantic Settings 配置
   - 数据库连接串、Redis 连接串
   - SteamDT API 基础 URL、API Key
   - 日志级别、worker 数量
   - **验证**: `python -c "from app.core.config import settings; print(settings)"`

2. **`app/core/database.py`** - AsyncEngine + session 工厂
   - SQLAlchemy async engine (asyncpg)
   - sessionmaker 工厂函数
   - **验证**: 能获取 session 并执行 `SELECT 1`

3. **`app/core/logging.py`** - 结构化日志
   - JSON 格式输出（生产环境）
   - 控制台彩色输出（开发环境）
   - **验证**: 日志输出格式正确

4. **`scripts/init_db.sql`** - 数据库表结构
   - `market_snapshots` (TimescaleDB hypertable)
   - `item_base_info` (饰品基础信息)
   - `broad_market_index` (大盘指数)
   - **验证**: 表创建成功，hypertable 转换成功

5. **`app/main.py`** - FastAPI 入口
   - lifespan 管理（启动/关闭事件）
   - CORS 中间件
   - 健康检查端点 `/health`
   - **验证**: `uvicorn app.main:app` 启动成功，`/health` 返回 200

### Phase 2：数据模型（预计 1-2 小时）

**目标：数据能存入数据库**

1. **`app/models/sql_models.py`** - SQLAlchemy ORM
   - `MarketSnapshot` - 价格快照（平台、价格、数量）
   - `ItemBaseInfo` - 饰品基础信息（marketHashName、平台映射）
   - `BroadMarketIndex` - 大盘指数数据
   - `WearData` - 磨损数据（float、贴纸、挂件）

2. **`app/models/schemas.py`** - Pydantic 模型
   - 请求/响应模型
   - 与 SteamDT API 返回结构对齐

3. **验证**: 能通过 ORM 插入和查询数据

### Phase 3：数据采集服务（预计 3-4 小时）

**目标：能从 SteamDT API 拉取数据并存储**

1. **`app/services/ingestion/client.py`** - HTTP 客户端
   - httpx AsyncClient 封装
   - 速率限制（aiolimiter）
   - 重试逻辑（tenacity）
   - API Key 鉴权

2. **`app/services/ingestion/fetcher.py`** - 数据解析
   - 解析各 API 响应
   - 数据标准化（平台名统一、价格单位统一）
   - 批量写入数据库

3. **验证**: 能调用 `/open/cs2/v1/base` 获取饰品列表，调用 `/open/cs2/v1/price/single` 获取价格

### Phase 4：量化计算引擎（预计 2-3 小时）

**目标：能计算技术指标**

1. **`app/services/quant/indicators.py`** - 指标算法
   - RSI（相对强弱指数）
   - MA（移动平均线）
   - 布林带
   - 价格变化率

2. **`app/services/quant/engine.py`** - 计算引擎
   - Polars DataFrame 操作
   - 时间序列对齐
   - 批量计算

3. **验证**: 对已有数据计算 RSI，结果合理

### Phase 5：API 接口层（预计 2-3 小时）

**目标：对外提供 REST API**

1. **`app/api/v1/endpoints.py`** - 路由定义
   - `GET /api/v1/items` - 饰品列表
   - `GET /api/v1/items/{name}/price` - 价格查询
   - `GET /api/v1/items/{name}/kline` - K线数据
   - `GET /api/v1/items/{name}/indicators` - 技术指标
   - `GET /api/v1/market/index` - 大盘指数
   - `POST /api/v1/ingest/trigger` - 手动触发数据采集

2. **验证**: Swagger UI 可访问，各端点返回正确数据

### Phase 6：集成测试 & 部署（预计 2-3 小时）

**目标：完整流程跑通，可部署**

1. Dockerfile 编写（多阶段构建，减小镜像体积）
2. docker-compose.yml 补充（app + timescaledb + redis）
3. 定时任务配置（arq worker，定时采集价格）
4. Prometheus metrics 端点
5. 完整流程测试：采集 → 存储 → 计算 → 查询

---

## 三、部署架构（2核4G 服务器）

```
┌─────────────────────────────────────────┐
│              Docker Compose             │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │TimescaleDB│  │ FastAPI  │  │ Redis │ │
│  │  ~800MB   │  │ ~150MB   │  │~100MB │ │
│  │  port:5432│  │ port:8000│  │port:6379│
│  └──────────┘  └──────────┘  └───────┘ │
│       │              │            │     │
│       └──────────────┴────────────┘     │
│              共享网络                    │
└─────────────────────────────────────────┘
         │
    Nginx 反向代理 (可选)
         │
    外部访问 :80/:443
```

### 关键配置建议

```yaml
# docker-compose.yml 资源限制
services:
  timescaledb:
    deploy:
      resources:
        limits:
          memory: 1G
    command: >
      postgres
        -c shared_buffers=256MB
        -c work_mem=16MB
        -c maintenance_work_mem=128MB
        -c max_connections=50

  app:
    deploy:
      resources:
        limits:
          memory: 512M
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2

  redis:
    deploy:
      resources:
        limits:
          memory: 128M
    command: redis-server --maxmemory 100mb --maxmemory-policy allkeys-lru
```

---

## 四、执行顺序

| 步骤 | 任务 | 预计时间 | 依赖 |
|------|------|----------|------|
| 1 | config.py + logging.py | 30min | 无 |
| 2 | database.py + init_db.sql | 45min | 步骤1 |
| 3 | sql_models.py + schemas.py | 45min | 步骤2 |
| 4 | main.py (健康检查) | 30min | 步骤2 |
| 5 | client.py (HTTP 客户端) | 60min | 步骤1 |
| 6 | fetcher.py (数据解析) | 90min | 步骤3,5 |
| 7 | indicators.py | 45min | 无 |
| 8 | engine.py | 45min | 步骤7 |
| 9 | endpoints.py | 60min | 步骤6,8 |
| 10 | Dockerfile + 部署 | 60min | 步骤4 |
| **总计** | | **~8 小时** | |

---

## 五、验证方式

每个 Phase 完成后的验证：

1. **Phase 1**: `curl localhost:8000/health` → 200 OK
2. **Phase 2**: 通过 psql 插入测试数据，查询成功
3. **Phase 3**: 日志显示数据采集成功，数据库有新记录
4. **Phase 4**: 调用计算接口，返回合理的 RSI 值（0-100）
5. **Phase 5**: Swagger UI 可访问，所有端点响应正确
6. **Phase 6**: Docker Compose 启动成功，完整流程跑通

---

## 六、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 内存不足 | OOM Kill | 限制各组件内存 + 添加 swap |
| API 限流 | 数据采集失败 | tenacity 重试 + 速率限制 |
| 磁盘满 | 服务崩溃 | 定时清理 + 监控告警 |
| Python 版本 | 兼容性问题 | 确认服务器 Python >=3.12 |
