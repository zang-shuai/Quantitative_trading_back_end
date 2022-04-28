from django.db import models


class UserInfo(models.Model):
    user_type_choices = (
        (1, '普通用户'),
        (2, '中级用户'),
        (3, '高级用户'),
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=64)
    img = models.CharField(max_length=128, default='')


class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


class UserSelect(models.Model):
    user = models.ForeignKey(to='UserInfo', on_delete=models.DO_NOTHING)
    # 自选
    ts_code = models.CharField(max_length=10)
