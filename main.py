from fastapi import FastAPI
from app.core.settings import settings
from app.api.router_registry import setup_api
from app.core.lifespan import lifespan

app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
setup_api(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
