# Generated by Django 4.0 on 2022-04-20 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userinfo_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSelect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_code', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo')),
            ],
        ),
    ]
