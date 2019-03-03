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
    计算指定日期指定周期均线是否开始拐头向上
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
    计算小级别周期均线向上穿越大级别周期均线
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
                return True

                # 大小级别均为升势
                # if sma_big_2 >= sma_big_1 and sma_small_2 >= sma_small_1:
                #     return True

    return False


def sma_small_period_down_big_period(code, date, small_period, big_period):
    """
    计算小级别周期均线向下穿越大级别周期均线
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

            # 小级别周期向下穿越大级别周期
            if sma_small_1 >= sma_big_1 and sma_small_2 < sma_big_2:
                return True

    return False


def cal_increase(code, trade_date, time_period):
    """
    根据指定日期计算若干个交易日后价格变化
    :param code:
    :param trade_date:
    :param time_period:
    :return:
    """
    count = time_period + 1
    stock_df = stock_trade_daily_dao.query_stock_trade_daily_after_date(code, str(trade_date), count)
    if len(stock_df) == count:
        first_trade_date = stock_df[0:1]['trade_date'].values[0]
        if trade_date.strftime('%Y-%m-%d') == str(first_trade_date):
            first_close = stock_df[0:1]['close'].values[0]
            last_close = stock_df[len(stock_df) - 1:]['close'].values[0]

            return (last_close - first_close) / first_close * 100.0

    return None


def cal_increase_by_date_gap(code, start_trade_date, end_trade_date):
    """
    根据起止日期计算此周内价格变化
    :param code:
    :param start_trade_date:
    :param end_trade_date:
    :return:
    """
    stock_df = stock_trade_daily_dao.query_stock_trade_daily(code, start_trade_date, end_trade_date)
    if len(stock_df) >= 2:
        first_stock_close = stock_df[0:1]['close'].values[0]
        last_stock_close = stock_df[len(stock_df) - 1:]['close'].values[0]

        return (last_stock_close - first_stock_close) / first_stock_close * 100.0

    return None


def __process_sma_upward(code, date):
    # 拐点向上
    if sma_upward(code, date, 20) and sma_upward(code, date, 60):
        __logger.info('sma start upward, code = {}, date = {}'.format(code, str(date)))


def __process_sma_small_period_over_big_period(date):
    # 向上穿越
    stock_list = stock_base_dao.query_stock_base()
    for stock in stock_list:
        if stock['status'] == 1:
            if sma_small_period_over_big_period(stock['code'], date, 20, 60):
                __logger.info('sma small_period over big_period, code = {}, date = {}'.format(stock['code'], str(date)))


def __process_sma_small_period_over_big_period_2(code, date):
    # 向上穿越
    if sma_small_period_over_big_period(code, date, 20, 60):
        current_date = datetime.datetime.today()
        start_date = date + datetime.timedelta(days=1)

        while True:
            if start_date > current_date:
                __logger.info('start_date > current_date, break while cause!!!')
                break

            # 向下穿越或者当前是最新的交易日期
            if sma_small_period_down_big_period(code, start_date, 5, 10) or start_date.strftime(
                    '%Y-%m-%d') == current_date.strftime('%Y-%m-%d'):
                # 计算价格变化
                stock_increase = round(
                    cal_increase_by_date_gap(code, date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d')), 2)
                __logger.info(
                    'sma small_period over big_period, code = {}, over_date = {}, down_date = {}, increase = {}'
                        .format(code, date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'), stock_increase))
                break

            # 寻找下一个交易日期
            start_date = start_date + datetime.timedelta(days=1)
            while True:
                if my_common.is_open_day(str(start_date)):
                    break

                start_date = start_date + datetime.timedelta(days=1)


if __name__ == '__main__':
    trade_date = datetime.datetime.strptime('2018-08-02', '%Y-%m-%d')

    # code = '601318'
    # while trade_date >= datetime.datetime.strptime('2010-01-01', '%Y-%m-%d'):
    #     # __process_sma_upward(code, trade_date)
    #     __process_sma_small_period_over_big_period_2(code, trade_date)
    #
    #     while True:
    #         trade_date = trade_date - datetime.timedelta(days=1)
    #         if my_common.is_open_day(str(trade_date)):
    #             break

    __process_sma_small_period_over_big_period(trade_date)

    print("done!!!")
    pass
