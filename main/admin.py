from django.contrib import admin
from .models import Question, Questionnaire, LikertAnswer, YesNoAnswer, PlainTextAnswer, Session

admin.site.register(Question)
admin.site.register(Questionnaire)
admin.site.register(LikertAnswer)
admin.site.register(YesNoAnswer)
admin.site.register(PlainTextAnswer)
admin.site.register(Session)

# TODO: Register other models
