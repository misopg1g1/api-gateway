from unittest.mock import Mock
from fastapi.testclient import TestClient
import api
import requests
import pytest
import helpers
import schemas


# class TestClassCreateSeller:
#     @pytest.fixture
#     def mock_response(self, monkeypatch):
#         mockup_resp = Mock()
#         mockup_resp.status_code = 204
#         mockup_resp.json.return_value = {'key': 'value'}

#         def mock_method(*args, **kwargs):
#             return mockup_resp

#         monkeypatch.setattr(requests, 'request', mock_method)
#         return mock_method
#     def test_success(self, mock_response):
#         client = TestClient(api.create_app())
#         headers = {
#             "accept": "aplication/json",
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer 1"
#         }
#         seller_to_add = schemas.CREATE_SELLER_EXAMPLE
#         seller_to_add["hash"] = helpers.get_hash(seller_to_add)
#         resp = client.post("sellers", json=seller_to_add, headers=headers)
#         assert resp.status_code == 201

#     def test_error_unauthorized(self, mock_response):
#         client = TestClient(api.create_app())
#         headers = {
#             "accept": "aplication/json",
#             "Content": "application/json",
#         }
#         seller_to_add = schemas.CREATE_SELLER_EXAMPLE
#         seller_to_add["hash"] = helpers.get_hash(seller_to_add)
#         resp = client.post("/sellers", json=seller_to_add, headers=headers)
#         assert resp.status_code == 403

class TestClassGetSellers:
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
        resp = client.get("/sellers", headers=headers)
        assert resp.status_code == 204

    def test_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/sellers", headers=headers)
        assert resp.status_code == 401


class TestClassGetSeller:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 204
        mockup_resp.json.return_value = {'key': 'value', 'role': 'ADMIN'}

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
        resp = client.get("/sellers/1", headers=headers)
        assert resp.status_code == 204

    def test_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/sellers/1", headers=headers)
        assert resp.status_code == 401


class TestClassGetVisitsFromSeller:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 204
        mockup_resp.json.return_value = {'key': 'value', 'role': 'ADMIN'}

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
        resp = client.get("/sellers/1/visits", headers=headers)
        assert resp.status_code == 204

    def test_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/sellers/1/visits", headers=headers)
        assert resp.status_code == 401


class TestClassGetVisitFromSeller:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 201
        mockup_resp.json.return_value = {'key': 'value', 'role': 'ADMIN'}

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
        resp = client.get("/sellers/1/visits/1", headers=headers)
        assert resp.status_code == 201

    def test_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/sellers/1/visits/1", headers=headers)
        assert resp.status_code == 401


class TestClassGetVisits:
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
        resp = client.get("/visits", headers=headers)
        assert resp.status_code == 204

    def test_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/visits", headers=headers)
        assert resp.status_code == 401


class TestClassGetVisit:
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
        resp = client.get("/visits/1", headers=headers)
        assert resp.status_code == 204

    def test_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/visits/1", headers=headers)
        assert resp.status_code == 401


class TestClassCreateVisit:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 201
        mockup_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mockup_resp

        monkeypatch.setattr(requests, 'request', mock_method)
        return mockup_resp

    @pytest.fixture
    def mock_response_unauthorized(self, monkeypatch):
        mockup_resp = Mock()
        mockup_resp.status_code = 403
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
        visit_to_add = schemas.CREATE_VISIT_EXAMPLE
        visit_to_add["hash"] = helpers.get_hash(visit_to_add)
        resp = client.post("/visits", json=visit_to_add, headers=headers)
        assert resp.status_code == 201

    def test_error_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content": "application/json",
            "Authorization": f"Bearer 1"
        }
        visit_to_add = schemas.CREATE_VISIT_EXAMPLE
        visit_to_add["hash"] = helpers.get_hash(visit_to_add)
        resp = client.post("/visits", json=visit_to_add, headers=headers)
        assert resp.status_code == 403


class TestClassUpdateVisit:
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
        visit_to_update = schemas.UPDATE_VISIT_EXAMPLE
        visit_to_update["hash"] = helpers.get_hash(visit_to_update)
        resp = client.put("/visits/1", json=visit_to_update, headers=headers)
        assert resp.status_code == 204

    def test_error_unauthorized(self, mock_response_unauthorized):
        client = TestClient(api.create_app())
        headers = {
            "accept": "aplication/json",
            "Content": "application/json",
            "Authorization": f"Bearer 1"
        }
        visit_to_update = schemas.UPDATE_VISIT_EXAMPLE
        visit_to_update["hash"] = helpers.get_hash(visit_to_update)
        resp = client.put("/visits/1", json=visit_to_update, headers=headers)
        assert resp.status_code == 401
