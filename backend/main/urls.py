from django.urls import path
from . import views
from .views import test_api

urlpatterns =[ 
               path ('api/test/', test_api, name='test_api'),
               path ('', views.index, name='index'),]