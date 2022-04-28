"""Quantitative_trading_back_end URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

# from api.views import AuthView
# from api.views.KImage import get_k_image
from Quantitative_trading_back_end import settings
from api.views.AuthView import AuthView
from api.views.KImage import get_k_image
from api.views.GetStock import *
from api.views.Trading import quantitative_trading_img
from api.views.data import get_daily
from api.views.others import count
from api.views.stock_pool import *
from api.views.user import modify_user_information, user_register
from django.views.static import serve

urlpatterns = [

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    path('admin/', admin.site.urls),
    path('login', AuthView.as_view()),
    path('register', user_register),
    path('loginByToken', AuthView.as_view()),
    path('get_k_image', get_k_image),
    path('get_concepts', get_concepts),
    path('stock_basic', stock_basic),
    path('get_daily', get_daily),
    path('modify_user_information', modify_user_information),
    path('count', count),
    path('getHs300', getHs300),
    path('getMySelect', getMySelect),
    path('plate', plate),
    path('smallMoney', smallMoney),
    path('allstock', allstock),
    path('quantitative_trading_img', quantitative_trading_img),
    # path('api/login', AuthView.as_view()),
]
