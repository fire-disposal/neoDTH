import asyncpg
from app.core.settings import settings

class PgSQLClient:
    def __init__(self):
        self.dsn = settings.pg_dsn

    async def get_pool(self):
        return await asyncpg.create_pool(dsn=self.dsn)

# 协作模式说明：
# 1. 高频原始数据仅写入 InfluxDB，PGSQL 只保留事件日志与元数据。
# 2. 事件总线驱动，Processor 消费事件后分别写入两库，保证解耦与一致性。