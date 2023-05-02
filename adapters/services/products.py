import config
import enums
import json
import schemas
from adapters.request_http import RequestsAdapter


class ProductsAdapter(RequestsAdapter):
    def __init__(self):
        super(ProductsAdapter, self).__init__(config.AppConfigValues.PRODUCTS_URL)

    def rollback_order(self):
        for comp in self.compensation_methods:
            self.__getattribute__(comp[0])(*comp[1::])

    def get_products(self):
        self.endpoint = "products"
        return self._get()

    def get_product(self, product_id):
        self.endpoint = f"products/{product_id}"
        return self._get()

    def create_product(self, create_product_schema: schemas.CreateProductSchema):
        self.endpoint = f"products"
        self.json = json.loads(create_product_schema.json())
        return self._post()

    def get_categories(self):
        self.endpoint = f"categories"
        return self._get()

    def create_category(self, create_category_schema: schemas.CreateCategorySchema):
        self.endpoint = f"categories"
        self.json = json.loads(create_category_schema.json())
        return self._post()

    def patch_category(self, category_id: str, create_category_schema: schemas.PatchCategorySchema):
        self.endpoint = f"categories/{category_id}"
        self.json = json.loads(create_category_schema.json())
        return self._patch()

__all__ = ['ProductsAdapter']
