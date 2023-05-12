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


def get_item_product(order, request, response, token):
    extended_items = []
    if (items := order.get("items")) and isinstance(items, list):
        for item in items:
            extended_item = item
            if product_id := item.get("product_id"):
                try:
                    _, product = get_product(product_id, request, response, False, token)
                    extended_item = {**item, "product_name": product.get("name")}
                except:
                    helpers.global_logger.getChild("OrderItem").error(traceback.format_exc())
            extended_items.append(extended_item)
    return extended_items


@order_router.get("")
def get_orders(request: Request, response: Response, skip: typing.Optional[int] = None,
               take: typing.Optional[int] = None, relations: bool = True, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    @common.verify_identity_for_order_resources()
    def method(*args, **kwargs):
        headers = dict(request.headers.items())
        orders_adapter = adapters.OrdersAdapter()
        orders_adapter.params = {"skip": skip, "take": take, "relations": relations}
        response.status_code, orders = orders_adapter.get_orders(headers=headers)
        new_orders_list = []
        if not isinstance(orders, typing.List):
            return orders
        for order in orders:
            visit_id = order.get("visit_id")
            if not visit_id:
                extended_order = order
            else:
                order["items"] = get_item_product(order, request, response, token)
                visit = get_visit(visit_id, request, response, token)
                seller = visit.get("seller")
                customer = visit.get("customer")
                extended_order = {**order, "seller": seller, "customer": customer}
            new_orders_list.append(extended_order)
        return new_orders_list

    return method(request=request, response=response)


@order_router.get("/{order_id}")
def get_order(order_id: typing.Union[str, int], request: Request, response: Response, relations: bool = True,
              token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    @common.verify_identity_for_order_resources()
    def method(*args, **kwargs):
        headers = dict(request.headers.items())
        orders_adapter = adapters.OrdersAdapter()
        orders_adapter.params = {"relations": relations}
        response.status_code, order = orders_adapter.get_order(order_id, headers)
        visit_id = order.get("visit_id")
        order["items"] = get_item_product(order, request, response, token)
        if visit_id:
            visit = get_visit(visit_id, request, response, token)
            seller = visit.get("seller")
            customer = visit.get("customer")
            return {**order, "seller": seller, "customer": customer}
        else:
            return order

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
