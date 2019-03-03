import pandas as pd
import sys
from sqlalchemy import create_engine
import freedom.db.dbutil as db_util
import freedom.db.stock_trade_daily_dao as stock_trade_daily_dao
import freedom.db.stock_base_dao as stock_base_dao
import tushare as ts


# sql = 'select `code`, `open`, `high`, `low`, `close`, `volume`, `trade_date` from stock_trade_daily where `code` = "300268" order by `trade_date`'
# df = pd.read_sql(sql, con=db_util.get_connection())
# print(df)

# stocks = stock_base_dao.query_stock_base()
# print(stocks)

df = ts.get_stock_basics()
df.to_csv('/Users/gyang/develop/PycharmProjects/freedom/docs/stock_basics.csv');