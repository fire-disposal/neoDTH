# neoDTH 数据总线与双数据库协作机制设计

## 1. 事件总线（EventBus）

- 统一异步事件流，所有数据入口（TCP/MQTT/HTTP）解析后发布事件，Processor消费事件并写入数据库。
- 支持事件订阅/发布，便于扩展与测试。
- 详见 [`src/core/event_bus.py`](src/core/event_bus.py:1)。

## 2. 双数据库协作机制

- **InfluxDB**：存储高频时序数据（如心率、体温原始采集值），适合大数据量、实时分析。
- **PostgreSQL**：存储患者主数据、事件日志、告警、元数据，便于事务管理与复杂查询。
- Processor收到事件后，先写入InfluxDB（原始数据），再写入PGSQL（事件日志/元数据）。
- 通过唯一标识（如 patient_id, device_id, timestamp）实现双库数据关联。

## 3. 患者模型设计

- 见 [`src/domain/patient/models.py`](src/domain/patient/models.py:1)，建议包含基本信息、设备绑定、索引字段。
- 事件模型（如HeartRateDataReceived）应包含patient_id、device_id、timestamp等，便于跨库映射。

## 4. 数据库连接与初始化

- [`src/adapters/pg_repository/pgsql_client.py`](src/adapters/pg_repository/pgsql_client.py:1)：PGSQL连接池，支持自动建表、连接管理。
- [`src/adapters/influx_repository/influx_client.py`](src/adapters/influx_repository/influx_client.py:1)：InfluxDB连接与初始化。
- 配置统一由 [`src/core/settings.py`](src/core/settings.py:1) 管理，支持多环境切换。

## 5. 双库关联映射机制

- 事件处理时，Processor将同一事件的核心字段同步写入两库。
- 查询时，先查PGSQL获取元数据，再查InfluxDB获取时序明细，或通过patient_id/device_id/timestamp联合查询。

## 6. 机制完善建议

- 明确各Processor的写入逻辑，保证幂等性与一致性。
- 增加数据库健康检查与重连机制。
- 完善患者模型与事件模型的注释与文档。
- 持续补充单元测试，确保端到端数据流正确。

---
本设计文档建议与代码持续同步维护，便于团队理解与扩展。