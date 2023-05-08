import copy

import config
import helpers
import adapters
import schemas

from common import ResponseMessagesValues

import json
import typing
import re
import requests

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


def verify_identity_for_seller_resources(target_user_id: typing.Optional[str] = None):
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
                if v_json_resp.get("role") not in ["ADMIN", "MARKETING"] and \
                        (not (requester_id := v_json_resp.get("id")) or requester_id != target_user_id):
                    return JSONResponse(status_code=401, content={"error": ResponseMessagesValues.NOT_ALLOWED})
            if v_json_resp.get("role") == "SELLER" and not target_user_id and \
                    re.fullmatch(r'/visits/[\dA-Za-z\-]+', request.url.path) and request.method in ["PUT", "DELETE"]:
                get_response = requests.request("GET", '/'.join([config.AppConfigValues.SELLERS_URL,
                                                                 *str(request.url).split("/")[3::]]),
                                                params={"relations": True})
                if get_response.status_code != 200:
                    try:
                        return JSONResponse(status_code=get_response.status_code,
                                            content=get_response.json())
                    except:
                        JSONResponse(status_code=500,
                                     content={"error": ResponseMessagesValues.GENERAL_REQUESTS_FAILURE_MESSAGE})
                else:
                    try:
                        if get_response.json().get("seller", {}).get("id") != v_json_resp.get("id"):
                            return JSONResponse(status_code=401, content={"error": ResponseMessagesValues.NOT_ALLOWED})
                    except:
                        JSONResponse(status_code=500,
                                     content={"error": ResponseMessagesValues.GENERAL_REQUESTS_FAILURE_MESSAGE})

            if v_json_resp.get("role") != "SELLER" and not target_user_id and \
                    re.fullmatch(r'/visits', request.url.path) and request.method in ["POST"]:
                return JSONResponse(status_code=401, content={"error": ResponseMessagesValues.ONLY_SELLERS_MSG})

            if v_json_resp.get("role") == "SELLER" and not target_user_id and \
                    re.fullmatch(r'/visits', request.url.path) and request.method in ["POST"]:
                kwargs["seller_id"] = v_json_resp.get("id")

            if (resp := func(*args, **kwargs)) is not None:
                if v_json_resp.get("role") == "SELLER" and not target_user_id and \
                        re.fullmatch(r'(/visits|/visits/[\dA-Za-z\-]+)', request.url.path) and request.method == "GET":
                    if isinstance(resp, typing.List):
                        return list(
                            filter(lambda obj: not obj.get("seller") or obj.get("seller",
                                                                                {}).get("id") == v_json_resp.get("id"),
                                   resp))
                    if isinstance(resp, dict) and not (
                            not resp.get("seller") or resp.get("seller", {}).get("id") == v_json_resp.get("id")):
                        return JSONResponse(status_code=401, content={"error": ResponseMessagesValues.NOT_ALLOWED})
                    return resp

                return resp

        return wrapper

    return lower_decorator


__all__ = ['verify_role_middleware', 'encrypter_middleware', 'verify_identity_for_seller_resources']
