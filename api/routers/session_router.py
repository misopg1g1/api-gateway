import schemas
import common
import adapters

from fastapi import APIRouter, Depends, Response

session_router = APIRouter(prefix="/session", tags=["mock resource"])


@session_router.post("/create_user")
def create_user(new_user_schema: schemas.CreateUserSchema, token: str = Depends(common.token_schema)):
    pass


@session_router.post("/login")
def login(user_schema: schemas.LoginUserSchema, response: Response):
    adapter = adapters.AuthAdapter()
    status_code, json_response = adapter.login(user_schema)
    response.status_code = status_code
    return json_response


__all__ = ["session_router"]
