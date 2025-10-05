import pytest
from fastapi.testclient import TestClient
from app._main_ import app
from app.domain.device.models import Device

client = TestClient(app)

def test_create_device_success(monkeypatch):
    # 模拟唯一性校验通过
    device_data = {
        "name": "dev1",
        "serial_number": "SN001"
    }
    response = client.post("/devices/", json=device_data)
    assert response.status_code == 201
    assert isinstance(response.json(), int)

def test_create_device_missing_required(monkeypatch):
    # 缺少name
    device_data = {
        "serial_number": "SN002"
    }
    response = client.post("/devices/", json=device_data)
    assert response.status_code == 422 or response.status_code == 400

def test_create_device_duplicate_serial(monkeypatch):
    # 首次创建
    device_data = {
        "name": "dev2",
        "serial_number": "SN003"
    }
    response1 = client.post("/devices/", json=device_data)
    # 再次创建同serial_number
    response2 = client.post("/devices/", json=device_data)
    assert response2.status_code == 400 or response2.status_code == 422

def test_get_device_not_found():
    response = client.get("/devices/999999")
    assert response.status_code == 404

def test_update_device_not_found():
    device_data = {
        "name": "dev3",
        "serial_number": "SN004"
    }
    response = client.put("/devices/999999", json=device_data)
    assert response.status_code == 404

def test_delete_device_not_found():
    response = client.delete("/devices/999999")
    assert response.status_code == 404

# 权限控制预留：如需鉴权，可在接口加上依赖项并在此模拟token