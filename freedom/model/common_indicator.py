import talib as ta

import freedom.common as my_common
import freedom.db.stock_trade_daily_dao as stock_trade_daily_dao
import freedom.log.logger as my_logger

__logger = my_logger.getlogger('common_indicator')


def avg_volume_ratio(code, date, avg_day=5):
    """
    计算当日成交量是指定周期成交量均值的倍率
    :param code:
    :param date:
    :param avg_day:
    :return:
    """
    last_date = my_common.get_the_day_before_yesterday(date)
    df1 = stock_trade_daily_dao.query_stock_trade_daily_limit_size(code, str(last_date), avg_day)
    if len(df1) >= avg_day:
        sma = ta.SMA(df1['volume'][len(df1) - avg_day:], avg_day)
        v_avg = sma.values[len(sma) - 1]
        # 当日成交量
        df2 = stock_trade_daily_dao.query_stock_trade_daily(code, str(date), str(date))
        if not df2.empty:
            v_current = df2[0:1]['volume'].values[0]
            return v_current / v_avg
        else:
            __logger.warn("获取当前成交量信息为空, code = {}, date = {}".format(code, str(date)))
            return None
    else:
        return None


def cal_price_std(code, date, timeperiod=10):
    """
    计算指定周期内价格的标准差
    :param code:
    :param date:
    :param timeperiod:
    :return:
    """
    df = stock_trade_daily_dao.query_stock_trade_daily_limit_size(code, str(date), timeperiod)
    if len(df) < timeperiod:
        __logger.warn("样本数据数量不足, code = {}, date = {}, timeperiod = {}".format(code, str(date), timeperiod))

    return df['close'].std()
