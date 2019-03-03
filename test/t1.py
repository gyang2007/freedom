import datetime
import time
import tushare as ts
import pandas as pd
import talib as ta
import numpy as np

# now = datetime.datetime.now()
# point_time = datetime.datetime.strptime('{}-{}-{} {}:{}:{}'.format(now.year, now.month, now.day, '09', '30', '00'),
#                                         '%Y-%m-%d %H:%M:%S')
#
# if now < point_time:
#     print(True)

# df = ts.get_k_data('300242', start='2018-06-23', end='2018-07-24')
# print(df)
# sma = ta.SMA(df['close'], timeperiod=5)
# std = pd.DataFrame(sma[4:]).std()
# print(sma)

# df = pd.DataFrame(columns=('code', 'name', 'close', 'std'))
# df.loc[len(df.index)] = ['123456', '测试', 10.34, 0.245]
# df.loc[len(df.index)] = ['456789', '测试', 4.5, 3.3]
#
# print(df)
# print(len(df))
# print(len(df.index))

df = pd.DataFrame({'a': [1, 2, 3], 'b': [1, None, None], 'c': [1, 2, 3], 'd': ['d1', 'd2', None]},
                  columns=['a', 'b', 'c', 'd'])
# df['b'] = -1
# df['b'][0] = 1
# df['b'][1] = 2
# df['b'][2] = 3
# df.loc[len(df)] = [4, 4, None, 'd4']
# df.sort_values(by=['b'])
# print(df)
# print(df.loc[0:1, 'a':'c'])
# print(df[['a', 'c']])
# print(df[0:1])
# print(df['a'].max())

dd = datetime.datetime.strptime('2018-07-25', '%Y-%m-%d')
dd2 = dd - datetime.timedelta(days=1)
print(dd > dd2)

# df = ts.get_day_all('2018-07-24')
# print(df)

# df = ts.get_k_data('300046', '2018-07-20')
# print(df)

# sss = set(("Google", "Runoob", "Taobao"))
# # sss2 = set(sss)
# # for s in sss:
# #     sss2.remove(s)
# #
# # print(sss)
# # print(sss2)

# sss = pd.Series({'000123': {'a1': 'v1', 'a2': 'v2'}, '000001': {'b1': 'v1', 'b2': 'v2'}})
# sss = sss.append(pd.Series({'000005': {'c1': 'c1', 'a2': 'v2'}}))
# print(sss)
# result = sss.get('000123')
# if not result:
#     print(True)

# d = datetime.date.today()
# dd = datetime.datetime.combine(d, datetime.datetime.min.time())
#
# print(d)
# print(dd)
# print(datetime.datetime.today())

# print(np.std([3, 5, 7], ddof=1))
# print(np.std([8, 10, 12], ddof=1))
# print(np.std([98, 100, 102], ddof=1))
#
# df = pd.DataFrame([8, 10, 12])
# print(df.std()[0])
