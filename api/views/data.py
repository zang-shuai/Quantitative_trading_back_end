import datetime

import tushare as ts
from django.http import JsonResponse

pro = ts.pro_api()


def get_daily(request):
    fields = ['trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount']
    # fields = ','.join(fields)
    ts_code = request.GET.get('ts_code')
    # start_date = request.GET.get('start_date')
    # if not start_date:
    #     start_date = '20000101'
    # end_date = request.GET.get('end_date')
    # if not end_date:
    #     end_date = datetime.date.today().strftime("%Y%m%d")
    # df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date,
    #                fields=fields)
    # df = pro.daily(ts_code=ts_code, fields=fields)
    print('xxxxxxxx')
    print(ts_code)
    print('xxxxxxxx')
    df = pro.daily(ts_code=ts_code, fields=fields)
    print(df)
    data = df.to_dict(orient='records')[::-1]
    print('xxx')
    # print(data)
    return JsonResponse(data, safe=False)
