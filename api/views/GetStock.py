from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from api import models
import tushare as ts
# Create your views here.
from rest_framework.views import APIView

from api.utils.auth import Authtication
from api.utils.encrypt import create_token
import numpy as np

pro = ts.pro_api()


def get_concepts(request):
    # pro = ts.pro_api()
    df = pro.concept()
    n = np.array(df.get(['code', 'name', 'src'])).tolist()

    return JsonResponse({
        'data': n
    })


def stock_basic(request):
    df = pro.stock_basic(exchange='', list_status='L',
                         fields='ts_code, symbol, name, area, industry, fullname, enname, cnspell, market, exchange,curr_type, list_status, list_date, delist_date, is_hs')
    n = np.array(df.get(
        ['ts_code', 'symbol', 'name', 'area', 'industry', 'fullname', 'enname', 'cnspell', 'market', 'exchange',
         'curr_type', 'list_status', 'list_date', 'delist_date', 'is_hs'])).tolist()
    return JsonResponse({
        'data': n
    })
