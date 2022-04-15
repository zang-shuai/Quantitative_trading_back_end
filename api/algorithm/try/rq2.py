import tushare as ts
ts.set_token('3cb9379a9a4f25f917b9f7cf73030848f2922944e98a52e3b5686b90')
pro = ts.pro_api()
df = pro.index_daily(ts_code='000001.SH',start_date="20190101")
df = df.sort_values(by='trade_date',ascending=True)
df = df.reset_index(drop=True)
df.rename(columns={'vol':'volume'}, inplace = True)