# 调研发现 — skinsight-core

## 研究笔记
<!-- 实施过程中发现的信息：API 文档、约束条件、技术备注 -->

### TimescaleDB
- 使用 `timescale/timescaledb:latest-pg16` 镜像（基于 PostgreSQL 16）
- 超表分块策略待根据数据量确定
- `init_db.sql` 挂载到 `/docker-entrypoint-initdb.d` 实现自动初始化

### 依赖（来自 pyproject.toml）
- **arq** + **redis**：后台任务队列（可能用于定时采集）
- **aiolimiter**：外部 API 调用的速率限制
- **tenacity**：API 调用的重试逻辑
- **prometheus-client**：指标暴露
- **orjson**：快速 JSON 序列化

### API 数据源
- `init_db.sql` 中提及"测试 API"——实际的外部行情 API 尚待确认
- `base.json` 和 `formatted_base.json` 位于项目根目录——可能是 API 返回的样例数据，用于设计数据库模式
- 数据涉及四大平台的 CS:GO/CS2 饰品：**C5**、**BUFF**、**YOUPIN**、**HALOSKINS**
- 每个饰品包含 `name`（中文名）、`marketHashName`（英文市场名）、以及各平台的 `itemId`
- `formatted_base.json` 共约 18MB，包含大量饰品数据

### 项目状态（2026-05-26）
- 分支：`feat/docker-db-setup`
- 工作区有修改：`docker-compose.yml` 已修改，`scripts/init_db.sql` 已修改（未暂存）
- 所有 `.py` 源文件均为空桩（0 行）
- README 中列出的所有目录已存在 `__init__.py` 包文件
