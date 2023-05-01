import helpers
from enums import RoleEnum, ProductType

import pydantic
import datetime
import typing
import base64

CREATE_PRODUCT_EXAMPLE = {
    "name": "Lechuga",
    "dimensions": [1, 2, 3],
    "type": "PERISHABLE",
    "temperature_control": 20,
    "expiration_date": f"{datetime.datetime.now().date()}",
    "fragility_conditions": "Es muy fragil",
    "description": "Vegetal verde para hacer hamburguesas",
    "status": True,
    "price": 25000,
    "img_base64_data": base64.b64encode(open("./public/no-image.jpg", "rb").read()).decode(),
    "suppliers": ["Exito"],
    "categories": ["Vegetales"]
}

CREATE_CATEGORY_EXAMPLE = {
    "name": "Verduras",
    "description": "Alimentos verdes"
}

PATCH_CATEGORY_EXAMPLE = {
    "name": "Verduras",
    "description": "Alimentos verdes como el brocoli",
    "status": False
}


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
    product_id: str
    stock: int

    class Config:
        use_enum_values = True


class UpdateInventorySchema(pydantic.BaseModel):
    stock: int

    class Config:
        use_enum_values = True


class RolesSchema(pydantic.BaseModel):
    hash: typing.Optional[str]
    roles: typing.List[RoleEnum] = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {
                'hash': '8f3c88c7f5dc8d10ba80d45f77280e8d',
                'roles': ['ADMIN', 'SELLER']

            }
        }


class CreateProductSchema(pydantic.BaseModel):
    name: str = pydantic.Field(...)
    dimensions: typing.Optional[str] = pydantic.Field(default="")
    type: ProductType = pydantic.Field(...)
    temperature_control: typing.Optional[int] = pydantic.Field(default="")
    expiration_date: typing.Optional[str] = pydantic.Field(...)
    fragility_conditions: typing.Optional[str] = pydantic.Field(default="")
    description: typing.Optional[str] = pydantic.Field(default="")
    status: typing.Optional[bool] = pydantic.Field(default=True)
    price: int = pydantic.Field(...)
    img_base64_data: typing.Optional[str] = pydantic.Field(...)
    suppliers: typing.Optional[typing.List[str]] = pydantic.Field(default=[])
    categories: typing.List[str] = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {**CREATE_PRODUCT_EXAMPLE, "hash": helpers.get_hash(CREATE_PRODUCT_EXAMPLE)}
        }


class CreateCategorySchema(pydantic.BaseModel):
    name: str = pydantic.Field(...)
    description: str = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {**CREATE_CATEGORY_EXAMPLE, "hash": helpers.get_hash(CREATE_CATEGORY_EXAMPLE)}
        }


class PatchCategorySchema(CreateCategorySchema):
    name: typing.Optional[str] = pydantic.Field(...)
    description: typing.Optional[str] = pydantic.Field(...)
    status: typing.Optional[bool] = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {**PATCH_CATEGORY_EXAMPLE, "hash": helpers.get_hash(PATCH_CATEGORY_EXAMPLE)}
        }


__all__ = ['LoginUserSchema', 'CreateUserSchema', 'UserSchema', 'LoginResponseSchema',
           'RolesSchema', 'CreateInventorySchema', 'UpdateInventorySchema', 'CreateProductSchema',
           'CreateCategorySchema', 'PatchCategorySchema']
