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




if __name__ == '__main__':
    api_key = '6b96bf9eb7324aa0a46d41286f17689a'
    api_secret = '0f76567dc36c4b87bc61b8751d0b729a'
    d = domain(api_key, api_secret)
    resolve_list = d.resolve_list('cqcy.ltd', 1, 100)
    print(resolve_list)