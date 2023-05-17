import config

import kombu
import pydantic
import json

from typing import Any, Union, Dict


class NewOrderEmailProducer(config.KombuProducer):

    def publish_user_to_verify(self, data: Union[pydantic.BaseModel, Dict[Union[str, int], Any]]):

        if isinstance(data, pydantic.BaseModel):
            dump_data = data.json(by_alias=False, exclude={"password", "previous_states"})
        elif isinstance(data, Dict):
            dump_data = json.dumps(data)
        else:
            dump_data = data
        self._publish(dump_data)


new_order_email_publisher = NewOrderEmailProducer(['new_order_email'], 'new_order_email',
                                                  kombu.Exchange(''),
                                                  config.kombu_client.connection)

__all__ = ['new_order_email_publisher']
