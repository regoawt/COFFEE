# Utility functions called in app
from .models import Questionnaire, Question

def is_group(user, group):
    return user.groups.filter(name=group).exists()

def create_default_questionnaire(user):

    default_questionnaire = Questionnaire(name='Default questionnaire', user=user)
    default_questionnaire.save()

    question_list = [
                    ['The objectives for this session were identified and met.', 1],
                    ['The delivery of this session was effective and clear.', 1],
                    ['The correct level of background knowledge and experience was assumed for this session.', 1],
                    ['The session was delivered in an appropriate teaching environment.', 1],
                    ['Do you feel more confident on the subject?', 2],
                    ['What was done well in this session?', 3],
                    ['What could be improved in future sessions?', 3],
                    ['Any other comments:', 3]
                    ]

    for question in question_list:
        question_ = Question(question=question[0], user=user, question_category=question[1])
        question_.save()
        question_.questionnaire.add(default_questionnaire)
