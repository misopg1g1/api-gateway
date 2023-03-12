import schemas
from config import AppConfigValues

import os
import requests

from fastapi import APIRouter, Header, Request
from fastapi.responses import JSONResponse

mock_router = APIRouter(prefix="/mock", tags=["mock resource"])


@mock_router.post("/")
def mock_post(body: schemas.MockBody, req: Request):
    response = requests.request(req.method, f"{AppConfigValues.SOME_MICROSERVICE_URL}{req.scope.get('path')}",
                                data=body.json())
    return JSONResponse(status_code=response.status_code, content=response.json())


@mock_router.put("/")
def mock_put(body: schemas.MockBody, req: Request):
    response = requests.request(req.method, f"{AppConfigValues.SOME_MICROSERVICE_URL}{req.scope.get('path')}",
                                data=body.json())
    return JSONResponse(status_code=response.status_code, content=response.json())


@mock_router.patch("/")
def mock_patch(body: schemas.MockBody, req: Request):
    response = requests.request(req.method, f"{AppConfigValues.SOME_MICROSERVICE_URL}{req.scope.get('path')}",
                                data=body.json())
    return JSONResponse(status_code=response.status_code, content=response.json())
