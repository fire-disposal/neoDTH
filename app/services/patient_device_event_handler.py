from app.domain.patient_device.events import PatientDeviceBound, PatientDeviceUnbound
from app.core.logger import logger

async def handle_patient_device_bound(event: PatientDeviceBound):
    logger.info(f"患者设备绑定事件: 患者ID={event.patient_id}, 设备ID={event.device_id}, 绑定时间={event.bind_time}")

async def handle_patient_device_unbound(event: PatientDeviceUnbound):
    logger.info(f"患者设备解绑事件: 患者ID={event.patient_id}, 设备ID={event.device_id}, 解绑时间={event.unbind_time}")