import config
import enums
import schemas
from adapters.request_http import RequestsAdapter


class InventoryAdapter(RequestsAdapter):
    def __init__(self):
        super(InventoryAdapter, self).__init__(config.AppConfigValues.INVENTORY_URL)

    def create_inventory(self, new_inventory_schema: schemas.CreateInventorySchema, headers):
        self.endpoint = '/inventories'
        self.json = new_inventory_schema.dict()
        return self._post(headers=headers)

    def get_inventory(self, productId: str, headers):
        self.endpoint = '/products/:productId/inventoy'
        self.params = {"productId": productId}
        return self._get(headers=headers)

    def get_inventories(self, headers):
        self.endpoint = '/inventories'
        return self._get(headers=headers)

    def put_inventory(self, update_inventory_schema: schemas.UpdateInventorySchema, productId: str, headers):
        self.endpoint = '/products/:productId/inventoy'
        self.params = {"productId": productId}
        self.json = update_inventory_schema.dict()
        return self._put(headers=headers)

__all__ = ['InventoryAdapter']