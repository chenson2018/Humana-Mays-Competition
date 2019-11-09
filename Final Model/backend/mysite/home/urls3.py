from django.urls import path

from . import views

urlpatterns = [
    path('', views.patient2, name='patient2'),
]