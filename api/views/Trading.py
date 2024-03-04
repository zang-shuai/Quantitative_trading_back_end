import datetime
import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model

from Quantitative_trading_back_end.settings import MEDIA_URL
from api import models
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
        # 'model': load_model('../../media/ai_code/' + params['userid']+'/model/train_params.h5')
    }
    # print(user_data)
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


@csrf_exempt
def quantitative_trading_code(request):
    params = dict()
    content = request.POST.get("content")
    g = {'res1': ''}
    exec(content, g)
    return JsonResponse({
        'code': g['result']
    })


@csrf_exempt
def get_ai_list(request):
    id = request.POST.get("id")
    objs = models.AIStrategy.objects.filter(user_id=int(id))
    code = []
    for obj in objs:
        code.append(obj.code)
    return JsonResponse({
        'code': code
    })


@csrf_exempt
def add_ai_list(request):
    ai_name = request.POST.get("ai_name")
    id = request.POST.get("id")
    create = models.AIStrategy.objects.create(user_id=int(id), code=ai_name)

    dirPath = MEDIA_URL + 'ai_code/' + id + '/' + ai_name + '/'
    filePath = dirPath + ai_name + '.py'

    if os.path.exists('.' + filePath) == False:
        os.makedirs(dirPath[1:])
        os.makedirs(dirPath[1:] + 'model/')
        f = open('.' + filePath, mode='w', encoding="utf-8")

    return JsonResponse({
        'code': 1000
    })


@csrf_exempt
def get_ai_code(request):
    ai_name = request.POST.get("ai_name")
    user_id = request.POST.get("user_id")
    code = models.AIStrategy.objects.filter(user_id=int(user_id), code=ai_name)

    dirPath = MEDIA_URL + 'ai_code/' + user_id + '/' + ai_name + '/'
    filePath = dirPath + ai_name + '.py'
    content = ''

    with open('.'+filePath, 'r', encoding='utf-8') as f:
        content = f.read()

    return JsonResponse({
        'code': content
    })


@csrf_exempt
def quantitative_trading_ai(request):
    params = dict()
    content = request.POST.get("content")
    g = {'res1': ''}
    exec(content, g)
    return JsonResponse({
        'code': g['result']
    })
