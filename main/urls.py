from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('group_selection', views.group_selection, name='group_selection'),
    path('login', views.login_request, name='login'),
    path('generate_questionnaire', views.generate_questionnaire, name='generate_questionnaire')
]
