import datetime
import typing

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

class CreateInventorySchema(pydantic.BaseModel):
    productId: str 
    stock:int
    class Config:
        use_enum_values = True

class UpdateInventorySchema(pydantic.BaseModel):
    stock:int
    class Config:
        use_enum_values = True

__all__ = ['LoginUserSchema', 'CreateUserSchema', 'UserSchema', 'LoginResponseSchema', 'CreateInventorySchema','UpdateInventorySchema']
