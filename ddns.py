import os
import socket
from domain import domain
from config import config


def get_ip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip

if __name__ == '__main__':
    api_key = config['api_key']
    api_secret = config['api_secret']
    domain_name = config['domain']
    sub_domain = config['sub_domain']

    d = domain(api_key, api_secret)
    resolve_list = d.resolve_list(domain_name, 1, 100)
    sub_domain_info = d.get_info_by_subdomain(resolve_list.result, sub_domain)
    ip = get_ip()
    ip = ip.decode('utf-8')
    if ip == sub_domain_info.rdata:
        os._exit(0)
    edit_info = d.resolve_edit(sub_domain_info.record_id, sub_domain, 'DEFAULT', 'A', 600, ip, domain_name)
    print(edit_info)