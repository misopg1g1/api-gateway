import json

import config
import schemas
from adapters.request_http import RequestsAdapter


class OrdersAdapter(RequestsAdapter):
    def __init__(self):
        super(OrdersAdapter, self).__init__(config.AppConfigValues.ORDER_URL)

    def rollback_order(self):
        for comp in self.compensation_methods:
            self.__getattribute__(comp[0])(*comp[1::])

    def create_order(self, new_order_schema: schemas.CreateOrderSchema, headers):
        self.endpoint = "orders"
        self.json = json.loads(new_order_schema.json())
        return self._post(headers=headers)

    def get_orders(self, headers):
        self.endpoint = "orders"
        formatted_header = dict(
            filter(lambda kv: kv[0] not in ["content-type", "origin", "content-length"], headers.items()))
        return self._get(headers=formatted_header)

    def get_order(self, order_id: str, headers):
        formatted_header = dict(
            filter(lambda kv: kv[0] not in ["content-type", "origin", "content-length"], headers.items()))
        self.endpoint = f"orders/{order_id}"
        return self._get(headers=formatted_header)


__all__ = ['OrdersAdapter']
