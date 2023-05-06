import typing
import schemas
import common
import adapters

from fastapi import APIRouter, Depends, Response, Request

inventory_router = APIRouter(prefix="", tags=["inventory resource"])


@inventory_router.post("/inventories")
def create_inventory(new_inventory_schema: schemas.CreateInventorySchema, request: Request, response: Response,
                     token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*arg, **kwarg):
        inventory_adapter = adapters.InventoryAdapter()
        response.status_code, json_response = inventory_adapter.create_inventory(new_inventory_schema)
        return json_response

    return method(request=request, response=response)


@inventory_router.get("/products/{product_id}/inventory")
def get_inventory(product_id: typing.Union[str, int], request: Request, response: Response,
                  token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*arg, **kwargs):
        inventory_adapter = adapters.InventoryAdapter()
        response.status_code, json_response = inventory_adapter.get_inventory(product_id)
        return json_response

    return method(request=request, response=response)


@inventory_router.get("/inventories")
def get_inventories(request: Request, response: Response, skip: typing.Optional[int] = None,
                    take: typing.Optional[int] = None, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*args, **kwargs):
        params = {"skip": skip, "take": take}
        inventory_adapter = adapters.InventoryAdapter()
        inventory_adapter.params = params
        response.status_code, json_response = inventory_adapter.get_inventories()
        return json_response

    return method(request=request, response=response)


@inventory_router.put("/products/{productId}/inventory")
def put_inventory(update_inventory_schema: schemas.UpdateInventorySchema, productId: typing.Union[str, int],
                  request: Request, response: Response,
                  token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*arg, **kwargs):
        inventory_adapter = adapters.InventoryAdapter()
        response.status_code, json_response = inventory_adapter.put_inventory(update_inventory_schema, productId)
        return json_response

    return method(request=request, response=response)
