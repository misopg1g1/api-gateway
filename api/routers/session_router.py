import enums
import schemas
import common
import adapters

import typing
from fastapi import APIRouter, Depends, Response, Request

session_router = APIRouter(prefix="/session", tags=["Auth resource"])


@session_router.post("/create_user")
def create_user(new_user_schema: schemas.CreateUserSchema, request: Request, response: Response,
                token: str = Depends(common.token_schema)):
    user_adapter = adapters.AuthAdapter()
    headers = dict(request.headers.items())
    response.status_code, json_response = user_adapter.create_user(new_user_schema, headers)
    if new_user_schema.role == enums.RoleEnum.SELLER.value:
        seller_adapter = adapters.SellersAdapter()
        if json_response and (user_id := json_response.get("id", None)):
            new_seller_schema = schemas.CreateSellerSchema(id=user_id)
            seller_adapter.compensation_methods.append(("delete_user", user_id, headers))
            seller_adapter.create_seller(new_seller_schema, headers)
    return {"msg": f'El usuario {json_response.get("user", new_user_schema.user)} fue creado exitosamente.'}


@session_router.get("/refresh_token")
def refresh_token(request: Request, response: Response, token: str = Depends(common.token_schema)):
    adapter = adapters.AuthAdapter()
    headers = dict(request.headers.items())
    response.status_code, json_response = adapter.refresh_token(headers)
    return json_response


@session_router.get("/verify_token")
def verify_token(request: Request, response: Response, token: str = Depends(common.token_schema)):
    adapter = adapters.AuthAdapter()
    headers = dict(request.headers.items())
    response.status_code, json_response = adapter.verify_token(headers)
    return json_response


@session_router.post("/verify_roles")
def verify_roles(roles_schema: schemas.RolesSchema, request: Request, response: Response,
                 token: str = Depends(common.token_schema)):
    adapter = adapters.AuthAdapter()
    headers = dict(request.headers.items())
    response.status_code, json_response = adapter.verify_roles(roles_schema, headers)
    return json_response


@session_router.post("/login")
def login(user_schema: schemas.LoginUserSchema, response: Response):
    adapter = adapters.AuthAdapter()
    response.status_code, json_response = adapter.login(user_schema)
    return json_response


__all__ = ["session_router"]
