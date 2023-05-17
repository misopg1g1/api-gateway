import kombu

from typing import List, Any


class KombuProducer:
    def __init__(self, queue_names: List[str], routing_key: str, exchange: kombu.Exchange,
                 connection: kombu.Connection):
        self.exchange = exchange
        self.routing_key = routing_key
        self.producer = connection.Producer(exchange=exchange, routing_key=routing_key)
        self.queues = list(map(lambda q: kombu.Queue(q, exchange=exchange, routing_key=routing_key), queue_names))

    def _publish(self, data: Any):
        for q in self.queues:
            self.producer.publish(data, routing_key=self.routing_key, retry=True, exchange=self.exchange,
                                  declare=[q])
