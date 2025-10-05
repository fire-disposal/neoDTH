from app.services.aggregators.health_combiner import HealthCombiner
from app.services.heart_rate_processor import HeartRateProcessor
from app.services.temperature_processor import TemperatureProcessor
from app.services.sleep_processor import SleepProcessor
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

    heart_rate_processor = HeartRateProcessor(influx_repo, heart_rate_repo)
    temperature_processor = TemperatureProcessor(influx_repo, temperature_repo)
    sleep_processor = SleepProcessor(influx_repo, temperature_repo)

    # 如需注册事件监听，可在此调用
    # 例如 event_bus.subscribe(..., heart_rate_processor.handle_data_received)
    # 目前事件订阅已在各聚合器/handler内部完成，如需统一注册可补充

    # 其他服务初始化需求可在此扩展
