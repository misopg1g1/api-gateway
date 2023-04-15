import common.error_handling

import requests
import typing
import abc

from requests import ConnectTimeout, ReadTimeout, Timeout, JSONDecodeError, ConnectionError
from urllib3.exceptions import ReadTimeoutError


class RequestsAdapter:
    base_url: str
    endpoint: typing.Optional[str]
    params: typing.Any
    data: typing.Any
    json: typing.Any
    compensation_methods: typing.List[typing.Tuple[str, typing.Any]]

    def __init__(self, base_url: str, endpoint: typing.Optional[str] = None, params=None, data=None, json=None,
                 compensation_methods=None):
        self.base_url = base_url
        self.endpoint = endpoint
        self.params = params
        self.data = data
        self.json = json
        self.compensation_methods = compensation_methods or []

    @abc.abstractmethod
    def rollback_order(self):
        pass

    def raise_non_exception_errors(self, response_data, response: requests.Response):
        if int(str(response.status_code)[0]) / 2 != 1 and int(str(response.status_code)[0]) % 5 != 0:

            if type(response_data) != str:
                response_data: typing.Optional[typing.Dict[str, typing.Any]]
                if self.compensation_methods:
                    self.rollback_order()
                raise common.error_handling.AnyCode(
                    f"{self.endpoint} | {response_data.get('error', common.ResponseMessagesValues.GENERAL_REQUESTS_FAILURE_MESSAGE)}",
                    response.status_code)
            else:
                if self.compensation_methods:
                    self.rollback_order()
                raise common.error_handling.AnyCode(f"{self.endpoint} | {response_data}", response.status_code)
        elif int(str(response.status_code)[0]) == 0:
            if self.compensation_methods:
                self.rollback_order()
            raise common.error_handling.AppErrorBaseClass(
                common.ResponseMessagesValues.GENERAL_REQUESTS_FAILURE_MESSAGE)

    @staticmethod
    def extract_response_data(response: requests.Response):
        try:
            response_data = response.json()
        except JSONDecodeError:
            response_data = response.text
        return response_data

    def _get(self, **kwargs):
        url = self.base_url
        if self.endpoint:
            url = f"{self.base_url}/{self.endpoint}"
        try:
            response = requests.get(url, self.params, **kwargs)
            response_data = self.extract_response_data(response)
            self.raise_non_exception_errors(response_data, response)
            return response.status_code, response_data
        except (ConnectTimeout, ConnectionError, ReadTimeoutError, ReadTimeout, Timeout):
            raise common.error_handling.AppErrorBaseClass(
                common.ResponseMessagesValues.GENERAL_REQUESTS_FAILURE_MESSAGE)

    def _post(self, **kwargs):
        url = self.base_url
        if self.endpoint:
            url = f"{self.base_url}/{self.endpoint}"
        try:
            response = requests.post(url, self.data, self.json, **kwargs)
            response_data = self.extract_response_data(response)
            self.raise_non_exception_errors(response_data, response)
            return response.status_code, response_data
        except (ConnectTimeout, ConnectionError, ReadTimeoutError, ReadTimeout, Timeout):
            raise common.error_handling.AppErrorBaseClass(
                common.ResponseMessagesValues.GENERAL_REQUESTS_FAILURE_MESSAGE)

    def _put(self, **kwargs):
        url = self.base_url
        if self.endpoint:
            url = f"{self.base_url}/{self.endpoint}"
        try:
            response = requests.put(url, self.data, **kwargs)
            response_data = self.extract_response_data(response)
            self.raise_non_exception_errors(response_data, response)
            return response.status_code, response_data
        except (ConnectTimeout, ConnectionError, ReadTimeoutError, ReadTimeout, Timeout):
            raise common.error_handling.AppErrorBaseClass(
                common.ResponseMessagesValues.GENERAL_REQUESTS_FAILURE_MESSAGE)

    def _patch(self, **kwargs):
        url = self.base_url
        if self.endpoint:
            url = f"{self.base_url}/{self.endpoint}"
        try:
            response = requests.patch(url, self.data, **kwargs)
            response_data = self.extract_response_data(response)
            self.raise_non_exception_errors(response_data, response)
            return response.status_code, response_data
        except (ConnectTimeout, ConnectionError, ReadTimeoutError, ReadTimeout, Timeout):
            raise common.error_handling.AppErrorBaseClass(
                common.ResponseMessagesValues.GENERAL_REQUESTS_FAILURE_MESSAGE)

    def _delete(self, **kwargs):
        url = self.base_url
        if self.endpoint:
            url = f"{self.base_url}/{self.endpoint}"
        try:
            response = requests.delete(url, **kwargs)
            response_data = self.extract_response_data(response)
            self.raise_non_exception_errors(response_data, response)
            return response.status_code, response_data
        except (ConnectTimeout, ConnectionError, ReadTimeoutError, ReadTimeout, Timeout):
            raise common.error_handling.AppErrorBaseClass(
                common.ResponseMessagesValues.GENERAL_REQUESTS_FAILURE_MESSAGE)
