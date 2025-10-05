import asyncio
from .handler import handle_client
import logging

TCP_PORT = 5858

logger = logging.getLogger("tcp_gateway.server")

async def start_tcp_server():
    logger.info("准备启动TCP服务")
    server = await asyncio.start_server(handle_client, host="0.0.0.0", port=TCP_PORT)
    logger.info(f"TCP监听端口: {TCP_PORT}")
    try:
        async with server:
            logger.info("TCP服务已启动，进入事件循环")
            await server.serve_forever()
    except Exception as e:
        logger.error(f"TCP服务启动异常: {e}")
    finally:
        logger.info("TCP服务关闭，清理资源")