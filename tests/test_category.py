from unittest.mock import Mock
from fastapi.testclient import TestClient
import api
import requests
import pytest
import helpers
import schemas
import common


class TestClassCreateCategory:
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
        category_to_add = schemas.CREATE_PRODUCT_EXAMPLE
        category_to_add["hash"] = helpers.get_hash(category_to_add)
        resp = client.post("/categories", json=category_to_add, headers=headers)
        assert resp.status_code == 204


    def test_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        category_to_add = schemas.CREATE_CATEGORY_EXAMPLE
        category_to_add["hash"] = helpers.get_hash(category_to_add)
        resp = client.post("/categories", json=category_to_add, headers=headers)
        assert resp.status_code == 401

    def test_error_hash(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        category_to_add = schemas.CREATE_CATEGORY_EXAMPLE
        category_to_add["hash"] = helpers.get_hash(category_to_add)
        category_to_add["something"] = "hello"
        resp = client.post("/categories", json=category_to_add, headers=headers)
        assert resp.status_code == 403


class TestClassGetCategories:
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
        resp = client.get("/categories", headers=headers)
        assert resp.status_code == 204

    def test_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/categories", headers=headers)
        assert resp.status_code == 401


class TestClassPatchCategories:
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
        category_to_add = schemas.PATCH_CATEGORY_EXAMPLE
        category_to_add["hash"] = helpers.get_hash(category_to_add)
        resp = client.patch("/categories/1", json=category_to_add, headers=headers)

        assert resp.status_code == 204
