import datetime

import pandas as pd
import talib as ta

import freedom.common as my_common
import freedom.db.stock_base_dao as stock_base_dao
import freedom.db.stock_trade_daily_dao as stock_trade_daily_dao
import freedom.db.stock_trade_calendar_dao as stock_trade_calendar_dao
import freedom.log.logger as my_logger
import freedom.model.common_indicator as my_common_indicator

__logger = my_logger.getlogger("ma_scatter")


def sma_upward(code, date, timeperiod):
    """
    计算指定日期指定周期线是否开始拐头向上
    :param code:
    :param date:
    :param timeperiod:
    :return: True | False
    """
    count = timeperiod + 2
    stock_df = stock_trade_daily_dao.query_stock_trade_daily_limit_size(code, str(date), count)
    if len(stock_df) >= count:
        last_trade_date = stock_df[len(stock_df) - 1:]['trade_date'].values[0]
        if date.strftime('%Y-%m-%d') == str(last_trade_date):
            sma_list = ta.SMA(stock_df['close'], timeperiod)
            sma_1 = sma_list[len(sma_list) - 3]
            sma_2 = sma_list[len(sma_list) - 2]
            sma_3 = sma_list[len(sma_list) - 1]
            if sma_2 <= sma_1 and sma_3 > sma_2:
                return True

    return False


def sma_small_period_over_big_period(code, date, small_period, big_period):
    """
    计算小级别周期均线穿越大级别周期均线
    :param code:
    :param date:
    :param small_period: 小级别周期
    :param big_period: 大级别周期
    :return: True | False
    """
    if big_period < small_period:
        return False

    count = big_period + 1
    stock_df = stock_trade_daily_dao.query_stock_trade_daily_limit_size(code, str(date), count)
    if len(stock_df) >= count:
        last_trade_date = stock_df[len(stock_df) - 1:]['trade_date'].values[0]
        if date.strftime('%Y-%m-%d') == str(last_trade_date):
            sma_big_list = ta.SMA(stock_df['close'], big_period)
            sma_small_list = ta.SMA(stock_df['close'], small_period)

            sma_big_1 = sma_big_list[len(sma_big_list) - 2]
            sma_big_2 = sma_big_list[len(sma_big_list) - 1]

            sma_small_1 = sma_small_list[len(sma_small_list) - 2]
            sma_small_2 = sma_small_list[len(sma_small_list) - 1]

            # 小级别周期上穿大级别周期
            if sma_small_1 <= sma_big_1 and sma_small_2 > sma_big_2:
                # 大小级别均为升势
                if sma_big_2 >= sma_big_1 and sma_small_2 >= sma_small_1:
                    return True

    return False


def cal_increase(code, trade_date, time_period):
    count = time_period + 1
    stock_df = stock_trade_daily_dao.query_stock_trade_daily_after_date(code, str(trade_date), count)
    if len(stock_df) == count:
        first_trade_date = stock_df[0:1]['trade_date'].values[0]
        if trade_date.strftime('%Y-%m-%d') == str(first_trade_date):
            first_close = stock_df[0:1]['close'].values[0]
            last_close = stock_df[len(stock_df) - 1:]['close'].values[0]

            return (last_close - first_close) / first_close * 100.0

    return None


def __process_sma_upward(code, date):
    if sma_upward(code, date, 20) and sma_upward(code, date, 60):
        __logger.info('sma start upward, code = {}, date = {}'.format(code, str(date)))


def __process_sma_small_period_over_big_period(code, date):
    if sma_small_period_over_big_period(code, date, 30, 60):
        day5_increase = round(cal_increase(code, date, 5), 2)
        day10_increase = round(cal_increase(code, date, 10), 2)
        day20_increase = round(cal_increase(code, date, 20), 2)
        day30_increase = round(cal_increase(code, date, 30), 2)
        __logger.info(
            'sma small_period over big_period, code = {}, date = {}, day5 = {}, day10 = {}, day20 = {}, day30 = {}'.format(
                code, str(date), day5_increase, day10_increase, day20_increase, day30_increase))


if __name__ == '__main__':
    code = '002183'
    trade_date = datetime.datetime.strptime('2018-07-30', '%Y-%m-%d')
    while trade_date >= datetime.datetime.strptime('2010-01-01', '%Y-%m-%d'):
        # __process_sma_upward(code, trade_date)
        __process_sma_small_period_over_big_period(code, trade_date)

        while True:
            trade_date = trade_date - datetime.timedelta(days=1)
            if my_common.is_open_day(str(trade_date)):
                break

    print("done!!!")
    pass
