import config
import enums
import json
import schemas
from adapters.request_http import RequestsAdapter


class SellersAdapter(RequestsAdapter):
    def __init__(self):
        super(SellersAdapter, self).__init__(config.AppConfigValues.SELLERS_URL)

    def rollback_order(self):
        for comp in self.compensation_methods:
            self.__getattribute__(comp[0])(*comp[1::])

    def get_seller(self, seller_id):
        self.endpoint = f"sellers/{seller_id}"
        return 200, {"id": seller_id, "first_name": "Gerzon", "last_name": "Bautista"}


__all__ = ['SellersAdapter']
