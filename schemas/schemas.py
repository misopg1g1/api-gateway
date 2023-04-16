import datetime
import typing

from enums import RoleEnum

import pydantic


class UserOperationSchema(pydantic.BaseModel):
    requester_user_password: typing.Optional[str] = pydantic.Field(...)


class LoginUserSchema(pydantic.BaseModel):
    hash: str = pydantic.Field(example='4c43e4f140f341bd5c28d8a8cbd97e35')
    user: str = pydantic.Field(example='user1')
    password: str = pydantic.Field(example='password1')


class CreateUserSchema(LoginUserSchema, UserOperationSchema):
    verify_password: str = pydantic.Field(...)
    role: RoleEnum = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {
                'hash': 'a78f864ae5a0398867ede61c6b8c5359',
                'user': 'user2',
                'password': 'password2',
                'verify_password': 'password2',
                'role': 'ADMIN',
                'requester_user_password': 'password1'

            }
        }


class UserSchemaWithoutPassword(pydantic.BaseModel):
    id: typing.Optional[int]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    user: str
    verified: bool
    enabled: bool
    role: str

    class Config:
        use_enum_values = True


class UserSchema(UserSchemaWithoutPassword):
    password: str

    class Config:
        use_enum_values = True


class LoginResponseSchema(pydantic.BaseModel):
    access_token: str
    token_type: str
    data: UserSchemaWithoutPassword


__all__ = ['LoginUserSchema', 'CreateUserSchema', 'UserSchema', 'LoginResponseSchema']
