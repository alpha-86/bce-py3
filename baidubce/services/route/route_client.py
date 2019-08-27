# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provides a client class for ROUTE.
"""

import copy
import json
import logging
import uuid

from baidubce import bce_base_client
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods

from baidubce.utils import required
from baidubce import compat

_logger = logging.getLogger(__name__)


class RouteClient(bce_base_client.BceBaseClient):
    """
        Route base sdk client
        """
    prefix = b'/v1'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json
        if headers is None:
            headers = {b'Accept': b'*/*', b'Content-Type': b'application/json;charset=utf-8'}
        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, RouteClient.prefix + path, body, headers, params)

    @required(route_table_id=(bytes, str),
              source_address=(bytes, str),
              destination_address=(bytes, str),
              next_hoop_type=(bytes, str),
              description=(bytes, str))
    def create_route(self, route_table_id, source_address, destination_address,
                     next_hop_type, description, next_hop_id=None, client_token=None,
                     config=None):
        """
        Create a route with the specified options.

        :param route_table_id:
            The id of the route table.
        :type route_table_id: string

        :param source_address:
            The source address of the route.
        :type source_address: string

        :param destination_address:
            The destination address of the route
        :type destination_address: string

        :param next_hop_type:
            route type
            the Bcc type is "custom";
            the VPN type is "vpn";
            the NAT type is "nat";
            the local gateway type is "defaultGateway"
        :type next_hop_type: string

        :param description:
            The option param to describe the route table.
        :type description: string

        :param next_hop_id:
            The next hop id
            when the nexthopType is "defaultGateway",this field can be empty
        :type next_hop_id: string

        :param client_token:
            If the clientToken is not specified by the user, a random String
            generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/route/rule'
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {
            'routeTableId': compat.convert_to_string(route_table_id),
            'sourceAddress': compat.convert_to_string(source_address),
            'destinationAddress': compat.convert_to_string(destination_address),
            'nexthopType': compat.convert_to_string(next_hop_type),
            'description': compat.convert_to_string(description)
        }

        if next_hop_id is not None:
            body['nexthopId'] = compat.convert_to_string(next_hop_id)

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params,
                                  config=config)

    @required(vpc_id=(bytes, str), route_table_id=(bytes, str))
    def get_route(self, vpc_id=None, route_table_id=None, config=None):
        """
        Get the detail information of route table for specific route table or/and vpc.

        :param vpc_id:
            the vpc id
            vpcId and routeTableId cannot be empty at the same time
        :type vpc_id: string

        :param route_table_id:
            the id of the route table
            vpcId and routeTableId cannot be empty at the same time
        :type route_table_id: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/route'
        params = {}
        if route_table_id is not None:
            params[b'routeTableId'] = route_table_id
        if vpc_id is not None:
            params[b'vpcId'] = vpc_id

        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(route_rule_id=(bytes, str))
    def delete_route(self, route_rule_id, client_token=None, config=None):
        """
        Delete the  specific route rule.

        :param route_rule_id:
            The id of the specified route table.
        :type route_rule_id: string

        :param client_token:
            If the clientToken is not specified by the user, a random String
            generated by default algorithm will be used.
        :type route_table_id: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/route/rule/%s' % compat.convert_to_bytes(route_rule_id)
        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token
        return self._send_request(http_methods.DELETE, path, params=params, config=config)


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.

    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid