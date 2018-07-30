import pandas as pd

import freedom.db.dbutil as db_util
import freedom.log.logger as my_logger

logger = my_logger.getlogger('stock_trade_daily_dao')


def query_stock_trade_daily(code, start_date, end_date):
    """
    根据code、起止日期（包含）查询数据，并按照交易日期升序排序
    :param code:
    :param start_date:
    :param end_date:
    :return: DafaFrame
        `code`, `open`, `high`, `low`, `close`, `volume`, `amount`, `turn_over_ratio`, `increase`, `amplitude`, `trade_date`
    """
    sql = 'select `code`, `open`, `high`, `low`, `close`, `volume`, `amount`, `turn_over_ratio`, `increase`, `amplitude`, `trade_date` from stock_trade_daily where `code` = "{code}" and `trade_date` BETWEEN "{start_date}" and "{end_date}" order by `trade_date`'.format(
        code=code, start_date=start_date, end_date=end_date)

    try:
        return pd.read_sql(sql, con=db_util.get_connection())
    except:
        logger.exception("query_stock_trade_daily error")

    return None


def query_stock_trade_daily_limit_size(code, end_date, size):
    """
    查询指定交易日期（包含）前指定数量的数据
    :param code:
    :param end_date:
    :param size:
    :return: DafaFrame
        `code`, `open`, `high`, `low`, `close`, `volume`, `amount`, `turn_over_ratio`, `increase`, `amplitude`, `trade_date`
    """
    sql = """
        SELECT
            `code`, `open`, `high`, `low`, `close`, `volume`, `amount`, `turn_over_ratio`, `increase`, `amplitude`, `trade_date`
        FROM
            (
                SELECT
                    `code`, `open`, `high`, `low`, `close`, `volume`, `amount`, `turn_over_ratio`, `increase`, `amplitude`, `trade_date`
                FROM
                    stock_trade_daily
                WHERE
                    CODE = '{}'
                AND trade_date <= '{}'
                ORDER BY
                    trade_date DESC
                LIMIT {}
            ) t1
        ORDER BY
            trade_date    
    """.format(code, end_date, size)
    try:
        return pd.read_sql(sql, con=db_util.get_connection())
    except:
        logger.exception("query_stock_trade_daily_limit_size error")

    return None


def insert_stock_trade_daily_batch(datas):
    """
    批量保存数据库交易信息
    :param
        datas: 交易信息二维数组
        数据信息按照以下字段顺序排列：`code`, `open`, `high`, `low`, `close`, `volume`, `amount`, `turn_over_ratio`, `increase`, `amplitude`, `trade_date`
    :return:
    """
    sql = """insert into stock_trade_daily(`code`, `open`, `high`, `low`, `close`, `volume`, `amount`, `turn_over_ratio`, `increase`, `amplitude`, `trade_date`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    conn = db_util.get_connection()
    try:
        cur = conn.cursor()
        cur.executemany(sql, datas)
        conn.commit()
        cur.close()
    except:
        conn.rollback()
        logger.exception("Insert stock_trade_daily_batch error")


def delete_stock_trade_daily_by_trade_date(start_date, end_date):
    """
    根据起止日期删除交易数据
    :param start_date:
    :param end_date:
    :return:
    """
    sql = 'delete from stock_trade_daily where trade_date BETWEEN "{}" and "{}"'.format(start_date, end_date)
    conn = db_util.get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except:
        conn.rollback()
        logger.exception("Delete stock_trade_daily error")


def query_stock_max_trade_date():
    """
    获取每一个stock数据最新的交易日期
    :return: DafaFrame
        code, max_trade_date
    """
    # 获取每一个stock数据最新的交易日期
    sql = """
        SELECT
            t1.code ,
            t2.max_trade_date
        FROM
            stock_base t1
        LEFT JOIN(
            SELECT
                CODE ,
                max(trade_date) AS max_trade_date
            FROM
                stock_trade_daily
            GROUP BY
                CODE
        ) t2 ON t1. CODE = t2. CODE
        WHERE
            t1. STATUS = 1
        AND t1.type = 1;    
    """
    try:
        return pd.read_sql(sql, con=db_util.get_connection())
    except:
        logger.exception("query_stock_max_trade_date error")

    return None
