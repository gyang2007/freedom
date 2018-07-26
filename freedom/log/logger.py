import logging.config

import yaml

# with open('freedom/log/logging.yml', 'r') as f_conf:
with open('/Users/gyang/develop/PycharmProjects/freedom/freedom/log/logging.yml', 'r') as f_conf:
    print("load log config[logging.yml]")
    dict_conf = yaml.load(f_conf)

logging.config.dictConfig(dict_conf)


def getlogger(name):
    return logging.getLogger(name)
