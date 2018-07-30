import time

import freedom.db.stock_trade_daily_dao as stock_trade_daily_dao
import freedom.db.stock_trade_calendar_dao as stock_trade_calendar_dao
import freedom.db.stock_base_dao as stock_base_dao

# df = stock_trade_daily_dao.query_stock_max_trade_date()
# print(df)

# result = stock_trade_calendar_dao.get_one('2018-07-25')
# # print(result)


# result = stock_base_dao.query_stock_base_by_code('123456')
# print(result)

# for i in range(100):
#     stock_trade_daily_dao.query_stock_trade_daily_limit_size('000001', '2018-07-25', 1)
#     print(i)
#     time.sleep(0.5)
#
# time.sleep(1000)

result_series = stock_base_dao.query_stock_base_to_map()
print(result_series)