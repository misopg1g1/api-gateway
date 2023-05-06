from unittest.mock import Mock
from fastapi.testclient import TestClient
import api
import requests
import pytest
import helpers


class TestClassCreateInventory:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 204
        mockup_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mockup_resp
        
        monkeypatch.setattr(requests, 'request', mock_method)
        return mockup_resp
    
    def test_success(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        inventory_to_add = {"product_id": '123456', "stock": 10}
        inventory_to_add["hash"] = helpers.get_hash(inventory_to_add)
        resp = client.post("/inventories", json=inventory_to_add, headers=headers)
        assert resp.status_code == 204

    def test_unauthorized(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
        }
        inventory_to_add = {"product_id": '123456', "stock": 9}
        inventory_to_add["hash"] = helpers.get_hash(inventory_to_add)
        resp = client.post("/inventories", json=inventory_to_add, headers=headers)
        assert resp.status_code == 403

    def test_error_hash(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"           
        }
        inventory_to_add = {"product_id": '123456', "stock": 9}
        inventory_to_add2 = {"product_id": '12345XX', "stock": 8}
        inventory_to_add["hash"] = helpers.get_hash(inventory_to_add2)
        resp = client.post("/inventories", json=inventory_to_add, headers=headers)
        assert resp.status_code == 403
        
class TestClassGetInventory:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 204
        mockup_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mockup_resp
        
        monkeypatch.setattr(requests, 'request', mock_method)
        return mockup_resp
    
    def test_success(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/products/123456/inventory", headers=headers)
        assert resp.status_code == 204

    def test_not_found(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/produc/123456/inventory", headers=headers)
        assert resp.status_code == 404

class TestClassGetInventories:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 204
        mockup_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mockup_resp
        
        monkeypatch.setattr(requests, 'request', mock_method)
        return mockup_resp
    
    def test_success(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/inventories", headers=headers)
        assert resp.status_code == 204

    def test_not_found(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/inventoriesXX", headers=headers)
        assert resp.status_code == 404

class TestClassUpdateInventory:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 204
        mockup_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mockup_resp
        
        monkeypatch.setattr(requests, 'request', mock_method)
        return mockup_resp
    
    def test_success(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        inventory_to_add = {"stock": 10}
        inventory_to_add["hash"] = helpers.get_hash(inventory_to_add)
        resp = client.put("/products/123456/inventory", json=inventory_to_add, headers=headers)
        assert resp.status_code == 204


    def test_unauthorized(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
        }
        inventory_to_add = {"stock": 5}
        inventory_to_add["hash"] = helpers.get_hash(inventory_to_add)
        resp = client.put("/products/123456/inventory", json=inventory_to_add, headers=headers)
        assert resp.status_code == 403

    def test_error_hash(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"           
        }
        inventory_to_add = {"stock": 4}
        inventory_to_add2 = {"stock": 3}
        inventory_to_add["hash"] = helpers.get_hash(inventory_to_add2)
        resp = client.put("/products/123456/inventory", json=inventory_to_add, headers=headers)
        assert resp.status_code == 403
        