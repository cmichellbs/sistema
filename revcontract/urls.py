from django.urls import path

from revcontract import views
from .autocomplete import BCBSGSAutocomplete

app_name = 'revcontract'

urlpatterns = [
    path('bcb-autocomplete/', BCBSGSAutocomplete.as_view(), name='bcb-autocomplete'),
    path('contact/<int:contract_id>/update/', views.update, name='update'),
    path('contact/<int:contract_id>/revision/', views.revisional, name='contract-revision'),
    path('contact/<int:contract_id>/', views.contract, name='contract'),
    path('contracts/', views.contracts, name='contracts'),
    path('contracts/create/', views.create, name='create'),
]
    