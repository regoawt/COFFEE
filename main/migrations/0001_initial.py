# Generated by Django 3.1.3 on 2020-12-16 22:17

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikertAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.answer')),
                ('answer', models.CharField(choices=[('strongly_agree', 'Strongly agree'), ('agree', 'Agree'), ('neutral', 'Neutral'), ('disagree', 'Disagree'), ('strongly_disagree', 'Strongly disagree')], max_length=20)),
            ],
            bases=('main.answer',),
        ),
        migrations.CreateModel(
            name='PlainTextAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.answer')),
                ('answer', models.CharField(max_length=500)),
            ],
            bases=('main.answer',),
        ),
        migrations.CreateModel(
            name='YesNoAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.answer')),
                ('answer', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=20)),
            ],
            bases=('main.answer',),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.TimeField(default=datetime.datetime(2020, 12, 16, 22, 17, 35, 563814, tzinfo=utc))),
                ('type', models.CharField(choices=[('lecture', 'Lecture'), ('small_group', 'Small group'), ('practical', 'Practical'), ('virtual', 'Virtual')], max_length=20)),
                ('additional_tutors', models.ManyToManyField(blank=True, null=True, related_name='additional_tutors', to=settings.AUTH_USER_MODEL)),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.questionnaire')),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tutor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('question_category', models.CharField(choices=[('likert', 'Likert'), ('yes_no', 'Yes/No'), ('plain_text', 'Plain text')], max_length=20)),
                ('questionnaire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.questionnaire')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]