from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('select_group', views.select_group, name='select_group'),
    path('login', views.login_request, name='login'),
    path('create_questionnaire', views.create_questionnaire, name='create_questionnaire'),
    path('questionnaire', views.questionnaire, name='questionnaire'),
    path('create_session', views.create_session, name='create_session')
]
