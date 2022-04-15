import tushare as ts
import numpy as np
import datetime

pro = ts.pro_api()


class Stock(object):
    def __init__(self, ts_code, start_date='20100101', end_date=datetime.date.today().strftime("%Y%m%d")):
        self.daily = pro.query('daily', ts_code=ts_code, start_date=start_date, end_date=end_date)
        self.weekly = pro.query('weekly', ts_code=ts_code, start_date=start_date, end_date=end_date)
        self.monthly = pro.query('monthly', ts_code=ts_code, start_date=start_date, end_date=end_date)

        # 取000001的前复权行情
        # self.df_before = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
        # # 取000001的后复权行情
        # self.df_after = ts.pro_bar(ts_code='000001.SZ', adj='hfq', start_date='20180101', end_date='20181011')
        pass

    def get_k_image(self):
        n = np.array(self.daily.get(['trade_date', 'open', 'close', 'low', 'high'])).tolist()
        return n

# s1 = Stock('000001.SZ')
# print(s1.get_k_image())
