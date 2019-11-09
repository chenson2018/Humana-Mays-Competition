from django.urls import path

from . import views

urlpatterns = [
    path('', views.patient1, name='patient1'),
]