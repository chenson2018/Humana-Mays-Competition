from django.urls import path

from . import views

urlpatterns = [
    path('', views.patient3, name='patient3'),
]