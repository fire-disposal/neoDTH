# 未实现/待完善功能清单

- [ ] 健康事件聚合器（services/aggregators/health_combiner.py）
- [ ] 心率数据仓储（adapters/pg_repository/heart_rate_repo.py）
- [ ] 体温数据仓储（adapters/pg_repository/temperature_repo.py）
- [ ] 时序数据仓储（adapters/influx_repository/metrics_repo.py）
- [x] TCP 服务器（adapters/tcp_gateway/server.py）
- [x] TCP 处理器（adapters/tcp_gateway/handler.py）
- [x] MQTT 客户端（adapters/mqtt_gateway/client.py）
- [x] MQTT 处理器（adapters/mqtt_gateway/handler.py）
- [ ] 患者信息接口（api/routes/patient.py）
- [ ] 数据接入接口（api/routes/data_ingress.py）
- [ ] 依赖注入配置（api/dependencies.py）
- [x] 核心单元/集成测试（tests/）
- [ ] 环境搭建与依赖配置（FastAPI、PostgreSQL、InfluxDB、MQTT、TCP 支持）

---

## 2025-10-05 项目初步可用性评估与推荐实现目标

### 现有未实现/待完善模块
1. 健康事件聚合器 [`src/services/aggregators/health_combiner.py`](src/services/aggregators/health_combiner.py:1)
2. 心率数据仓储 [`src/adapters/pg_repository/heart_rate_repo.py`](src/adapters/pg_repository/heart_rate_repo.py:1)
3. 体温数据仓储 [`src/adapters/pg_repository/temperature_repo.py`](src/adapters/pg_repository/temperature_repo.py:1)
4. 时序数据仓储 [`src/adapters/influx_repository/metrics_repo.py`](src/adapters/influx_repository/metrics_repo.py:1)
5. TCP 服务器 [`src/adapters/tcp_gateway/server.py`](src/adapters/tcp_gateway/server.py:1)
6. TCP 处理器 [`src/adapters/tcp_gateway/handler.py`](src/adapters/tcp_gateway/handler.py:1)
7. MQTT 客户端 [`src/adapters/mqtt_gateway/client.py`](src/adapters/mqtt_gateway/client.py:1) ✅
8. MQTT 处理器 [`src/adapters/mqtt_gateway/handler.py`](src/adapters/mqtt_gateway/handler.py:1) ✅
9. 患者信息接口 [`src/api/routes/patient.py`](src/api/routes/patient.py:1)
10. 数据接入接口 [`src/api/routes/data_ingress.py`](src/api/routes/data_ingress.py:1)
11. 依赖注入配置 [`src/api/dependencies.py`](src/api/dependencies.py:1)
12. 核心单元/集成测试（tests/，已补充MQTT相关测试）
13. 环境搭建与依赖配置（FastAPI、PostgreSQL、InfluxDB、MQTT、TCP 支持）

### 推荐实现目标与优先级
1. 完善核心数据流（数据采集、存储、聚合、API 接口）
2. 实现 TCP/MQTT 通信链路
3. 健全依赖注入与配置
4. 增加单元/集成测试
5. 完善环境搭建文档与自动化脚本

> 建议优先补全上述核心模块，确保系统端到端可用性，再逐步完善测试与文档。
> 本清单自动生成，建议开发过程中持续维护与补充。