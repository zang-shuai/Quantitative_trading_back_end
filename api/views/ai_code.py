import datetime
import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from Quantitative_trading_back_end.settings import MEDIA_URL
from api import models
from api.models import UserInfo
from api.utils.encrypt import create_token
from api.utils.trade.stock_utils import get_concept_detail
from api.utils.trade.trade_utils import *
from api.utils.trade.user_utils import User


@csrf_exempt
def save_ai_code(request):
    ai_name = request.POST.get("ai_name")
    user_id = request.POST.get("user_id")
    new_code = request.POST.get("new_code")
    code = models.AIStrategy.objects.filter(user_id=int(user_id), code=ai_name)

    dirPath = MEDIA_URL + 'ai_code/' + user_id + '/' + ai_name + '/'
    filePath = dirPath + ai_name + '.py'

    with open('.' + filePath, 'w') as f:
        f.write(new_code)
    f.close()
    return JsonResponse({
        'code': 1000
    })


@csrf_exempt
def run_ai_code(request):
    user_id = request.POST.get("user_id")
    ai_code = request.POST.get("ai_code")
    g = {'res1': None, 'res2': None}
    exec(ai_code, g)
    return JsonResponse({
        'code': g['res1'],
        'summary': g['res2']
    })


@csrf_exempt
def stop_ai_code(request):
    pass


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
    if os.path.exists(path):
        os.removedirs(path)  # 递归删除目录下面的空文件夹


@csrf_exempt
def delete_ai_code(request):
    ai_name = request.POST.get("ai_name")
    user_id = request.POST.get("user_id")
    dirPath = MEDIA_URL + 'ai_code/' + user_id + '/' + ai_name
    del_file('.' + dirPath)
    models.AIStrategy.objects.filter(user_id=int(user_id), code=ai_name).delete()
    return JsonResponse({
        'code': 1000
    })
    # return redirect('http://127.0.0.1:8080/#/ailab')
