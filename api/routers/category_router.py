import typing

import common
import adapters

from fastapi import APIRouter, Depends, Response, Request

import schemas

category_router = APIRouter(prefix="/categories", tags=["categories resource"])


@category_router.get("")
def get_categories(request: Request, response: Response, category_id: typing.Optional[str] = None,
                   name: typing.Optional[str] = None,
                   relations: bool = True, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*args, **kwargs):
        params = {"name": name, "categoryId": category_id, "relations": relations}
        params = dict(filter(lambda kv: kv[1] or kv[0] in ["relations"], params.items()))
        products_adapter = adapters.ProductsAdapter()
        products_adapter.params = params
        response.status_code, json_response = products_adapter.get_categories()
        return json_response

    return method(request=request, response=response)


@category_router.post("")
def create_category(category_schema: schemas.CreateCategorySchema, request: Request,
                    response: Response, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "MARKETING"])
    def method(*args, **kwargs):
        products_adapter = adapters.ProductsAdapter()
        response.status_code, json_response = products_adapter.create_category(category_schema)
        return json_response

    return method(request=request, response=response)


@category_router.patch("{category_id}")
def patch_category(category_id: str, category_schema: schemas.PatchCategorySchema, request: Request,
                   response: Response, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "MARKETING"])
    def method(*args, **kwargs):
        products_adapter = adapters.ProductsAdapter()
        response.status_code, json_response = products_adapter.patch_category(category_id, category_schema)
        return json_response

    return method(request=request, response=response)


__all__ = ["category_router"]
