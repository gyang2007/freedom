import datetime

import pandas as pd
import talib as ta

import freedom.db.stock_base_dao as stock_base_dao
import freedom.db.stock_trade_daily_dao as stock_trade_daily_dao
import freedom.log.logger as my_logger
import freedom.model.common_indicator as my_common_indicator

__logger = my_logger.getlogger('candle_stick')


def white_line_over_sma5_10_20(code, date):
    """
    筛选上一个交易日的收盘价和当天收盘价由下到上穿越5、10、20日均线
    :param df:
    :return:
    """
    df = stock_trade_daily_dao.query_stock_trade_daily_limit_size(code, str(date), 20)
    if len(df) < 20:
        __logger.warn("Valid DataFrame data size less than 20, code = {}, date = {}".format(code, str(date)))
        return False

    # 当前收盘价
    current_close = df[len(df) - 1:]['close'].values[0]
    # 上一个交易日收盘价
    yesterday_close = df[len(df) - 2:len(df) - 1]['close'].values[0]
    if current_close > yesterday_close:
        # 5日均线
        ma5s = ta.SMA(df['close'], timeperiod=5)
        current_ma5 = ma5s[len(ma5s) - 1:].values[0]
        # 10日均线
        ma10s = ta.SMA(df['close'], timeperiod=10)
        current_ma10 = ma10s[len(ma10s) - 1:].values[0]
        # 20日均线
        ma20s = ta.SMA(df['close'], timeperiod=20)
        current_ma20 = ma20s[len(ma20s) - 1:].values[0]

        if current_close >= current_ma5 and current_close >= current_ma10 and current_close >= current_ma20 and yesterday_close <= current_ma5 and yesterday_close <= current_ma10 and yesterday_close <= current_ma20:
            __logger.info(
                "white line over ma5, ma10, ma20 stick line, code = {}, current_close = {}, yesterday_close = {}, current_ma5 = {}, current_ma10 = {}, current_ma20 = {}".format(
                    code, current_close, yesterday_close, current_ma5, current_ma10, current_ma20))
            return True

    return False


if __name__ == '__main__':
    trade_date = datetime.datetime.strptime('2018-07-25', '%Y-%m-%d')

    result_df = pd.DataFrame(columns=['code', 'name', 'p_position', 'p_std', 'v_ratio'])
    stock_list = stock_base_dao.query_stock_base()
    for stock in stock_list:
        code = stock['code']
        if stock['status'] == 1 and stock['type'] == 1:
            if white_line_over_sma5_10_20(code, trade_date):
                v_ratio = my_common_indicator.avg_volume_ratio(code, trade_date, 10)
                if v_ratio and v_ratio >= 2.0:
                    p_position = my_common_indicator.cal_price_position(code, trade_date, 250)
                    p_std = my_common_indicator.cal_price_std(code, trade_date, 20)
                    result_df.loc[len(result_df)] = [code, stock['name'], p_position, p_std, v_ratio]

    result_df = result_df.sort_values(by=['p_position', 'p_std', 'v_ratio'])
    result_df = result_df.reset_index(drop=True)
    result_df.to_csv('/Users/gyang/develop/PycharmProjects/freedom/export/white_line_over_sma5_10_20.csv')
    print("done!!!")
