from domain import domain
from config import config

if __name__ == '__main__':
    api_key = config['api_key']
    api_secret = config['api_secret']
    domain_name = config['domain']
    d = domain(api_key, api_secret)
    resolve_list = d.resolve_list(domain_name, 1, 100)
    for i in resolve_list.result:
        #print(i)
        print(i.record_id, i.domain, i.rdtype, i.rdata)

    #add1 = d.resolve_add('t1', 'DEFAULT', 'CNAME', 600, 'www.baidu.com', domain_name)
    #print(add1)

    #edit1 = d.resolve_edit('13801407', 't1', 'DEFAULT', 'CNAME', 600, 'www2.baidu.com', domain_name)
    #print(edit1)