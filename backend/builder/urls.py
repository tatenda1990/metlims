from django.urls import path
from . import views

urlpatterns = [
    path('form/<int:form_id>/', views.get_form_definition, name='get_form_definition'),
    path('form/<int:form_id>/submit/', views.submit_form, name='submit_form'),
]
