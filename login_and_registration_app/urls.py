from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process_registration', views.registration),
    path('process_login', views.login),
    path('end_session', views.endSession),
    path('check_email_exist', views.check_email_exists, name="check_email_exists"),
]