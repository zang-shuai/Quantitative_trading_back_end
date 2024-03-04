import tushare as ts
import numpy as np
import datetime

pro = ts.pro_api('3cb9379a9a4f25f917b9f7cf73030848f2922944e98a52e3b5686b90')

'''
dt = datetime.datetime(2019,6,10)
'''


def get_stock_daily(ts_code, trade_date, data):
    if type(trade_date) == type(datetime.datetime(2022, 4, 15)):
        trade_date = trade_date.strftime("%Y%m%d")
    return pro.index_daily(**{
        "ts_code": ts_code,
        "trade_date": trade_date,
    }, fields=[
        data
    ])[data].loc[0]


