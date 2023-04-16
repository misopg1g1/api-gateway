import schemas
import api

import hashlib
import json
import pytest
import requests

from fastapi.testclient import TestClient
from cryptography.fernet import Fernet
from unittest.mock import Mock


class TestClassFirstTest:
    @pytest.fixture
    def mock_response(self, monkeypatch):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'key': 'value'}

        def mock_method(*args, **kwargs):
            return mock_resp

        monkeypatch.setattr(requests, 'post', mock_method)
        return mock_resp

    def test_success(self, mock_response):
        client = TestClient(api.create_app())
        user = {
            "user": "user1",
            "password": "password1"
        }
        ordered_user = dict(sorted(user.items(), key=lambda kv: kv[0]))
        raw_hash = hashlib.md5(json.dumps(ordered_user).encode()).hexdigest()
        hash_user = {
            "hash": raw_hash,
            "user": "user1",
            "password": "password1"
        }
        resp = client.post("/session/login", json=hash_user)
        assert resp.status_code == 200
        assert resp.json() == {'key': 'value'}

    def test_forbidden(self):
        client = TestClient(api.create_app())

        user = {
            "user": "user1",
            "password": "password1"
        }
        ordered_user = dict(sorted(user.items(), key=lambda kv: kv[0]))
        raw_hash = hashlib.md5(json.dumps(ordered_user).encode()).hexdigest()
        hash_user = {
            "hash": raw_hash,
            "user": "user2",
            "password": "password2"
        }
        resp = client.post("/session/login", json=hash_user)
        assert resp.status_code == 403
