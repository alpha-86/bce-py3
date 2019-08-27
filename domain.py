import json

from bce import bce3
from baidubce.http import http_methods


class domain(bce3):
    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)

    def resolve_list(self, domain, page_no, page_size):
        data = {
            'domain':domain,
            'pageNo':page_no,
            'pageSize':page_size
        }
        return self._send_request(http_methods.POST, 'resolve_list', body=json.dumps(data))

    def add(self, domain, view, rd_type, ttl, rdata, zone_name):
        pass

    def delete(self, zone_name, record_id):
        pass

    def edit(self, record_id, domain, view, rd_type, ttl, rdata, zone_name):
        pass

