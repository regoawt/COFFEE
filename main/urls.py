from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='views'),
    path('register', views.register, name='register'),
    path('group_selection', views.group_selection, name='group_selection'),
]
