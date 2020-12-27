# Generated by Django 3.1.3 on 2020-12-27 17:45

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20201227_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 18, 45, 33, 222612, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='session',
            name='questionnaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.questionnaire'),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 17, 45, 33, 222567, tzinfo=utc)),
        ),
    ]