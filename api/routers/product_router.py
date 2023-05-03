import traceback

import helpers
import common
import adapters
import schemas

from fastapi import APIRouter, Depends, Response, Request

import typing

product_router = APIRouter(prefix="/products", tags=["products resource"])


@product_router.get("/{product_id}")
def get_product(product_id: typing.Union[str, int], request: Request, response: Response, relations: bool = True,
                token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*args, **kwargs):
        params = {"relations": relations}
        products_adapter = adapters.ProductsAdapter()
        inventory_adapter = adapters.InventoryAdapter()
        products_adapter.params = params
        response.status_code, product_json_response = products_adapter.get_product(product_id)
        if isinstance(product_json_response, dict):
            _, inventory = inventory_adapter.get_inventory(product_id)
            if isinstance(inventory, dict) and isinstance((stock := inventory.get("stock")), int):
                product_json_response["stock"] = stock
        return product_json_response

    return method(request=request, response=response)


@product_router.get("")
def get_products(request: Request, response: Response, skip: typing.Optional[int] = None,
                 take: typing.Optional[int] = None, relations: bool = True, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*args, **kwargs):
        params = {"skip": skip, "take": take, "relations": relations}
        products_adapter = adapters.ProductsAdapter()
        inventory_adapter = adapters.InventoryAdapter()
        products_adapter.params = params
        response.status_code, products_json_response = products_adapter.get_products()
        if isinstance(products_json_response, typing.List):
            for i, p in enumerate(products_json_response):
                if product_id := p.get("id"):
                    try:
                        _, inventory = inventory_adapter.get_inventory(product_id)
                        if isinstance(inventory, dict) and isinstance((stock := inventory.get("stock")), int):
                            products_json_response[i]["stock"] = stock
                    except:
                        helpers.global_logger.error(traceback.format_exc())

        return products_json_response

    return method(request=request, response=response)


@product_router.post("")
def create_product(product_schema: schemas.CreateProductSchema, request: Request,
                   response: Response, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "MARKETING"])
    def method(*args, **kwargs):
        products_adapter = adapters.ProductsAdapter()
        inventory_adapter = adapters.InventoryAdapter()
        response.status_code, json_response = products_adapter.create_product(product_schema)
        new_inventory_schema: typing.Optional[schemas.CreateInventorySchema] = None
        if json_response and (product_id := json_response.get("id", None)):
            new_inventory_schema = schemas.CreateInventorySchema(**{"product_id": product_id, "stock": 0})
        else:
            return json_response
        inventory_adapter.compensation_methods.append(("delete_product", product_id))
        inventory_adapter.create_inventory(new_inventory_schema)
        return json_response

    return method(request=request, response=response)


__all__ = ["product_router"]
