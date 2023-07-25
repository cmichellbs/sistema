from django.urls import path

from revcontract import views

app_name = 'revcontract'

urlpatterns = [
    path('contracts/', views.contracts, name='contracts'),
]
    