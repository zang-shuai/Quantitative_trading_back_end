import datetime

import numpy as np
import tushare as ts

pro = ts.pro_api()
trade_cal = pro.trade_cal()


def get_concept_detail(id):
    return np.array(pro.concept_detail(id=id, fields='ts_code')).tolist()


def get_total_mv(ts_code, trade_date):
    if type(trade_date) == type(' '):
        return int(pro.daily_basic(ts_code=ts_code, trade_date=trade_date, fields='total_mv')['total_mv'])
    else:
        return int(
            pro.daily_basic(ts_code=ts_code, trade_date=trade_date.strftime('%Y%m%d'), fields='total_mv')['total_mv'])


class Stock(object):
    def __init__(self, ts_code):
        self.ts_code = ts_code
        daily = pro.daily(ts_code=ts_code).set_index('trade_date').sort_index(ascending=True)
        daily['ma5'] = daily['close'].rolling(5).mean()
        daily['ma10'] = daily['close'].rolling(10).mean()
        daily['ma30'] = daily['close'].rolling(30).mean()
        daily['ma120'] = daily['close'].rolling(120).mean()
        self.daily = daily

    def __getitem__(self, trade_date):
        try:
            data = self.daily.loc[trade_date.strftime('%Y%m%d')]
            return data
        except Exception:
            return False

    def is_trade_day(date):
        return int(trade_cal[trade_cal['cal_date'] == date.strftime('%Y%m%d')]['is_open']) == 1


class StockPool(object):
    def __init__(self, ts_codes):
        self.ts_codes = ts_codes
        self.stocks = {}
        for ts_code in self.ts_codes:
            self.stocks[ts_code] = Stock(ts_code)

    def __getitem__(self, item):
        return self.stocks[item]
