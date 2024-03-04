from collections import deque

import tushare as ts
import numpy as np
import datetime
import pandas as pd

from sklearn.preprocessing import StandardScaler

pro = ts.pro_api('3cb9379a9a4f25f917b9f7cf73030848f2922944e98a52e3b5686b90')


class User(object):
    def __init__(self, money):
        self.money = money

    def buy(self, stock_code, count):
        pass

    def sell(self, stock_code, count):
        pass


class Stock(object):
    def __init__(self, ts_code, start_date='20100101', end_date=datetime.date.today().strftime("%Y%m%d")):
        self.ts_code = ts_code
        self.daily = pro.query('daily', ts_code=ts_code, start_date=start_date, end_date=end_date)
        self.daily.set_index(
            ['trade_date'], inplace=True)
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
                X_dict[trade_date[i]] = list(deq)
        return X_dict

    def __getitem__(self, item):
        return self.daily.get(str(item))

    def get_standard_data(self, now):
        return self.standard_daily[now.strftime('%Y-%m-%d')]
