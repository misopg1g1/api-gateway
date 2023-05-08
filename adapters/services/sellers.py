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

    def get_sellers(self, headers):
        self.endpoint = f"sellers"
        return self._get(headers=headers)

    def create_seller(self, new_seller_schema: schemas.CreateSellerSchema, headers):
        self.endpoint = 'sellers'

        self.json = new_seller_schema.dict()
        return self._post(headers=headers)

    def get_seller(self, seller_id, headers):
        self.endpoint = f"sellers/{seller_id}"
        return self._get(headers=headers)

    def put_seller(self, seller_id, update_seller_schema, headers):
        self.endpoint = f"sellers/{seller_id}"
        self.json = update_seller_schema
        return self._put(headers=headers)

    def add_visit_to_seller(self, seller_id, visit_id, headers):
        self.endpoint = f"sellers/{seller_id}/visits/{visit_id}"
        return self._get(headers=headers)

    def get_visit_to_seller(self, seller_id, visit_id, headers):
        self.endpoint = f"sellers/{seller_id}/visit/{visit_id}"
        return self._get(headers=headers)

    def get_visits_to_seller(self, seller_id, headers):
        self.endpoint = f"sellers/{seller_id}/visits"
        return self._get(headers=headers)

    def get_visits(self, headers):
        self.endpoint = f"visits"
        return self._get(headers=headers)

    def create_visit(self, new_visit_schema: schemas.CreateVisitSchema, headers):
        self.endpoint = 'visits'
        self.json = new_visit_schema.dict()
        return self._post(headers=headers)

    def get_visit(self, visit_id, headers):
        self.endpoint = f"visits/{visit_id}"
        return self._get(headers=headers)

    def put_visit(self, visit_id, update_visit_schema, headers):
        self.endpoint = f"visits/{visit_id}"
        self.json = update_visit_schema
        return self._put(headers=headers)

    def delete_user(self, user_id, headers):
        self.base_url = config.AppConfigValues.AUTH_URL
        self.endpoint = f"session/delete/{user_id}"
        resp = self._delete(headers=headers)
        self.base_url = config.AppConfigValues.SELLERS_URL
        return resp


__all__ = ['SellersAdapter']
