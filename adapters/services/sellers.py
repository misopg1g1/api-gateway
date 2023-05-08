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

    def get_sellers(self):
        self.endpoint = f"sellers"
        return self._get()
    
    def create_seller(self, new_seller_schema: schemas.CreateSellerSchema):
        self.endpoint = 'sellers'
        self.json = new_seller_schema.dict()
        return self._post()

    def get_seller(self, seller_id):
        self.endpoint = f"sellers/{seller_id}"
        return self._get()

    def put_seller(self, seller_id):
        self.endpoint = f"sellers/{seller_id}"
        return self._put()

    def add_visit_to_seller(self, seller_id, visit_id):
        self.endpoint = f"sellers/{seller_id}/visits/{visit_id}"
        return self._get()

    def get_visit_to_seller(self, seller_id, visit_id):
        self.endpoint = f"sellers/{seller_id}/visit/{visit_id}"
        return self._get()
    
    def get_visits_to_seller(self, seller_id):
        self.endpoint = f"sellers/{seller_id}/visits"
        return self._get()    

    def get_visits(self):
        self.endpoint = f"visits"
        return self._get()  
    
    def create_visit(self, new_visit_schema: schemas.CreateVisitSchema):
        self.endpoint = 'visits'
        self.json = new_visit_schema.dict()
        return self._post()    

    def get_visit(self, visit_id):
        self.endpoint = f"visits/{visit_id}"
        return self._get()    

    def put_visit(self, visit_id):
        self.endpoint = f"visits/{visit_id}"
        return self._put()

__all__ = ['SellersAdapter']
