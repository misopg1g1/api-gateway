import helpers
from enums import RoleEnum, ProductType, ZoneEnum, IdentificationTypeEnum

import pydantic
import datetime
import typing
import base64

CREATE_PRODUCT_EXAMPLE = {"name": "asdf", "description": "asdf", "type": "PERISHABLE", "categories": ["Verduras"],
                          "price": 1232131}

CREATE_CUSTOMER_EXAMPLE = {
    "registered_name": "Acme",
    "first_name": "John",
    "last_name": "Doe",
    "identification": {
        "number": "123456789",
        "type": "DNI"
    },
    "seller_id": "seller 3",
    "address": {
        "country": "Honduras",
        "city": "Choloma",
        "zone": "ZONA CENTRO",
        "address": "Calle ciega, 55",
        "postal_code": "111111"
    },
    "phone": "123456789",
    "email": "john.doe@acme.com"
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

CREATE_SELLER_EXAMPLE = {
    "id": "a80ed738-ed20-11ed-a05b-0242ac120003"
}

UPDATE_SELLER_EXAMPLE = {
    "first_name": "Juan",
    "last_name": "Pérez",
    "sales_commission": 10,
    "status": False
}

CREATE_VISIT_EXAMPLE = {
    "visit_date": "2023-06-07",
    "description": "Ejemplo de visita",
    "order_id": "2b93fb04-ed28-11ed-a05b-0242ac120003"
}

UPDATE_VISIT_EXAMPLE = {
    "visit_date": "2023-06-07",
    "description": "Cambio descripcion",
    "order_id": "2b93fb04-ed28-11ed-a05b-0242ac120003"
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
    temperature_control: typing.Optional[int] = pydantic.Field(default=0)
    expiration_date: typing.Optional[str] = pydantic.Field(default=str(datetime.datetime.fromtimestamp(0)))
    fragility_conditions: typing.Optional[str] = pydantic.Field(default="")
    description: typing.Optional[str] = pydantic.Field(default="")
    status: typing.Optional[bool] = pydantic.Field(default=True)
    price: int = pydantic.Field(...)
    img_base64_data: typing.Optional[str] = pydantic.Field(default="")
    suppliers: typing.Optional[typing.List[str]] = pydantic.Field(default="")
    categories: typing.Optional[typing.List[str]] = []

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


class CreateAddressSchema(pydantic.BaseModel):
    address: str = pydantic.Field(...)
    city: str = pydantic.Field(...)
    country: str = pydantic.Field(...)
    zone: ZoneEnum = pydantic.Field(...)
    postal_code: typing.Optional[str] = pydantic.Field(...)

    class Config:
        use_enum_values = True


class CreateIdentificationSchema(pydantic.BaseModel):
    number: str = pydantic.Field(...)
    type: IdentificationTypeEnum = pydantic.Field(...)

    class Config:
        use_enum_values = True


class CreateCustomerSchema(pydantic.BaseModel):
    registered_name: str = pydantic.Field(...)
    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    financial_alert: typing.Optional[bool]
    seller_id: str = pydantic.Field(...)
    phone: str = pydantic.Field(...)
    email: str = pydantic.Field(...)
    address: CreateAddressSchema = pydantic.Field(...)
    identification: CreateIdentificationSchema = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {**CREATE_CUSTOMER_EXAMPLE, "hash": helpers.get_hash(CREATE_CUSTOMER_EXAMPLE)}
        }

class CreateSellerSchema(pydantic.BaseModel):
    id: str = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {**CREATE_SELLER_EXAMPLE, "hash": helpers.get_hash(CREATE_SELLER_EXAMPLE)}
        }

class UpdateSellerSchema(pydantic.BaseModel):
    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    sales_commission: int = pydantic.Field(...)
    status: typing.Optional[bool] = pydantic.Field()

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {**UPDATE_SELLER_EXAMPLE, "hash": helpers.get_hash(UPDATE_SELLER_EXAMPLE)}
        }

class CreateVisitSchema(pydantic.BaseModel):
    img_base64_data: typing.Optional[str] = pydantic.Field(default="")
    visit_date: typing.Optional[str] = pydantic.Field(default=str(datetime.datetime.fromtimestamp(0)))
    description: typing.Optional[str] = pydantic.Field(default="")
    order_id: str = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {**CREATE_VISIT_EXAMPLE, "hash": helpers.get_hash(CREATE_VISIT_EXAMPLE)}
        }

class UpdateVisitSchema(pydantic.BaseModel):
    img_base64_data: typing.Optional[str] = pydantic.Field(default="")
    visit_date: typing.Optional[str] = pydantic.Field(default=str(datetime.datetime.fromtimestamp(0)))
    description: typing.Optional[str] = pydantic.Field(default="")
    order_id: str = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {**UPDATE_VISIT_EXAMPLE, "hash": helpers.get_hash(UPDATE_VISIT_EXAMPLE)}
        }

__all__ = ['LoginUserSchema', 'CreateUserSchema', 'UserSchema', 'LoginResponseSchema',
           'RolesSchema', 'CreateInventorySchema', 'UpdateInventorySchema', 'CreateProductSchema',
           'CreateCategorySchema', 'PatchCategorySchema', 'CreateCustomerSchema', 'CREATE_PRODUCT_EXAMPLE',
           'CREATE_CATEGORY_EXAMPLE', 'PATCH_CATEGORY_EXAMPLE','CreateSellerSchema','CREATE_SELLER_EXAMPLE',
           'CreateVisitSchema','CREATE_VISIT_EXAMPLE','UpdateVisitSchema','UPDATE_VISIT_EXAMPLE',
           'UpdateSellerSchema','UPDATE_SELLER_EXAMPLE']
