# Generated by Django 4.0 on 2022-04-20 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_userselect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userselect',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.userinfo'),
        ),
    ]