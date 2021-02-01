# Utility functions called in app
from .models import Questionnaire, Question
from django.conf import settings

def is_group(user, group):
    return user.groups.filter(name=group).exists()

def get_domain():
    if settings.DEBUG:
        return 'http://192.168.1.123'
    else:
        return'http://www.hone-app.co.uk'

def create_default_questionnaire(user):

    default_questionnaire = Questionnaire(name='Default questionnaire', user=user)
    default_questionnaire.save()

    question_list = [
                    ['How well were the objectives of this session met?', 4],
                    ['Please rate your knowledge before the session.', 4],
                    ['Please rate your knowledge after the session.',4],
                    ['Please rate the presentation skills of the instructor.', 4],
                    ["Please rate the instructor's knowledge of the subject.", 4],
                    ['The session was delivered at the appropriate level.', 1],
                    ['The session was delivered in the appropriate teaching environment.', 1],
                    ['What was done well in this session?', 3],
                    ['What could be improved in future sessions?', 3],
                    ['Any other comments:', 3]
                    ]

    for question in question_list:
        question_ = Question(question=question[0], user=user, question_category=question[1])
        question_.save()
        question_.questionnaire.add(default_questionnaire)
