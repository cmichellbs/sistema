from django.contrib import admin
from . import models

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','address','city','state','zipcode','country','image','created_at','updated_at','blocked','cpf_cnpj',]
    list_filter = ['name','email','phone','address','city','state','zipcode','country','image','created_at','updated_at','blocked','cpf_cnpj',]
    search_fields = ['name','email','phone','address','city','state','zipcode','country','image','created_at','updated_at','blocked','cpf_cnpj',]
    list_per_page = 10



