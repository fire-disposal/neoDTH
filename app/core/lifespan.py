from fastapi import FastAPI
from contextlib import asynccontextmanager
import contextlib

from app.core.event_bus import event_bus
import asyncio
import logging
from asyncpg import connect as pg_connect
from influxdb_client import InfluxDBClient
import paho.mqtt.client as mqtt

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
from app.core.settings import settings
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI 启动，初始化事件总线")
    try:

        await verify_all_dependencies()
        
        _ = settings  # 强制触发 settings 加载
        _ = event_bus  # 强制触发 event_bus 加载
        logger.info("注册 API 路由")
        from app.api.router_registry import register_routers

        register_routers(app)
        logger.info("注册服务层统一初始化")
        from app.services.bootstrap_services import init_all_services

        await init_all_services()
        # 启动 TCP Gateway 服务（事件驱动架构）
        import asyncio
        from app.adapters.tcp_gateway import server as tcp_server

        tcp_task = asyncio.create_task(tcp_server.start_tcp_server())
        logger.info(f"msgpack监听服务启动: {getattr(tcp_server, 'TCP_PORT', '5858')}")
        logger.info("初始化完成，准备启动服务")
        try:
            yield
        finally:
            tcp_task.cancel()
            with contextlib.suppress(Exception):
                await tcp_task
    except Exception as e:
        logger.error(f"初始化阶段异常: {e}")
        raise
    finally:
        logger.info("FastAPI 关闭，清理资源")