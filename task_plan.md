# 任务计划 — skinsight-core

## 目标
实现一个高性能事件驱动的 CS:GO/CS2 饰品市场量化分析系统，基于 FastAPI + TimescaleDB + Polars，支持实时数据采集、可回放的时间序列分析和策略研究。

## 当前状态
- `pyproject.toml`：依赖已声明（FastAPI、Polars、SQLAlchemy、asyncpg、httpx、Redis/arq 等）
- `docker-compose.yml`：TimescaleDB 服务已配置
- `app/` 包结构已创建，含 `__init__.py` 文件
- 所有核心模块（`main.py`、`config.py`、`database.py`、`sql_models.py`、`schemas.py`）均为**空文件**
- `scripts/init_db.sql`：不完整（仅有注释）
- 缺失：`logging.py`、采集模块、量化模块、API 端点
- 测试 API 返回数据样例见于 `base.json` 和 `formatted_base.json`

## 实施阶段

### 阶段 1 — 核心基础设施（地基）
**目标：** 让应用可启动，具备数据库连接和配置能力。

- [ ] 1.1 实现 `app/core/config.py` — Pydantic Settings（数据库 URL、Redis URL、API 密钥等）
- [ ] 1.2 实现 `app/core/database.py` — SQLAlchemy 异步引擎 + TimescaleDB 会话工厂
- [ ] 1.3 实现 `app/core/logging.py` — 结构化日志配置
- [ ] 1.4 实现 `app/main.py` — FastAPI 应用工厂，含 lifespan（连接/断开数据库）

### 阶段 2 — 数据模型与数据库模式
**目标：** 定义 TimescaleDB 模式及对应的 ORM/Pydantic 模型。

- [ ] 2.1 完成 `scripts/init_db.sql` — `market_snapshots` 超表 DDL、索引
- [ ] 2.2 实现 `app/models/sql_models.py` — 与数据库模式匹配的 SQLAlchemy ORM 模型
- [ ] 2.3 实现 `app/models/schemas.py` — Pydantic 请求/响应校验模型

### 阶段 3 — 采集服务
**目标：** 从外部 API 获取市场数据并持久化到 TimescaleDB。

- [ ] 3.1 实现 `app/services/ingestion/client.py` — httpx 异步客户端，含速率限制、重试（tenacity）、错误处理
- [ ] 3.2 实现 `app/services/ingestion/fetcher.py` — 各平台 API 解析器，数据规范化转为数据库模型

### 阶段 4 — 量化引擎
**目标：** 基于 Polars 的计算引擎，用于技术指标和策略回测。

- [ ] 4.1 实现 `app/services/quant/indicators.py` — RSI、MA 等 Polars 技术指标
- [ ] 4.2 实现 `app/services/quant/engine.py` — 查询数据库 → Polars DataFrame → 计算 → 输出管线

### 阶段 5 — API 层
**目标：** 暴露 REST 端点用于数据查询和分析。

- [ ] 5.1 实现 `app/api/v1/endpoints.py` — 行情查询、指标计算、采集触发等路由

### 阶段 6 — 集成与验证
**目标：** 端到端串联、测试和文档。

- [ ] 6.1 在 `main.py` 中串联所有模块（路由注册、lifespan）
- [ ] 6.2 端到端测试：数据库初始化 → 数据采集 → 查询 → 指标计算
- [ ] 6.3 验证 docker-compose 从零开始可正常运行

---

## 决策记录
<!-- 在此记录架构决策 -->

| # | 决策 | 理由 | 日期 |
|---|------|------|------|
|   |      |      |      |
