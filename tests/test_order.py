import adapters
import common

from unittest.mock import Mock
from fastapi.testclient import TestClient
import api
import requests
import pytest


class TestClassGetOrders:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 200
        mockup_resp.json.return_value = [{"visit_id": 1, "seller": "mock_seller", "customer": "mock_customer"}]

        def mock_method(*args, **kwargs):
            return mockup_resp

        monkeypatch.setattr(requests, 'request', mock_method)

        return mockup_resp

    @pytest.fixture
    def mock_auth_adapter(self, monkeypatch):
        def mock_instance(*args, **kwargs):
            class MockClass:
                def verify_roles(self, *args, **kwargs):
                    return 200, "Mocked method"

                def verify_token(self, *args, **kwargs):
                    return 200, {"role": "ADMIN"}

            return MockClass()

        monkeypatch.setattr('adapters.AuthAdapter', mock_instance)
        return mock_instance

    @pytest.fixture
    def mock_seller_adapter(self, monkeypatch):
        def mock_instance(*args, **kwargs):
            class MockClass:
                def get_visit(self, *args, **kwargs):
                    return 200, {"visit_id": 1, "seller": "mock_seller", "customer": "mock_customer"}

            return MockClass()

        monkeypatch.setattr('adapters.SellersAdapter', mock_instance)
        return mock_instance

    def test_success(self, mock_auth_adapter, mock_response, mock_seller_adapter):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/orders", headers=headers)
        assert resp.status_code == 200


class TestClassGetOrder:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 200
        mockup_resp.json.return_value = {"visit_id": 1, "seller": "mock_seller", "customer": "mock_customer"}

        def mock_method(*args, **kwargs):
            return mockup_resp

        monkeypatch.setattr(requests, 'request', mock_method)

        return mockup_resp

    @pytest.fixture
    def mock_auth_adapter(self, monkeypatch):
        def mock_instance(*args, **kwargs):
            class MockClass:
                def verify_roles(self, *args, **kwargs):
                    return 200, "Mocked method"

                def verify_token(self, *args, **kwargs):
                    return 200, {"role": "ADMIN"}

            return MockClass()

        monkeypatch.setattr('adapters.AuthAdapter', mock_instance)
        return mock_instance

    @pytest.fixture
    def mock_seller_adapter(self, monkeypatch):
        def mock_instance(*args, **kwargs):
            class MockClass:
                def get_visit(self, *args, **kwargs):
                    return 200, {"visit_id": 1, "seller": "mock_seller", "customer": "mock_customer"}

            return MockClass()

        monkeypatch.setattr('adapters.SellersAdapter', mock_instance)
        return mock_instance

    def test_success(self, mock_auth_adapter, mock_response, mock_seller_adapter):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/orders/1", headers=headers)
        assert resp.status_code == 200
