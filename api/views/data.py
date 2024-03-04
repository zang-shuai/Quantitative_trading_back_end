import datetime

import tushare as ts
from django.http import JsonResponse

pro = ts.pro_api('3cb9379a9a4f25f917b9f7cf73030848f2922944e98a52e3b5686b90')


def get_daily(request):
    fields = ['trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount']
    ts_code = request.GET.get('ts_code')
    df = pro.daily(ts_code=ts_code, fields=fields)
    data = df.to_dict(orient='records')[::-1]
    return JsonResponse(data, safe=False)
