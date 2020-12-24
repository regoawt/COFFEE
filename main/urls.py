from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('select_group/', views.select_group, name='select_group'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('create_questionnaire/', views.create_questionnaire, name='create_questionnaire'),
    path('questionnaire/<tutor>/<slug:session_slug>/<slug:questionnaire_slug>/', views.questionnaire, name='questionnaire'),
    path('create_session/', views.create_session, name='create_session')
]

# Media files in dev server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
