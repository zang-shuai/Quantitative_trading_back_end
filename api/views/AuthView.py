from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
# from api.utils.permission import SVIPPermission
# from api.utils.permission import MyPermission1
# from api.utils.throttle import VisitThrottle
from api import models

# Create your views here.
from rest_framework.views import APIView

from api.utils.auth import Authtication
from api.utils.encrypt import create_token


class AuthView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            phone_number = request._request.POST.get('phone_number')
            pwd = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(phone_number=phone_number, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            token = create_token(phone_number)
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['id'] = obj.id
            ret['token'] = token
            ret['role'] = obj.user_type
            ret['password'] = obj.password
            ret['username'] = obj.username
            ret['phone_number'] = obj.phone_number
            ret['img'] = obj.img
            request.session['user_id'] = obj.id
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            token = request._request.GET.get('token')
            user_id = models.UserToken.objects.filter(token=token).first().user_id
            obj = models.UserInfo.objects.filter(id=user_id).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            ret['token'] = token
            ret['role'] = obj.user_type
            ret['username'] = obj.username
            ret['password'] = obj.password
            ret['phone_number'] = obj.phone_number
            ret['img'] = obj.img
            ret['id'] = obj.id
            request.session['user_id'] = obj.id
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)
