import json

import config
import enums
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

    def create_user(self, new_user_schema: schemas.CreateUserSchema, headers):
        self.endpoint = 'session/create_user'
        self.json = new_user_schema.dict()
        return self._post(headers=headers)

    def refresh_token(self, headers):
        self.endpoint = 'session/refresh_token'
        return self._get(headers=headers)

    def verify_token(self, headers):
        self.endpoint = 'session/verify_token'
        return self._get(headers=headers)

    def verify_roles(self, roles_schema: schemas.RolesSchema, headers):
        self.endpoint = 'session/verify_roles'
        self.json = json.loads(roles_schema.json())
        return self._post(headers=headers)


__all__ = ['AuthAdapter']
