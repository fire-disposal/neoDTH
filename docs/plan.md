
## 介绍

neoDTH 是一个基于 FastAPI 的新一代数字孪生健康信息系统（neo Digital Twin Health）。
它旨在通过现代化架构与高质量代码实践，探索多源异构健康数据的融合、分析与智能建模新范式。
项目规模小而精，但以可复用、可扩展、可验证为核心目标，成为未来医疗健康数字孪生系统的原型与技术验证平台。

托管仓库：github 

## 🗂 neoDTH 项目文件树与开发指南

```
neoDTH-backend/
├── README.md                   # 项目说明
├── requirements.txt            # Python 依赖
├── pyproject.toml / setup.cfg  # 可选，现代项目配置
├── main.py                     # 启动入口
├── config.py                   # 全局配置（数据库、MQ、端口等）
├── src/
│   ├── core/
│   │   ├── event_bus.py        # 事件总线实现
│   │   ├── settings.py         # Pydantic 配置管理
│   │   └── logger.py           # 日志工具
│   │
│   ├── domain/
│   │   ├── shared/             # 通用实体、接口
│   │   │   ├── base_model.py
│   │   │   └── repository.py
│   │   ├── heart_rate/
│   │   │   ├── events.py
│   │   │   └── models.py
│   │   ├── temperature/
│   │   │   ├── events.py
│   │   │   └── models.py
│   │   └── sleep/
│   │       ├── events.py
│   │       └── models.py
│   │
│   ├── services/
│   │   ├── heart_rate_processor.py
│   │   ├── temperature_processor.py
│   │   ├── sleep_processor.py
│   │   └── aggregators/
│   │       └── health_combiner.py
│   │
│   ├── adapters/
│   │   ├── pg_repository/
│   │   │   ├── pgsql_client.py
│   │   │   ├── heart_rate_repo.py
│   │   │   └── temperature_repo.py
│   │   ├── influx_repository/
│   │   │   ├── influx_client.py
│   │   │   └── metrics_repo.py
│   │   ├── tcp_gateway/
│   │   │   ├── server.py
│   │   │   └── handler.py
│   │   └── mqtt_gateway/
│   │       ├── client.py
│   │       └── handler.py
│   │
│   └── api/
│       ├── routes/
│       │   ├── patient.py
│       │   └── data_ingress.py
│       └── dependencies.py
│
└── tests/
    ├── test_event_bus.py
    ├── test_tcp_gateway.py
    ├── test_mqtt_gateway.py
    ├── test_http_api.py
    └── test_processors.py
```

---

## 📌 各模块职责与开发指示

### 1. **core/**

- **event_bus.py**

  - 异步事件总线，支持订阅/发布事件。
  - 初期使用内存实现，后续可替换 Kafka/RabbitMQ。
- **settings.py**

  - Pydantic Settings 管理 DB/MQ/端口/日志等配置。
- **logger.py**

  - 统一日志输出工具，支持模块名与事件类型标记。

---

### 2. **domain/**

- **shared/**

  - `base_model.py`: 所有事件/实体基类。
  - `repository.py`: 定义接口，不依赖数据库实现。
- **heart_rate/temperature/sleep/**

  - `events.py`: 定义指标事件（DataReceived, HighAlert 等）。
  - `models.py`: 定义实体结构（patient_id, device_id, value, timestamp）。

---

### 3. **services/**

- **heart_rate_processor.py / temperature_processor.py / sleep_processor.py**

  - 核心业务逻辑。
  - 方法: `handle_data_received(event)` → 写入 InfluxDB + PGSQL + 触发派生事件。
- **aggregators/health_combiner.py**

  - 订阅多个指标事件，生成复合事件（如发热伴心动过速）。
  - 支持简单规则判断，易于扩展。

---

### 4. **adapters/**

- **pg_repository/**

  - PostgreSQL 客户端 + 各指标 Repo。
  - 提供 `ensure_channel()`, `write_event_log()` 等方法。
- **influx_repository/**

  - InfluxDB 客户端 + 时序写入/查询方法。
- **tcp_gateway/**

  - TCP 服务器 + msgpack 解码 + 事件发布。
  - 高频采集设备入口。
- **mqtt_gateway/**

  - MQTT 客户端 + JSON decode + 事件发布。
  - IoT 传感器入口。

---

### 5. **api/**

- **routes/patient.py**

  - 查询患者信息、通道信息。
- **routes/data_ingress.py**

  - HTTP POST 数据接入入口。
  - 发布事件到 EventBus。

---

### 6. **main.py**

- 初始化 FastAPI app。
- 初始化 EventBus。
- 注册各 Processor。
- 启动 TCP、MQTT、HTTP 三种数据接入。

---

### 7. **tests/**

- 针对 EventBus、各 Gateway、Processor、HTTP API 做单元/集成测试。
- 保证核心事件流正确。

---

## ⚙️ 初期开发目标（迭代式）

| 阶段 | 内容              | 输出目标                                                         |
| -- | --------------- | ------------------------------------------------------------ |
| 1  | 环境搭建            | FastAPI + PostgreSQL + InfluxDB + asyncio-mqtt + msgpack TCP |
| 2  | 核心事件 &实体        | domain/ 各指标事件定义完成                                            |
| 3  | Repository & DB | PGSQL / Influx 写入/查询方法完成                                     |
| 4  | Processor       | 心率/体温数据处理逻辑完成，触发警报事件                                         |
| 5  | TCP Gateway     | Msgpack TCP 数据接入并发布事件                                        |
| 6  | MQTT Gateway    | MQTT 数据接入并发布事件                                               |
| 7  | HTTP API        | 数据接入与查询接口完成                                                  |
| 8  | Aggregator      | 简单跨指标组合事件逻辑完成                                                |
| 9  | 测试              | 核心事件流单元测试覆盖 >80%                                             |

---

## 📌 额外建议

1. **事件总线作为核心**，所有数据入口只负责解析 → 发布事件 → Processor 消费。
2. **高频数据优先写入 InfluxDB**，PGSQL 只保留元数据与事件日志。
3. **新增指标仅需**：

   - domain/ 新建事件 + model
   - services/ 新建 processor
   - adapters/ 订阅事件即可
4. **单独 TCP/MQTT 入口**方便后续微服务拆分，且不破坏现有 FastAPI 主流程。

---
