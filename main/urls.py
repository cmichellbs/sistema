from django.urls import path
from django.contrib import admin

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('calculo-rapido/', views.calculo_rapido, name='calculo-rapido'),
]
    