import pandas as pd

import freedom.db.dbutil as db_util
import freedom.log.logger as my_logger

__logger = my_logger.getlogger('stock_base_dao')


def update_stock_status(code, status):
    """
    修改stock交易状态
    :param code:
    :param status: 1: 正常; 2: 停牌
    :return:
    """
    sql = 'update stock_base set status = {} where code = "{}" and type = 1'.format(status, code)

    conn = db_util.get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except:
        conn.rollback()
        __logger.exception("Update stock_status error")


def query_stock_base():
    """
    获取stock基本信息数据
    :return:
    """
    result_list = []
    sql = 'select code, type, `name`, status, time_to_market from stock_base'
    try:
        cur = db_util.get_connection().cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()

        for r in res:
            result_list.append({'code': r[0], 'type': r[1], 'name': r[2], 'status': r[3], 'time_to_market': r[4]})
    except:
        __logger.exception("Query stock_base error")

    return result_list


def query_stock_base_by_code(code):
    """
    获取stock基本信息数据
    :return:
    """
    result = None
    sql = 'select code, type, `name`, status, time_to_market from stock_base where code = "{}"'.format(code)
    try:
        cur = db_util.get_connection().cursor()
        cur.execute(sql)
        res = cur.fetchone()
        cur.close()

        if res:
            result = {'code': res[0], 'type': res[1], 'name': res[2], 'status': res[3], 'time_to_market': res[4]}
    except:
        __logger.exception("Query stock_base error")

    return result


def query_stock_base_to_map():
    """
    查询所有Stock信息，并已code为索引
    :return: Series
    """
    result_series = pd.Series()
    sql = 'select code, type, `name`, status, time_to_market from stock_base where type = 1'
    try:
        cur = db_util.get_connection().cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()

        for r in res:
            result_series = result_series.append(pd.Series(
                {r[0]: {'code': r[0], 'type': r[1], 'name': r[2], 'status': r[3], 'time_to_market': r[4]}}))
    except:
        __logger.exception("Query query_stock_base_to_map error")

    return result_series
