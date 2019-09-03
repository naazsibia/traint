from . import views
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView 

urlpatterns = [ 
    path("dress_list/", views.dress_list)
]