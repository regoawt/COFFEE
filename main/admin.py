from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Question, Questionnaire, LikertAnswer, YesNoAnswer, PlainTextAnswer, Session, Resource, FiveScaleAnswer
from .utils import Utils

# TODO: Show linked questions under questionnaire in Admin
# FIXME: AA - update_default_questionnaire instead of delete, change old default name e.g 'Default questionnaire (archived - *date*)'

def update_default_questionnaire(modeladmin,request,queryset):
    for user in queryset:
        if Utils.is_group(user,'Tutors'):

            old_questionnaire = Questionnaire.objects.get(name='Default questionnaire',user=user)
            old_questionnaire.delete()

            default_questionnaire = Questionnaire(name='Default questionnaire', user=user)
            default_questionnaire.save()

            question_list = Utils.get_default_questionnaire()

            # FIXME: Should Question model have user attribute? All questions in default questionnaire will be
            # duplicated for every user. Do get or create first
            for question in question_list:
                question_ = Question(question=question[0], user=user, question_category=question[1])
                question_.save()
                question_.questionnaire.add(default_questionnaire)

admin.site.register(Question)
admin.site.register(Questionnaire)
admin.site.register(LikertAnswer)
admin.site.register(YesNoAnswer)
admin.site.register(PlainTextAnswer)
admin.site.register(FiveScaleAnswer)

class CustomUserAdmin(UserAdmin):
    actions = [update_default_questionnaire]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

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
