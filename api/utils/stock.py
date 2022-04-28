import tushare as ts
import numpy as np
import datetime

pro = ts.pro_api()


class User(object):
    def __init__(self, money):
        self.money = money

    def buy(self, stock_code, count):
        pass

    def sell(self, stock_code, count):
        pass


class Stock(object):
    def __init__(self, ts_code, start_date='20100101', end_date=datetime.date.today().strftime("%Y%m%d")):
        self.daily = pro.query('daily', ts_code=ts_code, start_date=start_date, end_date=end_date)
        self.daily.set_index(
            ['trade_date'], inplace=True)

    def get_k_image(self):
        n = np.array(self.daily.get(['trade_date', 'open', 'close', 'low', 'high'])).tolist()
        return n

    def __getitem__(self, item):
        return self.daily.get(str(item))

#
# s1 = Stock('000001.SZ')
# print(s1.daily)
