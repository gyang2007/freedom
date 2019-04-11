import logging.config

import yaml

import freedom.config as g_config

with open(g_config.log_config, 'r') as f_conf:
    dict_conf = yaml.load(f_conf)

logging.config.dictConfig(dict_conf)


def getlogger(name):
    return logging.getLogger(name)
