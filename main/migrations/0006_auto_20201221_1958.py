# Generated by Django 3.1.3 on 2020-12-21 19:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20201221_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likertanswer',
            name='answer',
            field=models.IntegerField(choices=[(1, 'Strongly agree'), (2, 'Agree'), (3, 'Neutral'), (4, 'Disagree'), (5, 'Strongly disagree')], max_length=2),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.TimeField(default=datetime.datetime(2020, 12, 21, 19, 58, 54, 520771, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='yesnoanswer',
            name='answer',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], max_length=2),
        ),
    ]
