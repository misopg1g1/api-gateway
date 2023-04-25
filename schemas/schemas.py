import datetime
import typing

import enums
from enums import RoleEnum

import pydantic


class LoginUserSchema(pydantic.BaseModel):
    hash: str = pydantic.Field(example='f2a125a706fea29d8bd81d9cfc6c52c4')
    user: str = pydantic.Field(example='user1')
    password: str = pydantic.Field(example='password1')


class CreateUserSchema(LoginUserSchema):
    verify_password: str = pydantic.Field(...)
    role: typing.Optional[RoleEnum] = pydantic.Field(default=RoleEnum.SELLER)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {
                'hash': '04ea08e045e25e0959e6907fa96bffa4',
                'user': 'user2',
                'password': 'password2',
                'verify_password': 'password2',
                'role': 'ADMIN'

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


class RolesSchema(pydantic.BaseModel):
    hash: typing.Optional[str]
    roles: typing.List[enums.RoleEnum] = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {
                'hash': '8f3c88c7f5dc8d10ba80d45f77280e8d',
                'roles': ['ADMIN', 'SELLER']

            }
        }


__all__ = ['LoginUserSchema', 'CreateUserSchema', 'UserSchema', 'LoginResponseSchema', 'RolesSchema']
