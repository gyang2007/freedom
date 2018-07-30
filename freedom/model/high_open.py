import datetime

import pandas as pd

import freedom.common as my_common
import freedom.db.stock_base_dao as stock_base_dao
import freedom.db.stock_trade_daily_dao as stock_trade_daily_dao
import freedom.log.logger as my_logger
import freedom.model.common_indicator as my_common_indicator

__logger = my_logger.getlogger('high_open')


def __is_jump_high(code, date):
    """
    是否是跳空高开的数据
    :param code: 代码
    :return: True | False
    """
    some_gap_date = date - datetime.timedelta(days=1)
    stock_trade_df = stock_trade_daily_dao.query_stock_trade_daily(code, str(some_gap_date),
                                                                   str(date))
    if len(stock_trade_df) >= 2:
        last = stock_trade_df[len(stock_trade_df) - 1:]
        last2 = stock_trade_df[len(stock_trade_df) - 2:len(stock_trade_df) - 1]

        last_low = last['low'].values[0]
        last2_high = last2['high'].values[0]
        if last_low - last2_high > 0:
            return True

    return False


def __process():
    trade_date = datetime.datetime.strptime('2018-07-26', '%Y-%m-%d')
    code_set = set()
    result_df = pd.DataFrame()
    stock_list = stock_base_dao.query_stock_base()

    for stock in stock_list:
        if stock['status'] == 1 and stock['type'] == 1:

            # 跳空高开
            if __is_jump_high(stock['code'], trade_date):
                code_set.add(stock['code'])

    # 输出跳空高开的code集合

    code_set_copy = set(code_set)
    for code in code_set_copy:
        # 是否高开一字涨停
        if my_common.is_jump_to_daily_limit(code_set, trade_date) or (
                not my_common.is_close_over_open_price(code, trade_date)):
            code_set.remove(code)

    result_df = pd.DataFrame(columns=['code', 'p_position', 'p_std', 'v_ratio'])
    # 计算成交量倍率，价格的标准差
    for code in code_set:
        v_ratio = my_common_indicator.avg_volume_ratio(code, trade_date, 10)
        if v_ratio and v_ratio >= 2.0:
            p_std = my_common_indicator.cal_price_std(code, trade_date, 20)
            p_position = my_common_indicator.cal_price_position(code, trade_date, 250)
            result_df.loc[len(result_df)] = [code, p_position, p_std, v_ratio]

    # 排序输出
    result_df = result_df.sort_values(by=['p_position', 'p_std', 'v_ratio'])
    result_df = result_df.reset_index(drop=True)
    result_df.to_csv("/Users/gyang/develop/PycharmProjects/freedom/export/high_open.csv")

    return result_df


if __name__ == '__main__':
    __process()
    pass
