from . import views
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView 

urlpatterns = [ 
    path("dress_list/", views.dress_list), url(r'^dress/(?P<dress_id>[0-9]+)/$', views.dress_detail, name='dress_detail'),
]