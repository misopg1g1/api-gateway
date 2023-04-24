import enums
import schemas
import common
import adapters

from fastapi import APIRouter, Depends, Response, Request

inventory_router = APIRouter(prefix="", tags=["inventory resource"])

@inventory_router.post("/inventories")
def create_inventory(new_inventory_schema: schemas.CreateInventorySchema, request: Request, response: Response,
                token: str = Depends(common.token_schema)):
    adapter = adapters.InventoryAdapter()
    headers = dict(request.headers.items())
    status_code, json_response = adapter.create_inventory(new_inventory_schema, headers)
    response.status_code = status_code
    return json_response


@inventory_router.get("/products/:productId/inventory")
def get_inventory(productId: str, request: Request, response: Response, token: str = Depends(common.token_schema)):
    adapter = adapters.InventoryAdapter()
    headers = dict(request.headers.items())
    status_code, json_response = adapter.get_inventory(productId, headers)
    response.status_code = status_code
    return json_response

@inventory_router.get("/inventories")
def get_inventories(request: Request, response: Response, token: str = Depends(common.token_schema)):
    adapter = adapters.InventoryAdapter()
    headers = dict(request.headers.items())
    status_code, json_response = adapter.get_inventories(headers)
    response.status_code = status_code
    return json_response

@inventory_router.put("/products/:productId/inventory")
def put_inventory(update_inventory_schema: schemas.UpdateInventorySchema,productId: str, request: Request, response: Response, token: str = Depends(common.token_schema)):
    adapter = adapters.InventoryAdapter()
    headers = dict(request.headers.items())
    status_code, json_response = adapter.put_inventory(update_inventory_schema ,productId, headers)
    response.status_code = status_code
    return json_response