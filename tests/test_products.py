from unittest.mock import Mock
from fastapi.testclient import TestClient
import api
import requests
import pytest
import helpers
import schemas


class TestClassCreateProduct:
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
        product_to_add = schemas.CREATE_PRODUCT_EXAMPLE
        product_to_add["hash"] = helpers.get_hash(product_to_add)
        resp = client.post("/products", json=product_to_add, headers=headers)
        assert resp.status_code == 204

    def test_unauthorized(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
        }
        product_to_add = schemas.CREATE_PRODUCT_EXAMPLE
        product_to_add["hash"] = helpers.get_hash(product_to_add)
        resp = client.post("/products", json=product_to_add, headers=headers)
        assert resp.status_code == 403

    def test_error_hash(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        product_to_add = schemas.CREATE_PRODUCT_EXAMPLE
        product_to_add["hash"] = helpers.get_hash(product_to_add)
        product_to_add["something"] = "hello"
        resp = client.post("/products", json=product_to_add, headers=headers)
        assert resp.status_code == 403


class TestClassGetProducts:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 204
        mockup_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mockup_resp

        monkeypatch.setattr(requests, 'request', mock_method)
        return mockup_resp

    @pytest.fixture
    def mock_response_unauthorized(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 401
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
        resp = client.get("/products", headers=headers)
        assert resp.status_code == 204

    def test_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/products", headers=headers)
        assert resp.status_code == 401


class TestClassGetProduct:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 204
        mockup_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mockup_resp

        monkeypatch.setattr(requests, 'request', mock_method)
        return mockup_resp

    @pytest.fixture
    def mock_response_unauthorized(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 401
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
        resp = client.get("/products/1", headers=headers)
        assert resp.status_code == 204


    def test_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/products/1", headers=headers)
        assert resp.status_code == 401
