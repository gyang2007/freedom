import tushare as ts
import datetime
import talib as ta
import numpy as np

if __name__ == '__main__':
    # df = ts.trade_cal()
    # print(ts.is_holiday(str(datetime.date.today())))
    # print(ta.MA(np.array([1.0, 321.0, 231.0, 321.0, 45.0, 46.0, 57.0, 897.0, 987.0, 64.0, 78987.0, 31.0, 32.0, 654.0, 5.0]), 5))
    current_date = datetime.date.today()
    current_date_30d_before = current_date - datetime.timedelta(days=30)
    datas = ts.get_k_data('603658', start=str(current_date_30d_before), end=str(current_date))
    pass
