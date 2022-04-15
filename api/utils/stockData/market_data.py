import tushare as ts

pro = ts.pro_api()


def get_daily(**kwargs):
    df = pro.daily(**kwargs)
    return df


print(get_daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718'))
