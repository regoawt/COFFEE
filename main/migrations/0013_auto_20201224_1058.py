# Generated by Django 3.1.3 on 2020-12-24 10:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20201223_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='date',
        ),
        migrations.AddField(
            model_name='session',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 24, 11, 58, 1, 611790, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='session',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 24, 10, 58, 1, 611742, tzinfo=utc)),
        ),
    ]
