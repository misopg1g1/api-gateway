import config
import enums
import schemas
from adapters.request_http import RequestsAdapter


class InventoryAdapter(RequestsAdapter):
    def __init__(self):
        super(InventoryAdapter, self).__init__(config.AppConfigValues.INVENTORY_URL)

    def rollback_order(self):
        for comp in self.compensation_methods:
            self.__getattribute__(comp[0])(*comp[1::])

    def create_inventory(self, new_inventory_schema: schemas.CreateInventorySchema):
        self.endpoint = 'inventories'
        self.json = new_inventory_schema.dict()
        return self._post()

    def get_inventory(self, product_id):
        self.endpoint = f"products/{product_id}/inventory"
        return self._get()

    def get_inventories(self):
        self.endpoint = 'inventories'
        return self._get()

    def put_inventory(self, update_inventory_schema: schemas.UpdateInventorySchema, product_id):
        self.endpoint = f"products/{product_id}/inventory"
        self.json = update_inventory_schema.dict()
        return self._put()

    def delete_product(self, product_id: str):
        self.base_url = config.AppConfigValues.PRODUCTS_URL
        self.endpoint = f"products/{product_id}"
        resp = self._delete()
        self.base_url = config.AppConfigValues.INVENTORY_URL
        return resp


__all__ = ['InventoryAdapter']
