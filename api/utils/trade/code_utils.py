# 买点
import datetime


def my_buy_point():
    print('xxxx')
    pass


# 卖点
def my_sell_point():
    print('yyyy')
    pass


user_data = {
    # 基础资金
    'money': 100000,
    # 月收入
    'income': 5000,
    # 开始日期
    'start_date': datetime.datetime(2001, 1, 1),
    # 结束日期
    'end_date': datetime.datetime.today(),
    # 股票池
    'stock_pool': ['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ'],
    # 买点
    'buy': my_buy_point,
    # 卖点
    'sell': my_sell_point
}


def run(a):
    a()


run(my_sell_point)
