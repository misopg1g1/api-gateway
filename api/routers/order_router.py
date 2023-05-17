import common
import publishers
import schemas
import adapters
import helpers
from .inventory_router import get_inventory, put_inventory

from .seller_router import get_visit, put_visit
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
                    product = get_product(product_id, request, response, False, token)
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
        dict_stock_request = {}
        for item in new_order_schema.items:
            product = get_product(item.product_id, request, response, False, token)
            inventory = get_inventory(item.product_id, request, response, token)
            if (product_stock := inventory.get("stock")) >= 0:
                if dict_stock_request.get(item.product_id):
                    dict_stock_request[item.product_id] += item.quantity
                else:
                    dict_stock_request[item.product_id] = item.quantity
                if dict_stock_request.get(item.product_id) > product_stock:
                    raise common.error_handling.Conflict(
                        common.ResponseMessagesValues.INSUFFICIENT_STOCK(product.get("name"), product_stock))
            new_order_schema.grand_total += item.quantity * product.get("price")

        get_visit(new_order_schema.visit_id, request, response, token)
        order_adapter = adapters.OrdersAdapter()
        response.status_code, json_response = order_adapter.create_order(new_order_schema, headers)
        if json_response and (order_id := json_response.get("id")):
            put_visit(new_order_schema.visit_id, request, response, token, {"order_id": order_id})
            for product_id, stock_to_remove in dict_stock_request.items():
                stock_update = schemas.UpdateInventorySchema(stock=-stock_to_remove)
                put_inventory(stock_update, product_id, request, response, token)
            if (newly_created_order := get_order(order_id, request, response, True, token)) and \
                    isinstance(newly_created_order, dict) and newly_created_order.get("id"):
                try:
                    publishers.new_order_email_publisher.publish_user_to_verify(newly_created_order)
                except:
                    helpers.global_logger.getChild("create_order").error("No se pudo publicar "
                                                                         "el mensaje en la cola de mensajeria")
        return json_response

    return method(request=request, response=response)


__all__ = ["order_router"]
