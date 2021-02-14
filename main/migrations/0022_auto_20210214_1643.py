# Generated by Django 3.1.3 on 2021-02-14 16:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20210127_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likertanswer',
            name='answer',
            field=models.IntegerField(choices=[(1, 'Strongly disagree'), (2, 'Disagree'), (3, 'Neutral'), (4, 'Agree'), (5, 'Strongly agree')]),
        ),
        migrations.AlterField(
            model_name='plaintextanswer',
            name='answer',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='session',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 17, 43, 7, 179191, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 16, 43, 7, 179153, tzinfo=utc)),
        ),
    ]
