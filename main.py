from fastapi import FastAPI
from fastapi import Request
from contextlib import asynccontextmanager
from app.core.event_bus import event_bus
from app.core.startup_checker import verify_all_dependencies
from app.core.settings import settings
from app.core.logger import logger
import contextlib


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI 启动，初始化事件总线")
    try:
        # await verify_all_dependencies()
        _ = settings  # 强制触发 settings 加载
        _ = event_bus  # 强制触发 event_bus 加载
        logger.info("注册 API 路由")
        from app.api.bootstrap_router import register_routers

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


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
@app.get("/")
async def health_check():
    return "😄"

from app.core.cors_middleware import setup_cors

# 注册 CORS 中间件，需在路由注册前调用
setup_cors(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
