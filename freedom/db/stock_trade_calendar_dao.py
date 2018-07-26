import freedom.db.dbutil as db_util
import freedom.log.logger as my_logger

__logger = my_logger.getlogger('stock_trade_calendar_dao')


def select_one(date):
    """
    根据日期查询是否是交易日信息
    :param date:
    :return:
    """
    result = {}
    sql = 'select `date`, is_open from stock_trade_calendar where `date` = "{}"'.format(date)
    conn = db_util.get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchone()
        cur.close()

        if len(res) > 0:
            result['date'] = str(res[0])
            result['is_open'] = res[1]
    except:
        __logger.exception("Query stock_trade_calendar error")

    return result
