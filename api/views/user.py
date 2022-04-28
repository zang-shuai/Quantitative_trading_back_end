import datetime
import os
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from Quantitative_trading_back_end.settings import MEDIA_URL
from api.models import UserInfo
from api.utils.encrypt import create_token


@csrf_exempt
def modify_user_information(request):
    file = request.FILES.get('file')
    params = {}
    if file:
        filePath = MEDIA_URL + 'images/userImg/' + create_token(file.name) + '.' + file.name.split('.')[-1]
        f = open('.' + filePath, mode='wb')
        for chunk in file.chunks():
            f.write(chunk)
        params['img'] = filePath
    p = ['user_type', 'username', 'phone_number', 'password']
    for col in p:
        if request.POST.get(col):
            params[col] = request.POST.get(col)

    UserInfo.objects.filter(id=int(request.session.get('user_id'))).update(**params)
    return redirect('http://127.0.0.1:8080/#/user_detail')


@csrf_exempt
def user_register(request):
    password = request.POST.get('password')
    phone_number = request.POST.get('phone_number')
    users = UserInfo.objects.filter(phone_number=phone_number)
    res = {'code': 1000}
    if len(users) == 0:
        UserInfo.objects.create(phone_number=phone_number, password=password, user_type=1)
        return JsonResponse(res)
    else:
        res['code'] = 0
        return JsonResponse(res)
