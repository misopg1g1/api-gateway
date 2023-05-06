import common
import schemas
import adapters
import helpers

import typing
import traceback
from fastapi import APIRouter, Depends, Response, Request

customer_router = APIRouter(prefix="/customers", tags=["customers resource"])


@customer_router.get("")
def get_customers(request: Request, response: Response, skip: typing.Optional[int] = None,
                  take: typing.Optional[int] = None, relations: bool = True, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*args, **kwargs):
        params = {"skip": skip, "take": take, "relations": relations}
        customers_adapter = adapters.CustomersAdapter()
        sellers_adapter = adapters.SellersAdapter()
        customers_adapter.params = params
        response.status_code, customers_json_response = customers_adapter.get_customers()
        if isinstance(customers_json_response, typing.List):
            for i, c in enumerate(customers_json_response):
                if seller_id := c.get("seller_id"):
                    try:
                        _, seller = sellers_adapter.get_seller(seller_id)
                        first_name = seller.get("first_name")
                        last_name = seller.get("last_name")
                        if isinstance(seller, dict) and (isinstance(last_name, str) or isinstance(first_name, str)):
                            customers_json_response[i]["seller_name"] = f"{first_name or ''} {last_name or ''}".strip()
                    except:
                        helpers.global_logger.error(traceback.format_exc())

        return customers_json_response

    return method(request=request, response=response)


@customer_router.get("/{customer_id}")
def get_customer(customer_id: typing.Union[str, int], request: Request, response: Response, relations: bool = True,
                 token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "SELLER", "TRANSPORTER", "MARKETING", "CLIENT"])
    def method(*args, **kwargs):
        params = {"relations": relations}
        customers_adapter = adapters.CustomersAdapter()
        sellers_adapter = adapters.SellersAdapter()
        customers_adapter.params = params
        response.status_code, customers_json_response = customers_adapter.get_customer(customer_id)
        if seller_id := customers_json_response.get("seller_id"):
            try:
                _, seller = sellers_adapter.get_seller(seller_id)
                first_name = seller.get("first_name")
                last_name = seller.get("last_name")
                if isinstance(seller, dict) and (isinstance(last_name, str) or isinstance(first_name, str)):
                    customers_json_response["seller_name"] = f"{first_name or ''} {last_name or ''}".strip()
            except:
                helpers.global_logger.error(traceback.format_exc())

        return customers_json_response

    return method(request=request, response=response)


@customer_router.post("")
def create_customer(new_customer_schema: schemas.CreateCustomerSchema, request: Request,
                    response: Response, token: str = Depends(common.token_schema)):
    @common.verify_role_middleware(["ADMIN", "MARKETING"])
    def method(*args, **kwargs):
        customers_adapter = adapters.CustomersAdapter()
        sellers_adapter = adapters.SellersAdapter()
        response.status_code, seller_json_response = sellers_adapter.get_seller(new_customer_schema.seller_id)
        if int(str(response.status_code)[0]) / 2 != 1:
            return seller_json_response
        response.status_code, customer_json_response = customers_adapter.create_customer(new_customer_schema)
        return customer_json_response

    return method(request=request, response=response)


__all__ = ["customer_router"]
