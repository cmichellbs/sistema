from django.contrib import admin
from . import models

@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number','contract_name','contract_description','contract_start_date','amortization_type','interest_rate','contract_value','contract_file','contract_term','contract_term_unit','contract_end_date','contract_status','contract_created_at','contract_updated_at','contract_installment_value','contract_installment_number','contract_installment_start_date','contract_installment_end_date','contract_owner','contract_created_by','contract_customer','contract_bcb_sgs_code',)
    list_filter = ('contract_number','contract_name','contract_description','contract_start_date','amortization_type','interest_rate','contract_value','contract_file','contract_term','contract_term_unit','contract_end_date','contract_status','contract_created_at','contract_updated_at','contract_installment_value','contract_installment_number','contract_installment_start_date','contract_installment_end_date','contract_owner','contract_bcb_sgs_code',)
    
    search_fields = ('contract_number','contract_name','contract_description','contract_start_date','interest_rate','contract_value','contract_file','contract_term','contract_end_date','contract_status','contract_created_at','contract_updated_at','contract_installment_value','contract_installment_number','contract_installment_start_date','contract_installment_end_date','contract_bcb_sgs_code',)
    
    list_per_page = 25
    ordering = ('contract_number','contract_name','contract_description','contract_start_date','amortization_type','interest_rate','contract_value','contract_file','contract_term','contract_term_unit','contract_end_date','contract_status','contract_created_at','contract_updated_at','contract_installment_value','contract_installment_number','contract_installment_start_date','contract_installment_end_date','contract_owner','contract_created_by','contract_customer','contract_bcb_sgs_code',)
    date_hierarchy = 'contract_start_date'
    list_max_show_all = 100
@admin.register(models.AmortizationType)
class AmortizationTypeAdmin(admin.ModelAdmin):
    list_display = ('amortization_type','amortization_type_description',)
    list_filter = ('amortization_type','amortization_type_description',)
    search_fields = ('amortization_type','amortization_type_description',)
    list_per_page = 25
    ordering = ('amortization_type','amortization_type_description',)
    list_max_show_all = 100
@admin.register(models.AmortizationSystem)
class AmortizationSystemAdmin(admin.ModelAdmin):
    list_display = ('amortization_system','amortization_system_description',)
    list_filter = ('amortization_system','amortization_system_description',)
    search_fields = ('amortization_system','amortization_system_description',)
    list_per_page = 25
    ordering = ('amortization_system','amortization_system_description',)
    list_max_show_all = 100
@admin.register(models.ContractTermUnit)
class ContractTermUnitAdmin(admin.ModelAdmin):
    list_display = ('contract_term_unit','contract_term_unit_description',)
    list_filter = ('contract_term_unit','contract_term_unit_description',)
    search_fields = ('contract_term_unit','contract_term_unit_description',)
    list_per_page = 25
    ordering = ('contract_term_unit','contract_term_unit_description',)
    list_max_show_all = 100


