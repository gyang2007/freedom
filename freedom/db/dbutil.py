# -*- coding: UTF-8 -*-
import MySQLdb
from DBUtils.PooledDB import PooledDB

import freedom.config as g_config

_pool = PooledDB(MySQLdb, mincached=g_config.db_datasource_mincached, maxcached=g_config.db_datasource_maxcached,
                 maxconnections=g_config.db_datasource_maxconnections, setsession=["set names utf8mb4"],
                 host=g_config.db_datasource_host, user=g_config.db_datasource_user,
                 passwd=g_config.db_datasource_passwd, db=g_config.db_datasource_database,
                 port=g_config.db_datasource_port, charset='utf8mb4')


def get_connection():
    return _pool.connection()
