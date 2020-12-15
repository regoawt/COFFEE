from django.db import models
from django.contrib.auth.models import User,Group,Permission
from django.utils import timezone

class Questionnaire(models.Model):

    name = models.CharField(max_length=100)
    num_questions = models.IntegerField()


class Question(models.Model):

    CATEGORY_CHOICES = (('likert','Likert'),
                        ('yes_no','Yes/No'),
                        ('plain_text','Plain text'))

    question = models.CharField(max_length=300)
    question_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.question

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, blank=True, null=True)


class LikertAnswer(Answer):

    LIKERT_CHOICES = (('strongly_agree','Strongly agree'),
                        ('agree','Agree'),
                        ('neutral','Neutral'),
                        ('disagree','Disagree'),
                        ('strongly_disagree','Strongly disagree'))

    answer = models.CharField(max_length=20, choices=LIKERT_CHOICES)


class YesNoAnswer(Answer):

    YESNO_CHOICES = (('yes','Yes'),
                        ('no','No'))

    answer = models.CharField(max_length=20, choices=YESNO_CHOICES)


class PlainTextAnswer(Answer):

    answer = models.CharField(max_length=500)


class Session(models.Model):

    TYPE_CHOICES = (('lecture','Lecture'),
                    ('small_group','Small group'),
                    ('practical','Practical'),
                    ('virtual','Virtual'))

    name = models.CharField(max_length=100)
    date = models.TimeField(default=timezone.now())
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    tutor = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True, related_name='tutor')
    additional_tutors = models.ManyToManyField(User, blank=True, null=True, related_name='additional_tutors')
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
