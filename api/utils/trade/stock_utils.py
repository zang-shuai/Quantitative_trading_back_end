import datetime
from collections import deque

import numpy as np
import tushare as ts
import pandas as pd
from sklearn.preprocessing import StandardScaler

pro = ts.pro_api('3cb9379a9a4f25f917b9f7cf73030848f2922944e98a52e3b5686b90')
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
        #
        # self.ts_code = ts_code
        # self.daily = pro.query('daily', ts_code=ts_code, start_date=start_date, end_date=end_date)
        # self.daily.set_index(
        #     ['trade_date'], inplace=True)
        self.standard_daily = self.Stock_Price_LSTM_Data_Precesing(ts_code, 5)

    def get_k_image(self):
        n = np.array(self.daily.get(['trade_date', 'open', 'close', 'low', 'high'])).tolist()
        return n

    def Stock_Price_LSTM_Data_Precesing(self, ts_code, men_his_days):
        df = pro.daily(ts_code=ts_code, fields=["trade_date", "open", "high", "low", "close", "vol", "amount"])
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df['trade_date'] = df['trade_date'].dt.strftime('%Y%m%d')
        df = df.set_index('trade_date')
        df = df.sort_index(ascending=True)
        # label: 10天后的价格
        trade_date = df.index.tolist()
        scaler = StandardScaler()
        sca_X = scaler.fit_transform(df.iloc[:, :])
        deq = deque(maxlen=men_his_days)
        X_dict = dict()
        trade_date_index = 0
        for i in sca_X:
            deq.append(list(i))
            trade_date_index += 1
            if len(deq) == men_his_days:
                if trade_date_index >= len(trade_date):
                    break
                # print(trade_date[trade_date_index])
                X_dict[trade_date[trade_date_index]] = list(deq)
        # print()
        return X_dict

    def __getitem__(self, trade_date):
        try:
            data = self.daily.loc[trade_date.strftime('%Y%m%d')]
            return data
        except Exception:
            return False

    def is_trade_day(date):
        return int(trade_cal[trade_cal['cal_date'] == date.strftime('%Y%m%d')]['is_open']) == 1

    def get_standard_data(self, now):
        try:
            res = self.standard_daily[now.strftime('%Y%m%d')]
            return res
        except Exception:
            return None



# class Stock(object):
#     def __init__(self, ts_code):
#         self.ts_code = ts_code
#         daily = pro.daily(ts_code=ts_code).set_index('trade_date').sort_index(ascending=True)
#         daily['ma5'] = daily['close'].rolling(5).mean()
#         daily['ma10'] = daily['close'].rolling(10).mean()
#         daily['ma30'] = daily['close'].rolling(30).mean()
#         daily['ma120'] = daily['close'].rolling(120).mean()
#         self.daily = daily
#
#     def __getitem__(self, trade_date):
#         try:
#             data = self.daily.loc[trade_date.strftime('%Y%m%d')]
#             return data
#         except Exception:
#             return False
#
#     def is_trade_day(date):
#         return int(trade_cal[trade_cal['cal_date'] == date.strftime('%Y%m%d')]['is_open']) == 1


class StockPool(object):
    def __init__(self, ts_codes):
        self.ts_codes = ts_codes
        self.stocks = {}
        for ts_code in self.ts_codes:
            self.stocks[ts_code] = Stock(ts_code)

    def __getitem__(self, item):
        return self.stocks[item]

s = Stock('000001.SZ')
# print(s.daily)
# for i in s.get_standard_data(datetime.datetime(2020,12,31)):
#     print(i)
