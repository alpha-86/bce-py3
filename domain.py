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

    def resolve_add(self, domain, view, rd_type, ttl, rdata, zone_name):
        data = {
            'domain': domain,
            'view': view,
            'rdType': rd_type,
            'ttl':ttl,
            'rdata':rdata,
            'zoneName':zone_name
        }
        return self._send_request(http_methods.POST, 'resolve_add', body=json.dumps(data))

    def resolve_delete(self, zone_name, record_id):
        data = {
            'zoneName': zone_name,
            'recordId': record_id
        }
        return self._send_request(http_methods.POST, 'resolve_delete', body=json.dumps(data))

    def resolve_edit(self, record_id, domain, view, rd_type, ttl, rdata, zone_name):
        data = {
            'recordId':record_id,
            'domain': domain,
            'view': view,
            'rdType': rd_type,
            'ttl': ttl,
            'rdata': rdata,
            'zoneName': zone_name
        }
        return self._send_request(http_methods.POST, 'resolve_edit', body=json.dumps(data))

    def get_info_by_subdomain(self, resolve_list, sub_domain):
        for i in resolve_list:
            if sub_domain == i.domain:
                return i
        return None
