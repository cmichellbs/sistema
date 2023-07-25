from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Userinfo(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile_pictures/%Y/%m/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Info'
        verbose_name_plural = 'User Info'
                    

    
    def __str__(self):
        return self.first_name + ' ' + self.last_name