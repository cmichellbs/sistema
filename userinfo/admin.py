from django.contrib import admin
from . import models

@admin.register(models.Userinfo)
class UserinfoAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','phone','address','city','state','zipcode','country','image','created_at','updated_at','user','blocked']
    list_filter = ['first_name','last_name','email','phone','address','city','state','zipcode','country','image','created_at','updated_at','user','blocked']
    search_fields = ['first_name','last_name','email','phone','address','city','state','zipcode','country','image','created_at','updated_at','user','blocked']
    list_per_page = 10
    





# Register your models here.

