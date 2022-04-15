from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from api import models


class FirstAuthtication(BaseAuthentication):
    def authenticate(self, request):
        pass

    def authenticate_header(self, request):
        pass


class Authtication(BaseAuthentication):
    def authenticate(self, request):
        # request.user.user_type
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        pass
