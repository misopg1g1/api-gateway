import config
import schemas
from adapters.request_http import RequestsAdapter


class ProductAdapter(RequestsAdapter):
    def __init__(self):
        super(ProductAdapter, self).__init__(config.AppConfigValues.AUTH_URL)

    def rollback_order(self):
        for comp in self.compensation_methods:
            globals()[f"{comp[0]}"](*comp[1::])

    def get(self, headers, productId: str):
        self.endpoint = 'products' + '/' + productId
        return self._get(headers=headers)
    
    def getAll(self, headers, productId: str):
        self.endpoint = 'products'
        return self._get(headers=headers)




__all__ = ['ProductAdapter']