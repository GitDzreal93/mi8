**标题** 基于免费/低成本 API 的军事态势感知系统（本地运行，外部 DeepSeek LLM，Docker Postgres）

**概要**
- 在本地单机环境运行的采集+处理+可视化系统，依赖已部署的 Docker Postgres。
- 所有智能结构化调用 DeepSeek 云端模型（无需本地 GPU），其他数据源均使用免费或低成本 API。
- 目标：24–72 小时军事热点的结构化聚合、地图展示与告警。

**核心约束调整**
- LLM：使用 DeepSeek API（建议 deepseek-chat / deepseek-reasoner 视成本与质量而定），通过 Instructor/Pydantic 约束返回 JSON。
- 部署：仅需本地可跑；不关心云上上架。依赖：Docker Postgres 已就绪；其余组件用本地容器或进程即可。
- 成本：优先免费额度；DeepSeek 按调用计费，需添加 QPS 与 token 上限保护。

**功能需求（更新版）**
- 数据源：GNews 100次/日；NewsAPI 100次/日；ACLED（key）；RSSHub（防部等）；NASA FIRMS；可选 ADS-B Exchange 社区源。
- 轮询：每30分钟；80% 配额即停并告警；pageSize 最大化；按源限速。
- 去重：标准化标题+源+日期哈希；嵌入相似度（可用开源嵌入或 DeepSeek embeddings）二次过滤；生成 canonical_event_id。
- LLM 结构化：Instructor + DeepSeek，将原文转为 schema {event_type, importance 1–5, location(lat,lng,precision), actors, equipment, casualties?, tags[], summary_en, summary_zh, event_time, confidence}；低置信度标记人工复核。
- 存储：Postgres+PostGIS（Docker 内）。表：events、sources、raw_items、tags、alerts。
- API（FastAPI，本地）：GET /events（时间/区域/国家/重要度/关键词），GET /events/{id}，GET /heatmap（GeoJSON/tiles），GET /sources/health，POST /feedback；本地 JWT（可简单密钥）或本地 SSO 代理留空。
- 前端（Next.js+Leaflet/OSM）：热力/聚合点地图；时间窗滑杆（默认24h，至7d）；过滤器；列表与详情；源健康；手动刷新；中英双语。
- 告警：importance≥4 命中关注区域或量级突增时发送本地邮箱/Slack Webhook（可选）。
- 运维：配额监控；raw 回放；开关控制 ADS-B/FIRMS。

**非功能**
- 延迟：读 API p95 ≤ 800ms（含本地缓存）；采集到可用 ≤ 5 分钟。
- 可用性：在单机情况下，源失败需降级但不阻塞整体。
- 成本：DeepSeek 调用设每日 token/QPS 上限；其他源按免费额度封顶；地图瓦片缓存。
- 安全：本地环境可简化为静态 JWT 秘钥；如需 SSO 可后续接入；审计日志写本地。

**数据流**
- 调度器 → 拉取各源 → 入队（Redis/Celery 或本地队列）→ DeepSeek 结构化 → 去重 → 写 Postgres/PostGIS → 缓存（Redis 可选）→ API → 前端 Leaflet 渲染。
- 回填：可选 ACLED 近30天批量导入，由开关控制。

**测试与验收**
- 单测：各源解析；LLM schema 校验（使用 DeepSeek mock/录制）；去重哈希与相似度阈值。
- 集成：录制夹具的端到端采集；API OpenAPI 合同；（可选）本地 SSO/静态 JWT 流程。
- 性能：/events 与 /heatmap 在缓存/非缓存模式下压测；采集在配额保护下运行。
- UX：宽带下 2 秒内渲染前 50 条；中英切换完整；地图交互流畅。
- 告警：模拟高重要度事件，验证邮件/Slack 仅一次且内容正确。

**假设**
- Docker Postgres 已启动并开放连接；可启用 PostGIS 扩展。
- 本地网络可访问 DeepSeek 与各 API。
- OSM 瓦片本地使用合规；无需 Mapbox token。
- 并发与用户量较小（≤50 RPS，≤200 内部用户）。
