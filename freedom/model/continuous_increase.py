"""
回测连续涨停的股票
"""

import pandas as pd

import freedom.db.stock_base_dao as stock_base_dao
import freedom.db.stock_trade_daily_dao as stock_trade_daily_dao
import freedom.log.logger as my_logger

__logger = my_logger.getlogger('continuous_increase')


def _t1():
    columns = ["code", "status", "trade_date"]
    three_day_list = []
    four_day_list = []
    # 涨停
    increase_upper = 9.8
    start_date = '2017-01-01'
    end_date = '2018-10-01'
    stock_base_list = stock_base_dao.query_stock_base()
    # stock_base_list = stock_base_list[0:100]
    for stock_base in stock_base_list:
        df = stock_trade_daily_dao.query_stock_trade_daily(stock_base['code'], start_date, end_date)
        start_index = 0
        end_index = start_index + 1
        length = len(df)
        while end_index <= length:
            increase = df[start_index:end_index]['increase'].values[0]
            amplitude = df[start_index:end_index]['amplitude'].values[0]
            trade_date = df[start_index:end_index]['trade_date'].values[0]
            # 第一天涨停且振幅大于0
            if increase >= increase_upper and increase < 12.0 and amplitude > 0.0:
                start_index = end_index
                end_index = start_index + 1
                if end_index > length:
                    break

                # 第二天涨停
                increase = df[start_index:end_index]['increase'].values[0]
                if increase >= increase_upper:
                    start_index = end_index
                    end_index = start_index + 1
                    if end_index > length:
                        break

                    # 第三天涨停
                    increase = df[start_index:end_index]['increase'].values[0]
                    if increase >= increase_upper:
                        three_day_list.append({"code": stock_base['code'], "status": "true", "trade_date": trade_date})
                        # 连续三天涨停
                        __logger.info(
                            "连续两天涨停后第三天是否继续涨停, code = {}, status = {}, trade_date = {}".format(stock_base['code'],
                                                                                               'true', trade_date))
                        start_index = end_index
                        end_index = start_index + 1
                        if end_index > length:
                            break

                        # 第四天涨停
                        increase = df[start_index:end_index]['increase'].values[0]
                        if increase >= increase_upper:
                            four_day_list.append(
                                {"code": stock_base['code'], "status": "true", "trade_date": trade_date})
                            # 连续四天涨停
                            __logger.info(
                                "连续三天涨停后第四天是否继续涨停, code = {}, status = {}, trade_date = {}".format(stock_base['code'],
                                                                                                   'true', trade_date))
                            while True:
                                start_index = end_index
                                end_index = start_index + 1
                                if end_index > length:
                                    break

                                increase = df[start_index:end_index]['increase'].values[0]
                                if increase < increase_upper:
                                    start_index = end_index
                                    end_index = start_index + 1
                                    break
                        else:
                            four_day_list.append(
                                {"code": stock_base['code'], "status": "false", "trade_date": trade_date})
                            __logger.info(
                                "连续三天涨停后第四天是否继续涨停, code = {}, status = {}, trade_date = {}".format(stock_base['code'],
                                                                                                   'false', trade_date))
                            start_index = end_index
                            end_index = start_index + 1

                    # 第三天没涨停
                    else:
                        three_day_list.append(
                            {"code": stock_base['code'], "status": "false", "trade_date": trade_date})
                        __logger.info(
                            "连续两天涨停后第三天是否继续涨停, code = {}, status = {}, trade_date = {}".format(stock_base['code'],
                                                                                               'false', trade_date))

                        start_index = end_index
                        end_index = start_index + 1
                else:
                    start_index = end_index
                    end_index = start_index + 1
            else:
                start_index = end_index
                end_index = start_index + 1

    three_day_df = pd.DataFrame(three_day_list, columns=columns)
    four_day_df = pd.DataFrame(four_day_list, columns=columns)

    three_day_df.to_csv('/Users/gyang/test/three.csv')
    four_day_df.to_csv('/Users/gyang/test/four.csv')


if __name__ == '__main__':
    _t1()
    pass
