from django.db import models
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from customer.models import Customer
from django.utils import timezone
import pandas as pd
import sgs
import requests
import datetime as dt
from main.utils import convert_date_format

# Create your models here.


class AmortizationType (models.Model):
    amortization_type = models.CharField(max_length=50,null=False,blank=False,verbose_name='Tipo de amortização',help_text='Tipo de amortização',)
    amortization_type_description = models.CharField(max_length=500,null=False,blank=False,verbose_name='Descrição do tipo de amortização',help_text='Descrição do tipo de amortização',)

    class Meta:
        verbose_name = 'Tipo de amortização'
        verbose_name_plural = 'Tipos de amortização'

    def __str__(self):
        return self.amortization_type


class AmortizationSystem (models.Model):
    amortization_system = models.CharField(max_length=300,null=False,blank=False,verbose_name='Sistema de amortização',help_text='Sistema de amortização',)
    amortization_system_description = models.CharField(max_length=50,null=False,blank=False,verbose_name='Descrição do sistema de amortização',help_text='Descrição do sistema de amortização',)

    class Meta:
        verbose_name = 'Sistema de amortização'
        verbose_name_plural = 'Sistemas de amortização'

    def __str__(self):
        return self.amortization_system


class ContractTermUnit (models.Model):
    contract_term_unit = models.CharField(max_length=1, null=False, blank=False, verbose_name='Unidade de prazo do contrato', help_text='Unidade de prazo do contrato', )
    contract_term_unit_description = models.CharField(max_length=50,null=False,blank=False,verbose_name='Descrição da unidade de prazo do contrato',help_text='Descrição da unidade de prazo do contrato',)

    class Meta:
        verbose_name = 'Unidade de prazo do contrato'
        verbose_name_plural = 'Unidades de prazo do contrato'

    def __str__(self):
        return self.contract_term_unit

class BCBSGS (models.Model):
    code = models.IntegerField(null=False,blank=False,verbose_name='Código BCB SGS',help_text='Código BCB SGS',unique=True,primary_key=True)
    name = models.CharField(max_length=300,null=False,blank=False,verbose_name='Nome do indicador',help_text='Nome do indicador',)
    unit = models.CharField(max_length=300,null=False,blank=False,verbose_name='Unidade do indicador',help_text='Unidade do indicador',)
    frequency = models.CharField(max_length=300,null=False,blank=False,verbose_name='Frequência do indicador',help_text='Frequência do indicador',)
    start_date = models.DateField(null=False,blank=False,verbose_name='Data de início do indicador',help_text='Data de início do indicador',)
    end_date = models.DateField(null=False,blank=False,verbose_name='Data de término do indicador',help_text='Data de término do indicador',)
    source = models.CharField(max_length=300,null=False,blank=False,verbose_name='Fonte do indicador',help_text='Fonte do indicador',)

    class Meta:
        verbose_name = 'Indicador BCB SGS'
        verbose_name_plural = 'Indicadores BCB SGS'

    def __str__(self):
        return f'{self.code} - {self.name}'
    
    

class Contract (models.Model):
    contract_number = models.CharField(max_length=300,null=True,blank=True,verbose_name='Número de contrato',help_text='Número de contrato',)
    contract_name = models.CharField(max_length=300,null=False,blank=False,verbose_name='Nome do contrato',help_text='Nome do contrato',)
    contract_description = models.TextField(max_length=300,blank=True,verbose_name='Descrição do contrato',help_text='Descrição do contrato',)
    contract_start_date = models.DateField(null=False,blank=False,verbose_name='Data de início do contrato',help_text='Data de início do contrato',)
    contract_amortization_type = models.ForeignKey(AmortizationType,verbose_name="Tipo de amortização",on_delete=models.SET_NULL,null=True,blank=True,help_text='Tipo de amortização',)
    contract_interest_rate = models.FloatField(null=False,blank=False,verbose_name='Taxa de juros do contrato',help_text='Taxa de juros do contrato',)
    contract_value = models.DecimalField(max_digits=20,decimal_places=2,null=False,blank=False,verbose_name='Valor do contrato',help_text='Valor do contrato',)
    contract_file = models.FileField(upload_to='documents/%Y/%m/%d/',null=True,blank=True,verbose_name='Arquivo do contrato',help_text='Arquivo do contrato',)
    contract_term = models.IntegerField(null=False,blank=False,verbose_name='Prazo do contrato',help_text='Prazo do contrato',)
    contract_term_unit = models.ForeignKey(ContractTermUnit,verbose_name="Unidade de prazo do contrato",on_delete=models.SET_NULL,null=True,blank=True,help_text='Unidade de prazo do contrato',)
    contract_end_date = models.DateField(null=True,blank=True,verbose_name='Data de término do contrato',help_text='Data de término do contrato',)
    contract_status = models.BooleanField(default=True,verbose_name='Status do contrato',help_text='Status do contrato',)
    contract_created_at = models.DateTimeField(auto_now_add=True,verbose_name='Data de criação do contrato',help_text='Data de criação do contrato',)
    contract_updated_at = models.DateTimeField(auto_now=True,verbose_name='Data de atualização do contrato',help_text='Data de atualização do contrato',)
    contract_installment_value = models.DecimalField(max_digits=20,decimal_places=2,null=False,blank=False,verbose_name='Valor da parcela',help_text='Valor da parcela',)
    contract_installment_number = models.IntegerField(null=False,blank=False,verbose_name='Número de parcelas',help_text='Número de parcelas',)
    contract_installment_start_date = models.DateField(null=False,blank=False,verbose_name='Data de início das parcelas',help_text='Data de início das parcelas',)
    contract_installment_end_date = models.DateField(null=False,blank=False,verbose_name='Data de término das parcelas',help_text='Data de término das parcelas',)    
    contract_owner = models.ForeignKey(User,related_name='contract_owner',verbose_name="Dono do contrato",on_delete=models.SET_NULL,null=True,blank=True,help_text='Dono do contrato',)
    contract_created_by = models.ForeignKey(User,related_name='contract_created_by',verbose_name="Criado por",on_delete=models.SET_NULL,null=True,blank=True,help_text='Criado por',)
    contract_customer = models.ForeignKey(Customer,verbose_name="Cliente",on_delete=models.SET_NULL,null=True,blank=True,help_text='Cliente',)
    contract_bcb_sgs_code = models.ForeignKey(BCBSGS,verbose_name="Código BCB SGS",to_field='code',on_delete=models.SET_NULL,null=True,blank=True,help_text='Código BCB SGS')
    contract_amortization_system = models.ForeignKey(AmortizationSystem,verbose_name="Sistema de amortização",on_delete=models.SET_NULL,null=True,blank=True,help_text='Sistema de amortização',)
    contract_abusive = models.BooleanField(default=False,verbose_name='Contrato abusivo',help_text='Contrato abusivo',)
    contract_super_abusive = models.BooleanField(default=False,verbose_name='Contrato super abusivo',help_text='Contrato super abusivo',)
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

    def __str__(self):
        return self.contract_name
    
    def get_bcb_sgs(self):
        return BCBSGS.objects.get(code=self.contract_bcb_sgs_code.code)
    
    def get_bcb_sgs_interest(self):
        start = self.contract_start_date.replace(day=1)
        start = str(start)
        start = convert_date_format(start)
        ts = sgs.time_serie(self.contract_bcb_sgs_code.code, start=start, end=start)
        df = pd.DataFrame(ts)
       
        
        if df.empty:
            ts = sgs.time_serie(self.contract_bcb_sgs_code.code, start='01/01/1900', end='31/12/3000')
            df = pd.DataFrame(ts)
            df = df.tail(3)
            avg = df[self.contract_bcb_sgs_code.code].sum() / 3
            return avg
        else:
            return df[self.contract_bcb_sgs_code.code].sum()
        
    def save(self, *args, **kwargs):
        if self.contract_term_unit == 'M' and self.contract_term > 0 and self.contract_start_date is not None and self.contract_end_date is None:
            self.contract_end_date = self.contract_start_date + \
                timedelta(months=self.contract_term)
        elif self.contract_term_unit == 'A' and self.contract_term > 0 and self.contract_start_date is not None and self.contract_end_date is None:
            self.contract_end_date = self.contract_start_date + \
                timedelta(years=self.contract_term)
        
        if self.contract_term_unit == 'M' and self.contract_installment_number > 0 and self.contract_installment_start_date is not None and self.contract_installment_end_date is None:
            self.contract_installment_end_date = self.contract_installment_start_date + \
                timedelta(months=self.contract_installment_number)
        elif self.contract_term_unit == 'A' and self.contract_installment_number > 0 and self.contract_installment_start_date is not None and self.contract_installment_end_date is None:
            self.contract_installment_end_date = self.contract_installment_start_date + \
                timedelta(years=self.contract_installment_number)
        
        if self.contract_interest_rate >= self.get_bcb_sgs_interest()*1.1:
            self.contract_abusive = True
        elif self.contract_interest_rate >= self.get_bcb_sgs_interest()*1.5:
            self.contract_super_abusive = True
        else:
            self.contract_abusive = False
            self.contract_super_abusive = False
        super(Contract, self).save(*args, **kwargs) 
            

