from django.db import models
from django.contrib.auth.models import User,Group,Permission
from django.utils import timezone, text


class Questionnaire(models.Model):
    '''Aggregate questions into a unit that can be used for many sessions.'''

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name)
        super(Questionnaire, self).save(*args, **kwargs)

class Question(models.Model):

    CATEGORY_CHOICES = (('likert','Likert'),
                        ('yes_no','Yes/No'),
                        ('plain_text','Plain text'))

    question = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    question_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    questionnaire = models.ManyToManyField(Questionnaire)


    def __str__(self):
        return self.question

# TODO: Add file upload field
# TODO: Add session end time
class Session(models.Model):

    TYPE_CHOICES = ((1,'Lecture'),
                    (2,'Small group'),
                    (3,'Practical'),
                    (4,'Virtual'))

    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now())
    type = models.IntegerField(choices=TYPE_CHOICES)
    tutor = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True, related_name='tutor')
    additional_tutors = models.ManyToManyField(User, blank=True, related_name='additional_tutors')
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name+str(self.date))
        super(Session, self).save(*args, **kwargs)


class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.SET_NULL, blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        linked_session = self.session
        if linked_session is not None:
            string = self.session.name + ' - ' + self.question.question
        else:
            string = 'None' + ' - ' + self.question.question
        return string

class LikertAnswer(Answer):

    LIKERT_CHOICES = ((1,'Strongly agree'),
                        (2,'Agree'),
                        (3,'Neutral'),
                        (4,'Disagree'),
                        (5,'Strongly disagree'))

    answer = models.IntegerField(choices=LIKERT_CHOICES)


class YesNoAnswer(Answer):

    YESNO_CHOICES = ((1,'Yes'),
                        (0,'No'))

    answer = models.IntegerField(choices=YESNO_CHOICES)


class PlainTextAnswer(Answer):

    answer = models.CharField(max_length=500)
