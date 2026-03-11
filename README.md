# skinsight-core
High-performance event-driven market quantitative analysis system built with FastAPI, TimescaleDB and Polars. Designed for real-time ingestion, replayable time-series analysis and strategy research.
# 一项目结构
```
skinsight-core/
├── docker-compose.yml          # [核心] 基础设施编排 (DB, Web)
├── pyproject.toml              # [核心] 依赖管理
├── README.md                   # 项目文档
├── .env                        # 环境变量 (API Key, DB URL)
│
├── scripts/                    # 运维脚本
│   └── init_db.sql             # [核心] 数据库初始化 (Hypertable DDL)
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # [核心] FastAPI 入口
│   │
│   ├── core/                   # 基础设施层
│   │   ├── config.py           # 配置加载 (Pydantic Settings)
│   │   ├── database.py         # 数据库连接池
│   │   └── logging.py          # 日志配置
│   │
│   ├── services/               # 业务逻辑层
│   │   ├── ingestion/          # >> 采集模块
│   │   │   ├── client.py       # [核心] Httpx 客户端封装
│   │   │   └── fetcher.py      # 具体 API 解析逻辑
│   │   │
│   │   └── quant/              # >> 量化模块
│   │       ├── engine.py       # Polars 计算引擎
│   │       └── indicators.py   # RSI/MA 纯算法实现
│   │
│   ├── api/                    # 接口层
│   │   └── v1/
│   │       └── endpoints.py    # 定义 URL 路由
│   │
│   └── models/                 # 数据模型层
│       ├── sql_models.py       # SQLAlchemy 数据库表定义
│       └── schemas.py          # Pydantic 数据校验模型

```