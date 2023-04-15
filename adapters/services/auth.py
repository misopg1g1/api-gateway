import config
import schemas
from adapters.request_http import RequestsAdapter


class AuthAdapter(RequestsAdapter):
    def __init__(self):
        super(AuthAdapter, self).__init__(config.AppConfigValues.AUTH_URL)

    def rollback_order(self):
        for comp in self.compensation_methods:
            globals()[f"{comp[0]}"](*comp[1::])

    def login(self, user_schema: schemas.LoginUserSchema):
        self.endpoint = 'session/login'
        self.json = user_schema.dict()
        return self._post()


__all__ = ['AuthAdapter']
