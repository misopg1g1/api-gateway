import config
import enums
import json
import schemas
from adapters.request_http import RequestsAdapter


class CustomersAdapter(RequestsAdapter):
    def __init__(self):
        super(CustomersAdapter, self).__init__(config.AppConfigValues.CUSTOMERS_URL)

    def rollback_order(self):
        for comp in self.compensation_methods:
            self.__getattribute__(comp[0])(*comp[1::])

    def get_customers(self):
        self.endpoint = "customers"
        return self._get()

    def get_customer(self, customer_id):
        self.endpoint = f"customers/{customer_id}"
        return self._get()

    def create_customer(self, create_customer_schema: schemas.CreateCustomerSchema):
        self.endpoint = f"customers"
        self.json = json.loads(create_customer_schema.json())
        return self._post()


__all__ = ['CustomersAdapter']
