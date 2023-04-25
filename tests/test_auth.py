import helpers
import api

import hashlib
import json
import pytest
import requests

from fastapi.testclient import TestClient
from unittest.mock import Mock


class TestClassLogin:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mock_resp

        monkeypatch.setattr(requests, 'request', mock_method)
        return mock_resp

    def test_success(self, mock_response):
        client = TestClient(api.create_app())
        user = {
            "user": "user1",
            "password": "password1"
        }
        user["hash"] = helpers.get_hash(user)
        resp = client.post("/session/login", json=user)
        assert resp.status_code == 200
        assert resp.json() == {'key': 'value'}

    def test_forbidden(self):
        client = TestClient(api.create_app())

        user = {
            "user": "user1",
            "password": "password1"
        }
        ordered_user = dict(sorted(user.items(), key=lambda kv: kv[0]))
        raw_hash = helpers.get_hash(ordered_user)
        hash_user = {
            "hash": raw_hash,
            "user": "user2",
            "password": "password2"
        }
        resp = client.post("/session/login", json=hash_user)
        assert resp.status_code == 403


class TestClassCreateUser:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mock_resp

        monkeypatch.setattr(requests, 'request', mock_method)
        return mock_resp

    def test_success(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        user_to_add = {"user": 'user2', "password": 'password2', "role": 'SELLER', "verify_password": "password2"}
        user_to_add["hash"] = helpers.get_hash(user_to_add)
        resp = client.post("/session/create_user", json=user_to_add, headers=headers)
        assert resp.status_code == 200
        assert resp.json() == {'key': 'value'}


class TestClassRefreshToken:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mock_resp

        monkeypatch.setattr(requests, 'request', mock_method)
        return mock_resp

    def test_success(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/session/refresh_token", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == {'key': 'value'}

    def test_unauthorized(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        resp = client.get("/session/refresh_token", headers=headers)
        assert resp.status_code == 403


class TestClassVerifyRoles:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mock_resp

        monkeypatch.setattr(requests, 'request', mock_method)
        return mock_resp

    def test_success(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        payload = {'roles': ['ADMIN', 'SELLER']}
        payload["hash"] = helpers.get_hash(payload)
        resp = client.post("/session/verify_roles", json=payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json() == {'key': 'value'}

    def test_unprocessable(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        payload = {}
        payload["hash"] = helpers.get_hash(payload)
        resp = client.post("/session/verify_roles", json=payload, headers=headers)
        assert resp.status_code == 422


class TestClassVerifyToken:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mock_resp

        monkeypatch.setattr(requests, 'request', mock_method)
        return mock_resp

    def test_success(self, mock_response):
        client = TestClient(api.create_app())
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer 1"
        }
        resp = client.get("/session/verify_token", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == {'key': 'value'}
