import typing

import common
import adapters

from fastapi import APIRouter, Depends, Response, Request

import schemas

product_router = APIRouter(prefix="/products", tags=["products resource"])


@product_router.get("/{product_id}")
def get_product(product_id: typing.Union[str, int], request: Request, response: Response,
                token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*args, **kwargs):
        products_adapter = adapters.ProductsAdapter()
        response.status_code, json_response = products_adapter.get_product(product_id)
        return json_response

    return method(request=request, response=response)


@product_router.get("")
def get_products(request: Request, response: Response, skip: typing.Optional[int] = None,
                 take: typing.Optional[int] = None, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*args, **kwargs):
        params = {"skip": skip, "take": take}
        products_adapter = adapters.ProductsAdapter()
        products_adapter.params = params
        response.status_code, json_response = products_adapter.get_products()
        return json_response

    return method(request=request, response=response)


__all__ = ["product_router"]
