from django.db import models
from django.contrib.auth.models import User,Group,Permission
from django.utils import timezone, text
import random
import string

# FIXME: Save method slugify changing on every save due to random
# TODO: Add attendees M2M in Session

class Questionnaire(models.Model):
    '''Aggregate questions into a unit that can be used for many sessions.'''

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    # Overwrite save method for dynamic slug assignment
    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name+'-'+''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
        super(Questionnaire, self).save(*args, **kwargs)

class Question(models.Model):
    '''Base question class'''

    CATEGORY_CHOICES = ((1,'Likert'),
                        (2,'Yes/No'),
                        (3,'Plain text'))

    question = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    question_category = models.IntegerField(choices=CATEGORY_CHOICES)
    questionnaire = models.ManyToManyField(Questionnaire)


    def __str__(self):
        return self.question


class Session(models.Model):
    '''Base session class'''

    TYPE_CHOICES = ((1,'Lecture'),
                    (2,'Small group'),
                    (3,'Practical'),
                    (4,'Virtual'))

    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField(default=timezone.now())
    end_datetime = models.DateTimeField(default=timezone.now()+timezone.timedelta(hours=1))
    type = models.IntegerField(choices=TYPE_CHOICES)
    tutor = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True, related_name='tutor')
    additional_tutors = models.ManyToManyField(User, blank=True, related_name='additional_tutors')
    questionnaire = models.ForeignKey(Questionnaire, null=True, on_delete=models.SET_NULL)
    attendees = models.ManyToManyField(User, blank=True, related_name='attendees')
    submitted_questionnaire = models.ManyToManyField(User, blank=True, related_name='submitted_questionnaire')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    # Overwrite save method for dynamic slug assignment
    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name+'-'+''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
        super(Session, self).save(*args, **kwargs)


class Resource(models.Model):
    '''Resource class'''
    # https://soshace.com/upload-multiple-images-to-a-django-model-without-plugins/

    # Callable func for upload_to attr of resources field
    def resources_folder(instance, filename):
         return 'resources/{0}/{1}'.format(str(instance.session), str(instance.file))

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    file = models.FileField(upload_to=resources_folder)

    def __str__(self):
        return str(self.file)


class Answer(models.Model):
    '''Base answer class'''

    question = models.ForeignKey(Question, on_delete=models.SET_NULL, blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    # Prepend answer str with session if available to make easier browsing in admin
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
