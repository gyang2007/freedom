import datetime

import tushare as ts
import pandas as pd

import freedom.common as my_common
import freedom.db.stock_base_dao as stock_base_dao
import freedom.db.stock_trade_daily_dao as stock_trade_daily_dao
import freedom.log.logger as my_logger

__logger = my_logger.getlogger('gather_data')


def check_stock_status(trade_date):
    """
    利用当日成交数据校验系统中的数据停牌、交易状态是否正确
    :return:
    """
    if my_common.is_open_day(str(trade_date)):
        day_all_df = ts.get_day_all(str(trade_date))
        if not day_all_df.empty:
            stock_series = stock_base_dao.query_stock_base_to_map()
            for index, row in day_all_df.iterrows():
                code = my_common.convert_standard_code(row['code'])
                stock_local = stock_series.get(code)
                # 本系统中无此stock数据
                if not stock_local:
                    __logger.warn(
                        "Stock is not exists in local system, code = {}".format(code))
                    continue

                open = row['open']
                high = row['high']
                low = row['low']
                volume = row['volume']
                # 停牌
                if open == 0.0 and high == 0.0 and low == 0.0 and volume == 0.0:
                    # 本系统是否为停牌状态
                    if stock_local and stock_local['status'] == 1:
                        __logger.warn(
                            "Stock is already suspension, but no suspension in local system, code = {}".format(code))
                        continue
                else:
                    if stock_local and (not stock_local['status'] == 1):
                        __logger.warn(
                            "Stock is no suspension, but suspension in local system, code = {}".format(code))
                        continue


# 完善交易数据
def gather_stock_trade_data(code, date):
    """
    向数据库中补充完善交易数据
    :param code: 补充数据的起始日期
    :param date: 代码编号
    :return:
    """
    __logger.info("Gather stock trade data, code = {}, date = {}".format(code, date))
    insert_datas = []
    # 上一个交易日
    yesterday_trade_date = my_common.get_yesterday_trading_date_before(date)
    yesterday_df = stock_trade_daily_dao.query_stock_trade_daily(code, str(yesterday_trade_date),
                                                                 str(yesterday_trade_date))
    yesterday_close = yesterday_df['close'].values[0]

    df = ts.get_k_data(code, str(date), pause=0.5)
    if len(df) > 0:
        for index, row in df.iterrows():
            # `code`, `open`, `high`, `low`, `close`, `volume`, `amount`, `turn_over_ratio`, `increase`, `amplitude`, `trade_date`
            # date  open  close  high   low    volume    code
            amount = 0
            turn_over_ratio = 0.0
            increase = (row['close'] - yesterday_close) / yesterday_close * 100.0
            amplitude = abs(row['high'] - row['low']) / yesterday_close * 100.0
            data = [my_common.convert_standard_code(row['code']), row['open'], row['high'], row['low'], row['close'],
                    row['volume'], amount, turn_over_ratio, increase, amplitude, row['date']]
            insert_datas.append(data)

            yesterday_close = row['close']

        stock_trade_daily_dao.insert_stock_trade_daily_batch(insert_datas)
        __logger.info(
            "Gather stock trade data success, code = {}, date = {}, size = {}".format(code, date, len(insert_datas)))

    else:
        __logger.warn("Get stock trade data empty, code = {}, date = {}".format(code, date))


def gather_current_day_stock_trade_data(date=None):
    """
    当天的交易截止后补充当天的交易数据
    :return:
    """
    if date:
        current_date = date
    else:
        current_date = datetime.date.today()
    if my_common.is_open_day(str(current_date)):
        day_all_df = ts.get_day_all(str(current_date))
        day_all_df.to_csv('/Users/gyang/develop/PycharmProjects/freedom/export/day_all.csv')
        if not day_all_df.empty:
            stock_series = stock_base_dao.query_stock_base_to_map()
            insert_datas = []
            for index, row in day_all_df.iterrows():
                code = my_common.convert_standard_code(row['code'])
                open = row['open']
                high = row['high']
                low = row['low']
                volume = row['volume']
                # 停牌
                if open == 0.0 and high == 0.0 and low == 0.0 and volume == 0.0:
                    __logger.warn("Stock is already suspension, code = {}".format(code))
                    continue

                # 查看在本系统中是否是停牌状态
                stock_base = stock_series.get(code)
                if stock_base:
                    if stock_base['status'] == 1:
                        data = [my_common.convert_standard_code(code), row['open'], row['high'], row['low'],
                                row['price'],
                                row['volume'], 0.0, 0.0, row['p_change'], row['range'], str(current_date)]
                        insert_datas.append(data)
                    else:
                        __logger.warn("Stock在系统中的状态为停牌或退市, code = {}, status = {}".format(code, stock_base['status']))

            # 删除当天的数据
            if len(insert_datas) > 0:
                stock_trade_daily_dao.delete_stock_trade_daily_by_trade_date(str(current_date), str(current_date))

            stock_trade_daily_dao.insert_stock_trade_daily_batch(insert_datas)
            __logger.info(
                "Gather current date stock trade data success, date = {}, size = {}".format(current_date,
                                                                                            len(insert_datas)))


def __process_gather_stock_trade_data():
    """
    完善交易数据信息，注意获取交易数据采用get_k_data方法，只能获取到前一天的数据
    :return:
    """
    yesterday_trade_date = my_common.get_yesterday_trading_date()
    trade_date_df = stock_trade_daily_dao.query_stock_max_trade_date()
    if len(trade_date_df) > 0:
        for index, row in trade_date_df.iterrows():
            try:
                code = row['code']
                max_trade_date = row['max_trade_date']
                # 如果是最新的交易日数据，则跳过
                if max_trade_date >= yesterday_trade_date:
                    __logger.info(
                        "Stock trade data is the newest data, code = {}, max_trade_date = {}".format(code,
                                                                                                     max_trade_date))
                    continue

                next_date = max_trade_date + datetime.timedelta(days=1)
                gather_stock_trade_data(code, next_date)
            except:
                __logger.exception("Gather stock trade data error, code = {}".format(code))


def __process_gather_real_time_stock_trade_data():
    """
    将当前实时交易的数据信息暂存
    :return:
    """
    date = str(datetime.date.today())
    today_df = ts.get_today_all()
    today_df.to_csv('/Users/gyang/develop/PycharmProjects/freedom/export/today_all_tmp.csv')
    # today_df = pd.read_csv('/Users/gyang/develop/PycharmProjects/freedom/export/today_all_tmp.csv')
    today_df = today_df.drop_duplicates(['code'])
    if not today_df.empty:
        insert_datas = []
        for index, row in today_df.iterrows():
            yesterday_close = row['settlement']
            if yesterday_close == 0.0:
                continue

            code = my_common.convert_standard_code(row['code'])
            amount = 0
            turn_over_ratio = 0.0
            increase = (row['trade'] - yesterday_close) / yesterday_close * 100.0
            amplitude = abs(row['high'] - row['low']) / yesterday_close * 100.0
            data = [code, row['open'], row['high'], row['low'], row['trade'],
                    row['volume'] / 100, amount, turn_over_ratio, increase, amplitude, date]
            insert_datas.append(data)

        stock_trade_daily_dao.insert_stock_trade_daily_batch(insert_datas)
        __logger.info("Gather temporary stock trade data success, code = {}, date = {}, size = {}".format(code, date,
                                                                                                          len(
                                                                                                              insert_datas)))


if __name__ == '__main__':
    # gather_stock_trade_data('300268')
    # __process_gather_stock_trade_data()
    # for i in range(3):
    #     __process_gather_stock_trade_data()
    # __process_gather_real_time_stock_trade_data()

    # day_all_df = ts.get_day_all('2018-07-25')
    # day_all_df.to_csv('/Users/gyang/develop/PycharmProjects/freedom/export/day_all.csv')
    # check_stock_status('2018-07-30')
    # gather_current_day_stock_trade_data('2018-07-30')
    print("done!!!")
    pass
