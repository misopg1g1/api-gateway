import typing
import schemas
import common
import adapters

from fastapi import APIRouter, Depends, Response, Request, Body

seller_router = APIRouter(prefix="", tags=["seller resource"])


@seller_router.get("/sellers")
def get_sellers(request: Request, response: Response, skip: typing.Optional[int] = None,
                take: typing.Optional[int] = None, relations: bool = True, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "MARKETING"])
    def method(*args, **kwargs):
        params = {"skip": skip, "take": take, "relations": relations}
        seller_adapter = adapters.SellersAdapter()
        seller_adapter.params = params
        headers = dict(request.headers.items())
        response.status_code, json_response = seller_adapter.get_sellers(headers)
        return json_response

    return method(request=request, response=response)


@seller_router.get("/sellers/{seller_id}")
def get_seller(seller_id: typing.Union[str, int], request: Request, response: Response,
               skip: typing.Optional[int] = None, take: typing.Optional[int] = None, relations: bool = True,
               token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    @common.verify_identity_for_seller_resources(seller_id)
    def method(*arg, **kwargs):
        headers = dict(request.headers.items())
        params = {"skip": skip, "take": take, "relations": relations}
        seller_adapter = adapters.SellersAdapter()
        seller_adapter.params = params
        response.status_code, json_response = seller_adapter.get_seller(seller_id, headers)
        return json_response

    return method(request=request, response=response)


@seller_router.put("/sellers/{seller_id}")
def put_seller(seller_id: typing.Union[str, int], request: Request, response: Response,
               update_seller_schema: typing.Any = Body(example={"first_name": "Andres"}),
               token: str = Depends(common.token_schema)):
    """
        El body puede ser parcial para cambiar solo un elemento del objeto y no todo el objeto.
    """

    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    @common.verify_identity_for_seller_resources(seller_id)
    def method(*arg, **kwargs):
        seller_adapter = adapters.SellersAdapter()
        headers = dict(request.headers.items())
        response.status_code, json_response = seller_adapter.put_seller(seller_id, update_seller_schema, headers)
        return json_response

    return method(request=request, response=response)


# @seller_router.post("/sellers/{seller_id}/visits/{visit_id}")
# def add_visit_to_seller(seller_id: typing.Union[str, int], visit_id: typing.Union[str, int],
#                         request: Request, response: Response,
#                         token: str = Depends(common.token_schema)):
#     @common.verify_identity(seller_id)
#     @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
#     def method(*arg, **kwarg):
#         seller_adapter = adapters.SellersAdapter()
#         headers = dict(request.headers.items())
#         response.status_code, json_response = seller_adapter.add_visit_to_seller(seller_id, visit_id, headers)
#         return json_response
#
#     return method(request=request, response=response)


@seller_router.get("/sellers/{seller_id}/visits/{visit_id}")
def get_visit_from_seller(seller_id: typing.Union[str, int], visit_id: typing.Union[str, int],
                          request: Request, response: Response,
                          token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    @common.verify_identity_for_seller_resources(seller_id)
    def method(*arg, **kwarg):
        seller_adapter = adapters.SellersAdapter()
        headers = dict(request.headers.items())
        response.status_code, json_response = seller_adapter.get_visit_to_seller(seller_id, visit_id, headers)
        return json_response

    return method(request=request, response=response)


@seller_router.get("/sellers/{seller_id}/visits")
def get_visits_from_seller(seller_id: typing.Union[str, int], request: Request, response: Response,
                           token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    @common.verify_identity_for_seller_resources(seller_id)
    def method(*arg, **kwarg):
        seller_adapter = adapters.SellersAdapter()
        headers = dict(request.headers.items())
        response.status_code, json_response = seller_adapter.get_visits_to_seller(seller_id, headers)
        return json_response

    return method(request=request, response=response)


@seller_router.get("/visits")
def get_visits(request: Request, response: Response, skip: typing.Optional[int] = None,
               take: typing.Optional[int] = None,
               token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    @common.verify_identity_for_seller_resources()
    def method(*args, **kwargs):
        params = {"skip": skip, "take": take, "relations": True}
        seller_adapter = adapters.SellersAdapter()
        customer_adapter = adapters.CustomersAdapter()
        seller_adapter.params = params
        customer_adapter.params = {"relations": True}
        headers = dict(request.headers.items())
        response.status_code, json_response = seller_adapter.get_visits(headers=headers)
        if isinstance(json_response, list):
            new_json_response = []
            for visit in json_response:
                try:
                    if customer_id := visit.get("customer_id"):
                        customer_status_code, customer_json_response = customer_adapter.get_customer(customer_id)
                        new_json_response.append({**dict(filter(lambda kv: kv[0] != "customer_id",
                                                                visit.items())), "customer": customer_json_response})
                except Exception as e:
                    new_json_response.append(visit)
            return new_json_response
        return json_response

    return method(request=request, response=response)


@seller_router.post("/visits")
def create_visit(new_visit_schema: schemas.CreateVisitSchema, request: Request, response: Response,
                 token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["SELLER"])
    @common.verify_identity_for_seller_resources()
    def method(*arg, **kwarg):
        new_visit_schema.seller_id = kwarg.get("seller_id")
        seller_adapter = adapters.SellersAdapter()
        headers = dict(request.headers.items())
        response.status_code, json_response = seller_adapter.create_visit(new_visit_schema, headers=headers)
        return json_response

    return method(request=request, response=response)


@seller_router.get("/visits/{visit_id}")
def get_visit(visit_id: typing.Union[str, int], request: Request, response: Response,
              token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    @common.verify_identity_for_seller_resources()
    def method(*arg, **kwargs):
        params = {"relations": True}
        seller_adapter = adapters.SellersAdapter()
        customer_adapter = adapters.CustomersAdapter()
        headers = dict(request.headers.items())
        seller_adapter.params = params
        customer_adapter.params = params
        response.status_code, json_response = seller_adapter.get_visit(visit_id, headers)
        try:
            if customer_id := json_response.get("customer_id"):

                customer_status_code, customer_json_response = customer_adapter.get_customer(customer_id)
                return {**dict(filter(lambda kv: kv[0] != "customer_id",
                                      json_response.items())), "customer": customer_json_response}
            else:
                return json_response
        except Exception as e:
            return json_response

    return method(request=request, response=response)


@seller_router.put("/visits/{visit_id}")
def put_visit(visit_id: typing.Union[str, int], request: Request, response: Response,
              token: str = Depends(common.token_schema),
              update_visit_schema: typing.Any = Body(example={"description": "Some description"})):
    """
        El body puede ser parcial para cambiar solo un elemento del objeto y no todo el objeto.
    """

    @common.verify_role_middleware(["ADMIN", "SELLER", "MARKETING"])
    @common.verify_identity_for_seller_resources()
    def method(*arg, **kwargs):
        seller_adapter = adapters.SellersAdapter()
        headers = dict(request.headers.items())
        response.status_code, json_response = seller_adapter.put_visit(visit_id, update_visit_schema, headers)
        return json_response

    return method(request=request, response=response)
