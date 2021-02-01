from django.contrib import admin
from .models import Question, Questionnaire, LikertAnswer, YesNoAnswer, PlainTextAnswer, Session, Resource

# TODO: Show linked quetions under questionnaire in Admin
# TODO: Admin action to change users' default questionnaire when updated

admin.site.register(Question)
admin.site.register(Questionnaire)
admin.site.register(LikertAnswer)
admin.site.register(YesNoAnswer)
admin.site.register(PlainTextAnswer)

class ResourceAdmin(admin.StackedInline):
    model = Resource

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    inlines = [ResourceAdmin]

    class Meta:
       model = Session

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass
