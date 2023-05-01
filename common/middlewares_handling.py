import helpers
import adapters
import schemas

from common import ResponseMessagesValues

import json
import typing

from fastapi.responses import JSONResponse
from starlette.requests import Message
from fastapi import FastAPI, Request


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


def verify_role_middleware(roles: typing.List[str]):
    def lower_decorator(func):
        def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            response = kwargs.get("response")
            headers = dict(request.headers.items())
            auth_adapter = adapters.AuthAdapter()
            v_status_code, v_json_resp = auth_adapter.verify_roles(
                schemas.RolesSchema(**{"roles": roles}),
                headers)
            if v_status_code != 204:
                response.status_code = v_status_code
                return v_json_resp
            if (resp := func(*args, **kwargs)) is not None:
                return resp

        return wrapper

    return lower_decorator


__all__ = ['verify_role_middleware', 'encrypter_middleware']
