import configparser
import os

# 获取文件的当前路径（绝对路径）
cur_path = os.path.dirname(os.path.realpath(__file__))

# 获取config.ini的路径
config_path = os.path.join(cur_path, 'config.ini')

conf = configparser.ConfigParser()
conf.read(config_path)

db_datasource_host = conf.get("db", "datasource_host")
db_datasource_user = conf.get("db", "datasource_user")
db_datasource_passwd = conf.get("db", "datasource_passwd")
db_datasource_database = conf.get("db", "datasource_database")
db_datasource_port = conf.getint("db", "datasource_port")
db_datasource_mincached = conf.getint("db", "datasource_mincached")
db_datasource_maxcached = conf.getint("db", "datasource_maxcached")
db_datasource_maxconnections = conf.getint("db", "datasource_maxconnections")
