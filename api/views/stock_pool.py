import datetime

import numpy as np
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
# 导入tushare
import tushare as ts
from api.models import UserSelect

# 初始化pro接口
pro = ts.pro_api()


@csrf_exempt
def getHs300(request):
    df = np.array(pro.index_weight(**{
        "index_code": "000300.SH",
        "trade_date": 20220401,
        "start_date": "",
        "end_date": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "con_code",
        "weight"
    ])).tolist()
    return JsonResponse({
        'data': df
    })

    pass


@csrf_exempt
def getMySelect(request):
    data = UserSelect.objects.filter(user_id=request.POST.get('user_id'))
    l_data = []
    for i in data:
        l_data.append(i.ts_code)
    print('++++++')
    print(l_data)
    print('++++++')

    return JsonResponse({
        'data': l_data
    })


@csrf_exempt
def plate(request):
    df = np.array(pro.concept(**{
        "src": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "code",
        "name"
    ])).tolist()

    return JsonResponse({
        'data': df
    })
    pass


@csrf_exempt
def smallMoney(request):
    smallmoney = request.POST.get('smallmoney')
    pass


@csrf_exempt
def allstock(request):
    # 拉取数据
    df = np.array(pro.stock_basic(**{
        "ts_code": "",
        "name": "",
        "exchange": "",
        "market": "",
        "is_hs": "",
        "list_status": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "name",
        "ts_code"
    ])).tolist()
    return JsonResponse({
        'data': df
    })
