import config
import enums
import schemas
from adapters.request_http import RequestsAdapter


class ProductsAdapter(RequestsAdapter):
    def __init__(self):
        super(ProductsAdapter, self).__init__(config.AppConfigValues.PRODUCTS_URL)

    def rollback_order(self):
        for comp in self.compensation_methods:
            globals()[f"{comp[0]}"](*comp[1::])

    def get_products(self):
        self.endpoint = "products"
        return self._get()

    def get_product(self, product_id):
        self.endpoint = f"products/{product_id}"
        return self._get()


__all__ = ['ProductsAdapter']
