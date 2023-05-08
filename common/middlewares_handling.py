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
        # Receive the entire request body using request.stream()
        body = b""
        async for chunk in request.stream():
            body += chunk

        if body:
            # Check the hash and add it to the request headers
            raw_json_body = json.loads(body)
            hash_sum = helpers.get_hash(raw_json_body)
            if not raw_json_body.get('hash') == hash_sum:
                return JSONResponse(status_code=403, content={"error": ResponseMessagesValues.NO_MATCHING_HATCH})

        async def new_receive() -> Message:
            return {"type": "http.request", "body": body}

        request = Request(request.scope, new_receive, request._send)

        # Call the next middleware or the endpoint with the updated request
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


def verify_identity(target_user_id: typing.Optional[str] = None):
    def lower_decorator(func):
        def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            response = kwargs.get("response")
            headers = dict(request.headers.items())
            auth_adapter = adapters.AuthAdapter()
            v_status_code, v_json_resp = auth_adapter.verify_token(headers)
            if v_status_code != 200:
                response.status_code = v_status_code
                return v_json_resp
            if target_user_id:
                if not (requester_id := v_json_resp.get("id")) or requester_id != target_user_id:
                    return JSONResponse(status_code=401, content={"error": ResponseMessagesValues.NOT_ALLOWED})
            if (resp := func(*args, **kwargs)) is not None:
                return resp

        return wrapper

    return lower_decorator


__all__ = ['verify_role_middleware', 'encrypter_middleware', 'verify_identity']
