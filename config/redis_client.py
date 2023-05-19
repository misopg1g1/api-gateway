import helpers
import config

import redis
import pydantic
import hashlib
import json

from typing import Dict, Any, Union


class RedisClient:

    def __init__(self):
        self.host = config.AppConfigValues.REDIS_HOST
        self.port = config.AppConfigValues.REDIS_PORT
        self.password = config.AppConfigValues.REDIS_PASSWORD
        self.logger = helpers.global_logger.getChild('redis_client')
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password)

    def set_data(self, data: Union[pydantic.BaseModel, Dict[Union[str, int], Any], str], key=None):
        if isinstance(data, pydantic.BaseModel):
            dump_data = json.loads(data.json(by_alias=False, exclude={"password", "previous_states"}))
            dump_data = json.dumps(dump_data, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
        elif isinstance(data, Dict):
            dump_data = json.dumps(data, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
        elif isinstance(data, set):
            dump_data = json.dumps(tuple(data))
        else:
            dump_data = json.dumps(data)
        final_key = hashlib.md5(dump_data.encode('utf-8')).hexdigest() if not key else key
        self.client.set(final_key, dump_data, 600)
        return final_key

    def get_data(self, key: str):
        if data := self.client.get(key):
            try:
                return json.loads(data)
            except:
                return data


create_redis_client = lambda: RedisClient()

__all__ = ['create_redis_client']
