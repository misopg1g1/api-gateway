import helpers
from config import AppConfigValues
from common import ResponseMessagesValues

import json
import hashlib

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
            hash_sum: str
            if not raw_json_body.get('hash') == helpers.get_hash(raw_json_body):
                return JSONResponse(status_code=403, content={"error": ResponseMessagesValues.NO_MATCHING_HATCH})
            new_bytes_body = json.dumps(raw_json_body).encode()
            receive["body"] = new_bytes_body

            async def new_receive() -> Message:
                return receive

            request = Request(request.scope, new_receive, send)
        response = await call_next(request)
        return response
