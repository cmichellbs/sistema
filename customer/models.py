from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=50,verbose_name='Nome',help_text='Nome do cliente',blank=False,null=False)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    image = models.ImageField(upload_to='customer_pictures/%Y/%m/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blocked = models.BooleanField(default=False)
    cpf_cnpj = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def save(self, *args, **kwargs):
        self.cpf_cnpj = self.cpf_cnpj.replace('.','').replace('/','').replace('-','')
        super(Customer, self).save(*args, **kwargs)
    

                    

    def __str__(self):
        return self.name