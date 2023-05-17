import helpers

from .default import AppConfigValues

import kombu


class KombuClient:

    def __init__(self):
        self.__host = AppConfigValues.RABBIT_HOST
        self.__port = AppConfigValues.RABBIT_PORT if isinstance(AppConfigValues.RABBIT_PORT, int) else \
            int(AppConfigValues.RABBIT_PORT)
        self.__user = AppConfigValues.RABBIT_USER
        self.__password = AppConfigValues.RABBIT_PASSWORD
        self.logger = helpers.global_logger.getChild('rabbitmq_client')
        self.connection = kombu.Connection(host_name=self.__host, userid=self.__user, password=self.__password,
                                           port=self.__port, virtual_host='/')
