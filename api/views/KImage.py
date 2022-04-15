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

from api.utils.stock import Stock
from api.utils.auth import Authtication
from api.utils.encrypt import create_token


def get_k_image(request):
    s1 = Stock(request.GET.get('stock_code'), start_date=request.GET.get('start_day'))
    l = s1.get_k_image()[::-1]
    return JsonResponse({
        'data': l
    })
