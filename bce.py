import copy
from urllib import request, parse
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

from baidubce.bce_base_client import BceBaseClient
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.auth import bce_v1_signer
from baidubce import utils


class bce3(BceBaseClient):
    __api_key = None
    __api_secret = None
    api_name = None
    host = None
    config = None

    def __init__(self, api_key, api_secret):
        self.__api_key = api_key.encode("utf-8")
        self.__api_secret = api_secret.encode("utf-8")
        self.api_name = self.__class__.__name__.replace('_', '/')
        self.api_name = self.api_name.encode("utf-8")
        self.host = b'bcd.baidubce.com'
        BceBaseClient.__init__(self, None)

    def set_host(self, host):
        self.host = host.encode("utf-8")

    def set_api_name(self, api_name):
        self.api_name = api_name.replace('_','/').encode("utf-8")

    def init_conf(self):
        if self.config is not None:
            return
        self.config = BceClientConfiguration(credentials=BceCredentials(self.__api_key, self.__api_secret), endpoint = self.host)


    def _merge_config(self, config):
        if config is None:
            return self.conf
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    @staticmethod
    def _handle_str(data):
        if type(data) == str:
            data = data.replace('_', '/')
            data = data.encode("utf-8")
        return data

    def _get_path(self, config, function_name=None, key=None):
        function_name = bce3._handle_str(function_name)
        key = bce3._handle_str(key)
        return utils.append_uri(b'/v1/', self.api_name, function_name, key)

    def _get_path_v2(self, config, function_name=None, key=None):
        function_name = bce3._handle_str(function_name)
        key = bce3._handle_str(key)
        return utils.append_uri(b'/v2/', self.api_name, function_name, key)

    def _send_request(
            self, http_method, function_name=None, key=None,
            body=None, headers=None, params=None,
            body_parser=None,
            api_version=1):

        self.init_conf()
        config = self._merge_config(self.config)
        path = {1: self._get_path,
                2: self._get_path_v2
                }[api_version](config, function_name, key)

        if body_parser is None:
            body_parser = handler.parse_json

        if headers is None:
            headers = {b'Accept': b'*/*', b'Content-Type': b'application/json;charset=utf-8'}

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [body_parser],
            http_method, path, body, headers, params)

