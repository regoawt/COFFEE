# Generated by Django 3.1.3 on 2020-12-26 19:47

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0017_auto_20201224_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='attendees',
            field=models.ManyToManyField(blank=True, related_name='attendees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='session',
            name='submitted_questionnaire',
            field=models.ManyToManyField(blank=True, related_name='submitted_questionnaire', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='session',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 26, 20, 47, 25, 426665, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 26, 19, 47, 25, 426618, tzinfo=utc)),
        ),
    ]