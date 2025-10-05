import uvicorn
from app.core.settings import settings

async def main():
    """启动 FastAPI 服务"""
    uvicorn.run(
        "main:app",
        host=settings.host if hasattr(settings, "host") else "0.0.0.0",
        port=settings.port if hasattr(settings, "port") else 8000,
        reload=getattr(settings, "reload", False)
    )