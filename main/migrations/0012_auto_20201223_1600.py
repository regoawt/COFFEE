# Generated by Django 3.1.3 on 2020-12-23 16:00

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0011_auto_20201222_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likertanswer',
            name='answer',
            field=models.IntegerField(choices=[(1, 'Strongly agree'), (2, 'Agree'), (3, 'Neutral'), (4, 'Disagree'), (5, 'Strongly disagree')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='additional_tutors',
            field=models.ManyToManyField(blank=True, related_name='additional_tutors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 23, 16, 0, 15, 513205, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='yesnoanswer',
            name='answer',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No')]),
        ),
    ]
