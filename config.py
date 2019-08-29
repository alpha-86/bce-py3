import yaml
import os
conf_file = 'config.yaml'
conf_file_product = 'config_product.yaml'
if os.path.exists(conf_file_product):
    conf_file = conf_file_product
f = open(conf_file)
config = yaml.load(f)
