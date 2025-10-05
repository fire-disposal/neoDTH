# app/core/startup_checker.py
import asyncio
import logging
from asyncpg import connect as pg_connect
from influxdb_client import InfluxDBClient
import paho.mqtt.client as mqtt
from app.core.settings import settings

logger = logging.getLogger(__name__)

async def check_pgsql():
    conn = await pg_connect(
        host=settings.pg_host,
        port=settings.pg_port,
        user=settings.pg_user,
        password=settings.pg_password,
        database=settings.pg_db,
    )
    await conn.close()

async def check_influx():
    client = InfluxDBClient(
        url=settings.influx_url,
        token=settings.influx_token,
        org=settings.influx_org,
    )
    await asyncio.to_thread(client.ping)  # 用线程包装同步调用
    client.close()

async def check_mqtt():
    loop = asyncio.get_event_loop()
    def _connect():
        client = mqtt.Client()
        client.connect(settings.mqtt_host, settings.mqtt_port, 3)
        client.disconnect()
    await loop.run_in_executor(None, _connect)

async def wait_for_service(check_func, name, retries=3, base_delay=1):
    for attempt in range(1, retries + 1):
        try:
            await check_func()
            logger.info(f"[{name}] ✅ 连接成功")
            return True
        except Exception as e:
            logger.warning(f"[{name}] ❌ 第 {attempt} 次失败: {e}")
            await asyncio.sleep(base_delay * (2 ** (attempt - 1)))
    logger.error(f"[{name}] ❌ 重试 {retries} 次后仍失败")
    return False

async def verify_all_dependencies():
    logger.info("开始检测外部依赖服务状态...")
    results = await asyncio.gather(
        wait_for_service(check_pgsql, "PostgreSQL"),
        wait_for_service(check_influx, "InfluxDB"),
        wait_for_service(check_mqtt, "MQTT"),
    )
    if not all(results):
        raise RuntimeError("依赖服务未全部就绪，启动中止。")
    logger.info("✅ 所有依赖服务检测通过")
