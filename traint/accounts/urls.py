# credits: https://wsvincent.com/django-user-authentication-tutorial-signup/
from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]
