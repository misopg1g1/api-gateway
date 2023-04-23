import enums
import schemas
import common
import adapters

from fastapi import APIRouter, Depends, Response, Request

product_router = APIRouter(prefix="/products", tags=["mock resource"])


@product_router.get("/products")
def getAll(productId: int,request: Request, response: Response,
                token: str = Depends(common.token_schema)):
    adapter = adapters.ProductAdapter()
    headers = dict(request.headers.items())
    status_code, json_response = adapter.getAll(headers,productId)
    response.status_code = status_code
    return json_response

@product_router.get("/products/{productId}")
def get(productId: int,request: Request, response: Response,
                token: str = Depends(common.token_schema)):
    adapter = adapters.ProductAdapter()
    headers = dict(request.headers.items())
    status_code, json_response = adapter.get(headers,productId)
    response.status_code = status_code
    return json_response



__all__ = ["product_router"]