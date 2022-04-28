import datetime
import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from Quantitative_trading_back_end.settings import MEDIA_URL
from api.models import UserInfo
from api.utils.encrypt import create_token
from api.utils.trade.stock_utils import get_concept_detail
from api.utils.trade.trade_utils import *
from api.utils.trade.user_utils import User


@csrf_exempt
def quantitative_trading_img(request):
    params = dict()
    for i in request.POST:
        params[i] = request.POST[i]
    params['stock_pool'] = params['stock_pool'].split(',')
    uselist = []
    for p in params['stock_pool']:
        if p[0:2] == 'TS':
            l = get_concept_detail(p)
            for li in l:
                uselist.append(li[0])
        else:
            uselist.append(p)
    params['stock_pool'] = uselist

    user_data = {
        'buy_run': double_averages_buying_point1,
        'sell_run': double_averages_selling_point1,
        'money': int(params['basic_money']),
        'income': int(params['month_income']),
        'start_date': datetime.datetime.strptime(params['start_date'], '%Y-%m-%d'),
        'end_date': datetime.datetime.today(),
        'stock_pool': params['stock_pool'],
        'buy': params['buy'],
        'sell': params['sell'],
    }
    print(user_data)
    code = 'ok'
    try:
        u = User(**user_data)
        u.advance()
        code = u.return_data()
    except Exception:
        code = 'err'

    return JsonResponse({
        'code': code
    })
