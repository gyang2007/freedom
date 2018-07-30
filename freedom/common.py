import datetime

import talib as ta
import tushare as ts

import freedom.db.stock_trade_daily_dao as stock_trade_daily_dao
import freedom.db.stock_trade_calendar_dao as stock_trade_calendar_dao
import freedom.log.logger as my_logger

__logger = my_logger.getlogger('common')


def is_open_day(date):
    """
    查看指定日期是否是交易日
    :param date: 字符串日期，格式%Y-%m-%d
    :return: True | False
    """
    result = stock_trade_calendar_dao.select_one(date)
    if result and result['is_open'] == 1:
        return True

    return False


def get_the_day_before_yesterday(date):
    """
    获取指定日期前一天的日期
    :param date
    :return: date
    """
    return date - datetime.timedelta(days=1)


def get_yesterday_trading_date_before(date):
    """
    获取指定日期上一个交易日
    :param date:
    :return:
    """
    if isinstance(date, str):
        d = datetime.datetime.strptime(date, '%Y-%m-%d')

    if isinstance(date, datetime.date):
        d = date

    if isinstance(date, datetime.datetime):
        d = date

    l_d = get_the_day_before_yesterday(d)
    while True:
        result = stock_trade_calendar_dao.select_one(l_d.strftime('%Y-%m-%d'))
        if result['is_open'] == 1:
            return l_d
        else:
            l_d = get_the_day_before_yesterday(l_d)


def get_yesterday_trading_date():
    """
    获取最近上一个交易日期（非当天交易日）
    如果当前时间大于当天开盘时间，则为上一个交易日
    如果当前时间小于当天开盘时间，则为上上一个交易日
    :return: date
    """
    # 当前时间
    now = datetime.datetime.now()
    # 当天开盘时间
    open_time = datetime.datetime.strptime('{}-{}-{} {}:{}:{}'.format(now.year, now.month, now.day, '09', '30', '00'),
                                           '%Y-%m-%d %H:%M:%S')
    # 当前时间大于开盘时间
    if now > open_time:
        current_date = datetime.date.today()
    else:
        current_date = get_the_day_before_yesterday(datetime.date.today())

    return get_yesterday_trading_date_before(current_date)

    # yesterday_date = get_the_day_before_yesterday(current_date)
    # while True:
    #     if not ts.is_holiday(str(yesterday_date)):
    #         return yesterday_date
    #     else:
    #         yesterday_date = get_the_day_before_yesterday(yesterday_date)


def get_yesterday_trading_date2():
    """
    获取最近上一个交易日期（非当天交易日）
    如果当前时间大于当天开盘时间，则为上一个交易日
    如果当前时间小于当天开盘时间，则为上上一个交易日
    :return: date
    """
    current_date = None
    # 当前时间
    now = datetime.datetime.now()
    # 当天开盘时间
    open_time = datetime.datetime.strptime('{}-{}-{} {}:{}:{}'.format(now.year, now.month, now.day, '09', '30', '00'),
                                           '%Y-%m-%d %H:%M:%S')
    # 当前时间大于开盘时间
    if now > open_time:
        current_date = datetime.date.today()
    else:
        current_date = get_the_day_before_yesterday(datetime.date.today())

    yesterday_date = get_the_day_before_yesterday(current_date)
    while True:
        datas = ts.get_k_data('000001', start=str(yesterday_date), end=str(yesterday_date), index=True)
        if datas.empty:
            yesterday_date = get_the_day_before_yesterday(yesterday_date)
        else:
            return yesterday_date


def convert_standard_code(code):
    """
    将指标代码转为标准6为字符串
    :param code:
    :return:
    """
    if isinstance(code, int):
        if len(str(code)) == 6:
            return str(code)

        if len(str(code)) < 6:
            return str(1000000 + code)[1:]

    if isinstance(code, str):
        tmp = '000000' + code
        return str(tmp)[len(tmp) - 6:]

    return None


def level_position(df, indicator='close'):
    """
     计算最新的指标价格所在一定周期内价格的位置
    :param df: DataFrame
    :param indicator: 价格指标
    :return: position
    """
    nearest_df = df[len(df) - 1:]
    value = nearest_df[indicator].values[0]
    max = df[indicator].max()
    min = df[indicator].min()
    position = (value - min) / (max - min) * 100.0
    __logger.info(
        'Cal price level position, min = {}, max = {}, price = {}, position = {}'.format(min, max, value, position))
    return position


def avg_volume(df, avg_day=5):
    """
    获取成交量指定周期的均值
    :param df:
    :param avg_day:
    :return: 成交量均值
    """
    if len(df) >= avg_day:
        sma = ta.SMA(df['volume'][len(df) - avg_day:], avg_day)
        return sma.values[len(sma) - 1]
    else:
        raise Exception("计算均值数据的长度不足！！！")


def is_jump_to_daily_limit(code, date):
    """
    是否是涨停一字板
    :param code: 代码
    :param date: 日期
    :return: True | False
    """
    stock_trade_df = stock_trade_daily_dao.query_stock_trade_daily(code, str(date),
                                                                   str(date))
    if not stock_trade_df.empty:
        increase = stock_trade_df['increase'].values[0]
        amplitude = stock_trade_df['amplitude'].values[0]
        if increase > 9.5 and amplitude == 0.0:
            return True

    return False


def is_close_over_open_price(code, trade_date):
    """
    查询指定交易日收盘价是否大于或等于开盘价
    :param code:
    :param trade_date:
    :return: True | False
    """
    if is_open_day(str(trade_date)):
        stock_df = stock_trade_daily_dao.query_stock_trade_daily(code, str(trade_date), str(trade_date))
        if not stock_df.empty:
            open = stock_df['open'].values[0]
            close = stock_df['close'].values[0]

            return close - open >= 0

    return False


if __name__ == '__main__':
    print(get_yesterday_trading_date_before('2018-07-25'))
    print(get_yesterday_trading_date2())
    print(get_yesterday_trading_date())
    # print(ts.get_k_data('002061', '2018-07-23', '2018-07-24'))
    # ts.get_today_all().to_csv("/Users/gyang/develop/PycharmProjects/freedom/export/today_all.csv")
    pass
