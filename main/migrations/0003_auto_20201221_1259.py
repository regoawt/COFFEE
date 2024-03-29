# Generated by Django 3.1.3 on 2020-12-21 12:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20201216_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='question',
            name='questionnaire',
        ),
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ManyToManyField(to='main.Questionnaire'),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.TimeField(default=datetime.datetime(2020, 12, 21, 12, 59, 33, 42064, tzinfo=utc)),
        ),
    ]
