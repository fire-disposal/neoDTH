from fastapi import FastAPI
from app.api.routes.patient import router as patient_router
from app.api.routes.device import router as device_router
from app.api.routes.patient_device import router as patient_device_router
from app.api.routes.alert import router as alert_router

def register_routers(app: FastAPI):
    """
    挂载所有业务路由，并为每个路由分组添加 tags、summary、description，支持 FastAPI 动态文档。
    """
    app.include_router(
        patient_router,
        prefix="/patients",
        tags=["患者管理"]
    )
    app.include_router(
        device_router,
        prefix="/devices",
        tags=["设备管理"]
    )
    app.include_router(
        patient_device_router,
        prefix="/patient-devices",
        tags=["患者设备绑定"]
    )
    app.include_router(
        alert_router,
        prefix="/alerts",
        tags=["告警管理"]
    )