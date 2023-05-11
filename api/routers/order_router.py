import common
import schemas
import adapters
import helpers

from .seller_router import get_visit
from .product_router import get_product

import typing
import traceback
from fastapi import APIRouter, Depends, Response, Request

order_router = APIRouter(prefix="/orders", tags=["orders resource"])


@order_router.get("")
def get_orders(request: Request, response: Response, skip: typing.Optional[int] = None,
               take: typing.Optional[int] = None, relations: bool = True, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    def method(*args, **kwargs):
        pass

    return method(request=request, response=response)


@order_router.get("/{order_id}")
def get_order(order_id: typing.Union[str, int], request: Request, response: Response, relations: bool = True,
              token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    def method(*args, **kwargs):
        pass

    return method(request=request, response=response)


@order_router.post("")
def create_order(new_order_schema: schemas.CreateOrderSchema, request: Request,
                 response: Response, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["SELLER"])
    def method(*args, **kwargs):
        headers = dict(request.headers.items())
        visit = get_visit(new_order_schema.visit_id, request, response, token)
        for item in new_order_schema.items:
            product = get_product(item.product_id, request, response, False, token)
            new_order_schema.grand_total += item.quantity * product.get("price")
        order_adapter = adapters.OrdersAdapter()
        response.status_code, json_response = order_adapter.create_order(new_order_schema, headers)
        return json_response

    return method(request=request, response=response)


__all__ = ["order_router"]
