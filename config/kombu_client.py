import helpers

from .default import AppConfigValues

import kombu


class KombuClient:

    def __init__(self, host, port, user, password):
        self.__host = host
        self.__port = port if isinstance(port, int) else int(port)
        self.__user = user
        self.__password = password
        self.logger = helpers.global_logger.getChild('rabbitmq_client')
        self.connection = kombu.Connection(host_name=self.__host, userid=self.__user, password=self.__password,
                                           port=self.__port, virtual_host='/')


kombu_client = KombuClient(AppConfigValues.RABBIT_HOST, AppConfigValues.RABBIT_PORT, AppConfigValues.RABBIT_USER,
                           AppConfigValues.RABBIT_PASSWORD)
