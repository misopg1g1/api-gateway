import typing
import schemas
import common
import adapters

from fastapi import APIRouter, Depends, Response, Request

seller_router = APIRouter(prefix="", tags=["seller resource"])

@seller_router.get("/sellers")
def get_sellers(request: Request, response: Response, skip: typing.Optional[int] = None,
                    take: typing.Optional[int] = None, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER"])
    def method(*args, **kwargs):
        params = {"skip": skip, "take": take}
        seller_adapter = adapters.SellersAdapter()
        seller_adapter.params = params
        response.status_code, json_response = seller_adapter.get_sellers()
        return json_response

    return method(request=request, response=response)

@seller_router.post("/sellers")
def create_seller(new_seller_schema: schemas.CreateSellerSchema, request: Request, response: Response,
                     token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN"])
    def method(*arg, **kwarg):
        seller_adapter = adapters.SellersAdapter()
        response.status_code, json_response = seller_adapter.create_seller(new_seller_schema)
        return json_response

    return method(request=request, response=response)

@seller_router.get("/sellers/{seller_id}")
def get_seller(seller_id: typing.Union[str, int], request: Request, response: Response,
                  token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER"])
    def method(*arg, **kwargs):
        seller_adapter = adapters.SellersAdapter()
        response.status_code, json_response = seller_adapter.get_seller(seller_id)
        return json_response

    return method(request=request, response=response)

@seller_router.put("/sellers/{seller_id}")
def put_seller(update_seller_schema: schemas.UpdateSellerSchema, seller_id: typing.Union[str, int],
                  request: Request, response: Response,
                  token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN"])
    def method(*arg, **kwargs):
        seller_adapter = adapters.SellersAdapter()
        response.status_code, json_response = seller_adapter.put_seller(update_seller_schema, seller_id)
        return json_response

    return method(request=request, response=response)

@seller_router.post("/sellers/{seller_id}/visits/{visit_id}")
def add_visit_to_seller(seller_id: typing.Union[str, int], visit_id: typing.Union[str, int], 
                        request: Request, response: Response,
                        token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN"])
    def method(*arg, **kwarg):
        seller_adapter = adapters.SellersAdapter()
        response.status_code, json_response = seller_adapter.add_visit_to_seller (seller_id, visit_id)
        return json_response

    return method(request=request, response=response)

@seller_router.get("/sellers/{seller_id}/visits/{visit_id}")
def get_visit_from_seller(seller_id: typing.Union[str, int], visit_id: typing.Union[str, int], 
                        request: Request, response: Response,
                        token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER"])
    def method(*arg, **kwarg):
        seller_adapter = adapters.SellersAdapter()
        response.status_code, json_response = seller_adapter.get_visit_to_seller (seller_id, visit_id)
        return json_response

    return method(request=request, response=response)

@seller_router.get("/sellers/{seller_id}/visits")
def get_visits_from_seller(seller_id: typing.Union[str, int], request: Request, response: Response,
                        token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER"])
    def method(*arg, **kwarg):
        seller_adapter = adapters.SellersAdapter()
        response.status_code, json_response = seller_adapter.get_visits_to_seller (seller_id)
        return json_response

    return method(request=request, response=response)

@seller_router.get("/visits")
def get_visits(request: Request, response: Response, skip: typing.Optional[int] = None,
                    take: typing.Optional[int] = None, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER"])
    def method(*args, **kwargs):
        params = {"skip": skip, "take": take}
        seller_adapter = adapters.SellersAdapter()
        seller_adapter.params = params
        response.status_code, json_response = seller_adapter.get_visits()
        return json_response

    return method(request=request, response=response)

@seller_router.post("/visits")
def create_visit(new_visit_schema: schemas.CreateVisitSchema, request: Request, response: Response,
                     token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER"])
    def method(*arg, **kwarg):
        seller_adapter = adapters.SellersAdapter()
        response.status_code, json_response = seller_adapter.create_visit(new_visit_schema)
        return json_response

    return method(request=request, response=response)

@seller_router.get("/visits/{visit_id}")
def get_visit(visit_id: typing.Union[str, int], request: Request, response: Response,
                  token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER"])
    def method(*arg, **kwargs):
        seller_adapter = adapters.SellersAdapter()
        response.status_code, json_response = seller_adapter.get_visit(visit_id)
        return json_response

    return method(request=request, response=response)

@seller_router.put("/visits/{visit_id}")
def put_visit(update_visit_schema: schemas.UpdateVisitSchema, visit_id: typing.Union[str, int],
                  request: Request, response: Response,
                  token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN","SELLER"])
    def method(*arg, **kwargs):
        seller_adapter = adapters.SellersAdapter()
        response.status_code, json_response = seller_adapter.put_visit(update_visit_schema, visit_id)
        return json_response

    return method(request=request, response=response)