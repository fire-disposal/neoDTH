from app.services.aggregators.health_combiner import HealthCombiner
from app.services.health_metrics.heart_rate_processor import HeartRateProcessor
from app.services.health_metrics.temperature_processor import TemperatureProcessor
from app.services.health_metrics.sleep_processor import SleepProcessor
from app.adapters.influx_repository.metrics_repo import MetricsRepo
from app.adapters.pg_repository.heart_rate_repo import HeartRateRepo
from app.adapters.pg_repository.temperature_repo import TemperatureRepo
from app.adapters.influx_repository.influx_client import InfluxClient
from app.adapters.pg_repository.pgsql_client import PgSQLClient

# 统一初始化所有服务监听与事件订阅
async def init_all_services():


    # 初始化健康聚合器并订阅事件
    health_combiner = HealthCombiner()
    await health_combiner.start()

    # 初始化数据处理器与存储库
    influx_client = InfluxClient()
    influx_repo = MetricsRepo(influx_client)


    pg_client = PgSQLClient()
    heart_rate_repo = HeartRateRepo(pg_client)
    temperature_repo = TemperatureRepo(pg_client)


    # 其他服务初始化需求可在此扩展
