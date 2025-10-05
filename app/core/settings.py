from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # 基础配置
    app_name: str = "neoDTH"
    debug: bool = True

    # PostgreSQL 配置
    pg_host: str = Field("localhost", env="PG_HOST")
    pg_port: int = Field(5432, env="PG_PORT")
    pg_user: str = Field("neo_user", env="PG_USER")
    pg_password: str = Field("neo_pass", env="PG_PASSWORD")
    pg_db: str = Field("neo_dth", env="PG_DB")
    pg_dsn: str = Field("postgresql://neo_user:neo_pass@localhost:5432/neo_dth", env="PG_DSN")

    # InfluxDB 配置
    influx_url: str = Field("http://localhost:8086", env="INFLUX_URL")
    influx_token: str = Field("test-token", env="INFLUX_TOKEN")
    influx_org: str = Field("neo-org", env="INFLUX_ORG")
    influx_bucket: str = Field("neo-bucket", env="INFLUX_BUCKET")

    # MQTT 配置
    mqtt_host: str = Field("localhost", env="MQTT_HOST")
    mqtt_port: int = Field(1883, env="MQTT_PORT")
    mqtt_user: str = Field("neo_mqtt", env="MQTT_USER")
    mqtt_password: str = Field("neo_mqtt_pass", env="MQTT_PASSWORD")
    mqtt_topic: str = Field("neo/dth/#", env="MQTT_TOPIC")

    # TCP 配置
    tcp_host: str = Field("0.0.0.0", env="TCP_HOST")
    tcp_port: int = Field(9000, env="TCP_PORT")

    # 日志配置
    log_level: str = Field("INFO", env="LOG_LEVEL")

    # 兼容旧配置
    database_url: str = "sqlite:///./test.db"

settings = Settings()