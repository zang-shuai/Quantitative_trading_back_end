import datetime
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import load_model

from api.utils.trade.stock_utils import Stock
from api.utils.trade.trade_utils import *

from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time

m = PyMouse()
k = PyKeyboard()


class User(object):
    def __init__(self, buy_run, sell_run, stock_pool=None, money=100000, income=5000, model=None,
                 start_date=datetime.datetime(2020, 3, 1), now_price=None, buy_sell=False,
                 end_date=datetime.datetime.today(), buy='', sell='', sell_point='a0', buy_point='a0'):
        self.now_price = now_price
        self.buy_sell = buy_sell
        self.stock_pool = dict()
        self.position = dict()
        self.sell_point = sell_point
        self.buy_point = buy_point
        if stock_pool is None:
            self.stock_pool['000001.SZ'] = Stock('000001.SZ')
        else:
            for stock in stock_pool:
                self.stock_pool[stock] = Stock(stock)
                # self.position[stock] = 0
        self.buy_run = buy_run
        self.sell_run = sell_run
        if model:
            self.model = load_model(model)
        else:
            self.model = None
        self.start_date = start_date
        self.end_date = end_date
        self.now_money = money
        self.now_money2 = money
        self.now_asset = money
        self.income = income
        self.money = {start_date: money}
        self.money2 = {start_date: money}
        self.asset = {start_date: money}
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
        return self.buy_run(date, self.stock_pool, self.now_money, self.model)
        # if self.buy_point == 'a0':
        #     return double_averages_buying_point1(date, self.stock_pool, self.now_money)
        # elif self.buy_point == 'a1':
        #     return double_averages_buying_point2(date, self.stock_pool, self.now_money)
        # else:
        #     pass

    def selling_point(self, date):
        return self.sell_run(date, self.position, self.stock_pool, self.now_money, self.model)
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
        if self.buy_sell:
            self.trade()

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

    def trade(self):
        while True:
            now = datetime.datetime.today()
            if now.min == 31 and now.hour == 9 and now.second == 1:
                pre_date = now
                while True:
                    pre_date = pre_date - datetime.timedelta(1)
                    if Stock.is_trade_day(pre_date):
                        break
                self.add_money(now, self.income)
                print(now)
                if Stock.is_trade_day(pre_date):
                    sell_stocks = self.selling_point(pre_date)
                    for stock in sell_stocks:
                        self.sell(stock, now, sell_stocks[stock])
                        self.click_sell(stock, sell_stocks[stock] * 100)
                    buy_stocks = self.buying_point(pre_date)
                    for stock in buy_stocks:
                        self.buy(stock, now, buy_stocks[stock])
                        self.click_buy(stock, sell_stocks[stock] * 100)
                self.money[now] = self.now_money
                self.money2[now] = self.now_money2
                self.asset[now] = self.get_asset(now)
                pass
            else:
                pass

    def clear_ts_code(self):
        # 双击代码
        m.click(58, 194, 1, 1)
        m.click(159, 195, 1, 2)
        time.sleep(2)
        for i in range(8):
            k.press_key('delete')
        time.sleep(2)

    def click_buy(self, ts_code, count):
        self.clear_ts_code()
        # 点击买入
        m.click(66, 132, 1, 1)
        # 点击代码
        time.sleep(1)
        m.click(85, 196, 1, 1)
        time.sleep(1)
        k.type_string(ts_code[0:7])
        # 点击数量
        m.click(78, 303, 1, 1)
        time.sleep(1)
        k.type_string(str(count))
        # 确定买入
        time.sleep(1)
        m.click(112, 348, 1, 1)
        time.sleep(1)
        m.click(364, 593, 1, 1)
        m.click(323, 564, 1, 1)

    def click_sell(self, ts_code, count):
        self.clear_ts_code()
        # 点击买入
        m.click(145, 131, 1, 1)
        # 点击代码
        time.sleep(1)
        m.click(85, 196, 1, 1)
        time.sleep(1)
        k.type_string(ts_code[0:7])
        # 点击数量
        m.click(78, 303, 1, 1)
        time.sleep(1)
        k.type_string(str(count))
        # 确定买入
        time.sleep(1)
        m.click(112, 348, 1, 1)
        time.sleep(1)
        m.click(364, 593, 1, 1)
        m.click(323, 564, 1, 1)


# 买点
def my_buy_point(date, stock_pool, now_money, model):
    res = dict()
    for stock in stock_pool:
        s = stock_pool[stock]
        pre_date = date
        while True:
            pre_date = pre_date - datetime.timedelta(1)
            if Stock.is_trade_day(pre_date):
                break
        now_stock = s[date]
        pre_stock = s[pre_date]
        if type(now_stock) != type(False) and type(pre_stock) != type(False) and now_stock['ma5'] > now_stock[
            'ma10'] and pre_stock['ma5'] < pre_stock['ma10']:
            res[s.ts_code] = now_money // (now_stock['open'] * 100) // 2
    return res


# 卖点
def my_sell_point(date, position, stock_pool, now_money, model):
    res = dict()
    for stock in position:
        s = stock_pool[stock]
        pre_date = date
        while True:
            pre_date = pre_date - datetime.timedelta(1)
            if Stock.is_trade_day(pre_date):
                break
        now_stock = s[date]
        pre_stock = s[pre_date]
        if type(now_stock) != type(False) and type(pre_stock) != type(False) and now_stock['ma10'] > now_stock[
            'ma5'] and pre_stock['ma10'] < pre_stock['ma5']:
            res[s.ts_code] = position[s.ts_code] // 100
    return res


user_data = {
    # 基础资金
    'money': 100000,
    # 月收入
    'income': 5000,
    # 开始日期
    'start_date': datetime.datetime(2015, 1, 1),
    # 结束日期
    'end_date': datetime.datetime.today(),
    # 股票池
    'stock_pool': ['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ'],
    # 买点
    'buy_run': my_buy_point,
    # 卖点
    'sell_run': my_sell_point,
    'model': None,
}

# u = User(**user_data)
# u.advance()
# print(u.log)
#
# print(u.return_data())