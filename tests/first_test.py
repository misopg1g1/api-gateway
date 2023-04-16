import schemas
import api

import hashlib
import json

from fastapi.testclient import TestClient
from cryptography.fernet import Fernet


class TestClassFirstTest:
    def test_succes(self):
        client = TestClient(api.create_app())

        user = {
            "user": "user1",
            "password": "password1"
        }
        ordered_user = dict(sorted(user.items(),key=lambda kv: kv[0]))
        raw_hash = hashlib.md5(json.dumps(ordered_user).encode()).hexdigest()
        hash_user  = {
            "hash":raw_hash,
            "user": "user1",
            "password": "password1"
        }
        resp= client.post("/login", json=hash_user)
        assert resp.status_code == 404

    def test_forbidden   (self):
        client = TestClient(api.create_app())

        user = {
            "user": "user1",
            "password": "password1"
        }
        ordered_user = dict(sorted(user.items(),key=lambda kv: kv[0]))
        raw_hash = hashlib.md5(json.dumps(ordered_user).encode()).hexdigest()
        hash_user  = {
            "hash":raw_hash,
            "user": "user2",
            "password": "password2"
        }
        resp= client.post("/login", json=hash_user)
        assert resp.status_code == 403