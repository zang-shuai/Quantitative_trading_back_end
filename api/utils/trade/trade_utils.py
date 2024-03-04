import datetime

from api.utils.trade.stock_utils import Stock


def double_averages_buying_point1(date, stock_pool, now_money,model):
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


def double_averages_selling_point1(date, position, stock_pool, now_money,model):
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
        if type(now_stock) != type(False) and type(pre_stock) != type(False) and now_stock['ma30'] > now_stock[
            'ma5'] and pre_stock['ma30'] < pre_stock['ma5']:
            res[s.ts_code] = position[s.ts_code] // 100
    return res


def double_averages_buying_point2(date, stock_pool, now_money,model):
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


def double_averages_selling_point2(date, position, stock_pool, now_money,model):
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


def ai_buying_point(now, stock_pool, now_money, model):
    res = dict()
    for stock in stock_pool:
        s = stock_pool[stock]
        standard_data = s.get_standard_data(now)
        predict = model.predict(standard_data)
        if predict - s[now]['open'] > 5:
            res[s.ts_code] = now_money // (s[now]['open'] * 100) // 2
    return res


def ai_averages_selling_point(now, position, stock_pool, now_money, model):
    res = dict()
    for stock in stock_pool:
        s = stock_pool[stock]
        standard_data = s.get_standard_data(now)
        predict = model.predict(standard_data)
        if predict - s[now]['open'] < -5:
            res[s.ts_code] = position[s.ts_code] // 100
    return res


# return render(request,'xxx.html',{
#     img: '/xxx/xxx/xx.jpg'
# })
#
#
#
# 127.0.0.1:8080/+{{img}}