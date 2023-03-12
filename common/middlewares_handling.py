from config import AppConfigValues

import json
import hashlib

from common import ResponseMessagesValues
from fastapi.responses import JSONResponse
from starlette.requests import Message
from fastapi import FastAPI, Request
from cryptography.fernet import Fernet


def encrypter_middleware(app: FastAPI):
    @app.middleware("http")
    async def encrypt_body(request: Request, call_next):
        receive = await request._receive()
        send = request._send
        if bytes_body := receive.get("body"):
            raw_json_body = json.loads(bytes_body)
            clean_json_body = dict(filter(lambda kv: kv[0] not in ["hash"], json.loads(bytes_body).items()))
            hash: str
            if (hash := raw_json_body.get('hash')) == hashlib.md5(json.dumps(clean_json_body).encode()).hexdigest():
                fernet = Fernet(AppConfigValues.ENCRYPTION_KEY_SECRET.encode())
                clean_json_body["hash"] = fernet.encrypt(hash.encode()).decode()
            else:
                return JSONResponse(status_code=403, content={"error": ResponseMessagesValues.NO_MATCHING_HATCH})
            new_bytes_body = json.dumps(clean_json_body).encode()
            receive["body"] = new_bytes_body

            async def new_receive() -> Message:
                return receive

            request = Request(request.scope, new_receive, send)
        response = await call_next(request)
        return response
