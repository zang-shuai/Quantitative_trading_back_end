import datetime
import matplotlib.pyplot as plt

from api.utils.trade.stock_utils import Stock
from api.utils.trade.trade_utils import *


class User(object):
    def __init__(self, buy_run, sell_run, stock_pool=None, money=100000, income=5000,
                 start_date=datetime.datetime(2020, 3, 1),
                 end_date=datetime.datetime.today(), buy='', sell='', sell_point='a0', buy_point='a0'):
        self.sell_point = sell_point
        self.buy_point = buy_point
        if stock_pool is None:
            stock_pool = {'000001.SZ'}
        self.buy_run = buy_run
        self.sell_run = sell_run
        # self.buy_point = buy
        # self.sell_point = sell
        self.start_date = start_date
        self.end_date = end_date
        self.stock_pool = dict()
        for stock in stock_pool:
            self.stock_pool[stock] = Stock(stock)
        self.now_money = money
        self.now_money2 = money
        self.now_asset = money
        self.income = income
        self.money = {start_date: money}
        self.money2 = {start_date: money}
        self.asset = {start_date: money}
        self.position = dict()
        self.log = dict()

    def get_data(self, ts_code, now):
        try:
            return self.stock_pool[ts_code][now]['close']
        except Exception:
            return self.get_data(ts_code, now - datetime.timedelta(1))

    def get_asset(self, now=datetime.datetime.today()):
        res = self.now_money
        for ts_code in self.position:
            close = self.get_data(ts_code, now)
            res += self.position[ts_code] * close
        return res

    def buy(self, ts_code, trade_date, count):
        count *= 100
        amount = self.stock_pool[ts_code][trade_date]['open'] * count
        amount += self.service_charge_buy(amount)
        if amount < self.now_money:
            self.now_money = self.now_money - amount
            if ts_code in self.position:
                self.position[ts_code] = count + self.position[ts_code]
            else:
                self.position[ts_code] = count
            if trade_date not in self.log:
                self.log[trade_date] = dict()
            self.log[trade_date][ts_code] = count
            return True
        else:
            return False

    def sell(self, ts_code, trade_date, count):
        count *= 100
        amount = self.stock_pool[ts_code][trade_date]['close'] * count
        if self.position[ts_code] >= count:
            self.now_money = self.now_money + amount - self.service_charge_sell(amount)
            if self.position[ts_code] == count:
                del self.position[ts_code]
            else:
                self.position[ts_code] = self.position[ts_code] - count
            if trade_date not in self.log:
                self.log[trade_date] = dict()
            self.log[trade_date][ts_code] = -count
            return True
        else:
            return False

    def service_charge_buy(self, amount):
        if amount * 0.00025 < 5:
            return 5 + amount * 0.00002
        return amount * 0.00025 + amount * 0.00002

    def service_charge_sell(self, amount):
        if amount * 0.00025 < 5:
            return 5 + amount * 0.00002 + amount * 0.001
        return amount * 0.00025 + amount * 0.00002 + amount * 0.001

    def add_money(self, now, count):
        if now.day == 1:
            self.now_money += count
            self.now_money2 += count

    def buying_point(self, date):
        return self.buy_run(date, self.stock_pool, self.now_money)
        # if self.buy_point == 'a0':
        #     return double_averages_buying_point1(date, self.stock_pool, self.now_money)
        # elif self.buy_point == 'a1':
        #     return double_averages_buying_point2(date, self.stock_pool, self.now_money)
        # else:
        #     pass

    def selling_point(self, date):
        return self.sell_run(date, self.position, self.stock_pool, self.now_money)
        # if self.sell_point == 'a0':
        #     return double_averages_selling_point1(date, self.position, self.stock_pool, self.now_money)
        # elif self.sell_point == 'a1':
        #     return double_averages_selling_point2(date, self.position, self.stock_pool, self.now_money)
        # else:
        #     pass

    def advance(self):
        now = self.start_date
        while (now - self.end_date).days < 0:
            self.add_money(now, self.income)
            print(now)
            if Stock.is_trade_day(now):
                sell_stocks = self.selling_point(now)
                for stock in sell_stocks:
                    self.sell(stock, now, sell_stocks[stock])
                buy_stocks = self.buying_point(now)
                for stock in buy_stocks:
                    self.buy(stock, now, buy_stocks[stock])
            self.money[now] = self.now_money
            self.money2[now] = self.now_money2
            self.asset[now] = self.get_asset(now)
            now = now + datetime.timedelta(1)

    def return_data(self):
        date = []
        for ass in self.asset:
            date.append(ass.strftime('%Y%m%d'))
        log = dict()
        for k in self.log:
            log[k.strftime('%Y-%m-%d')] = self.log[k]
        return {
            'date': date,
            'asset': list(self.asset.values()),
            'money': list(self.money2.values()),
            'log': log,
            'position': self.position
        }

    def draw(self):
        plt.plot(range(0, len(self.asset.values())), self.asset.values())
        plt.plot(range(0, len(self.money2.values())), self.money2.values())
        plt.show()

# if __name__ == '__main__':
#     user_data = {
#         'money': 100000,
#         'income': 5000,
#         'start_date': datetime.datetime(2012, 1, 1),
#         'end_date': datetime.datetime.today(),
#         'stock_pool': ['000001.SZ', ]
#     }
#     u = User(**user_data)
#     u.advance()
#     u.draw()
#
#     for i in u.log:
#         print(i, '----', u.log[i])
#     print(u.get_asset())
