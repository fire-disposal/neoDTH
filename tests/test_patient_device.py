import pytest
from fastapi.testclient import TestClient
from app._main_ import app
from app.domain.patient_device.models import PatientDevice

client = TestClient(app)

@pytest.fixture
def patient_and_device(monkeypatch):
    # 假设有患者ID 1 和设备ID 1，实际应根据测试库准备
    return {"patient_id": 1, "device_id": 1}

def test_bind_device_success(patient_and_device):
    pd = {
        "patient_id": patient_and_device["patient_id"],
        "device_id": patient_and_device["device_id"],
        "note": "test bind"
    }
    response = client.post("/patient-devices/bind", json=pd)
    assert response.status_code == 201
    assert isinstance(response.json(), int)

def test_bind_device_duplicate(patient_and_device):
    pd = {
        "patient_id": patient_and_device["patient_id"],
        "device_id": patient_and_device["device_id"],
        "note": "test bind"
    }
    # 第一次绑定
    response1 = client.post("/patient-devices/bind", json=pd)
    # 第二次绑定应报唯一性冲突
    response2 = client.post("/patient-devices/bind", json=pd)
    assert response2.status_code == 400
    assert "已绑定" in response2.json()["detail"]

def test_unbind_device_success(patient_and_device):
    pd = {
        "patient_id": patient_and_device["patient_id"],
        "device_id": patient_and_device["device_id"],
        "note": "test bind"
    }
    # 先绑定
    bind_resp = client.post("/patient-devices/bind", json=pd)
    pd_id = bind_resp.json()
    # 解绑
    unbind_resp = client.post(f"/patient-devices/unbind/{pd_id}")
    assert unbind_resp.status_code == 200
    assert unbind_resp.json() is True

def test_unbind_device_idempotent(patient_and_device):
    pd = {
        "patient_id": patient_and_device["patient_id"],
        "device_id": patient_and_device["device_id"],
        "note": "test bind"
    }
    # 绑定
    bind_resp = client.post("/patient-devices/bind", json=pd)
    pd_id = bind_resp.json()
    # 解绑两次
    client.post(f"/patient-devices/unbind/{pd_id}")
    resp2 = client.post(f"/patient-devices/unbind/{pd_id}")
    assert resp2.status_code == 200
    assert resp2.json() is True

def test_unbind_device_not_found():
    resp = client.post("/patient-devices/unbind/999999")
    assert resp.status_code == 404
