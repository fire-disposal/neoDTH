from influxdb_client import InfluxDBClient
from app.core.settings import settings

class InfluxClient:
    def __init__(self):
        self.url = settings.influx_url
        self.token = settings.influx_token
        self.org = settings.influx_org

    def get_client(self):
        return InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )

# 协作模式说明：
# 1. 高频原始数据优先写入 InfluxDB，适合时序分析与大数据量。
# 2. 事件日志、元数据写入 PGSQL，便于结构化检索与业务追踪。
# 3. 事件总线驱动，Processor 负责两库写入与一致性保障。