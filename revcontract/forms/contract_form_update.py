from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from revcontract import models

class DateInput(forms.DateInput):
    input_type = 'date'

class ContractFormUpdate(forms.ModelForm):
    """This code block defines a Django form for creating a contract. The form contains the following fields:
    - contract_number: a CharField for the contract number
    - contract_name: a CharField for the contract name
    - contract_description: a CharField for the contract description
    - contract_start_date: a DateField for the contract start date
    - contract_end_date: a DateField for the contract end date
    - contract_value: a DecimalField for the contract value
    - contract_interest_rate: a DecimalField for the contract interest rate
    - contract_term: an IntegerField for the contract term
    - contract_term_unit: a ModelChoiceField for the contract term unit
    - contract_installment_value: a DecimalField for the contract installment value
    - contract_installment_number: an IntegerField for the contract installment number
    - contract_amortization_type: a ModelChoiceField for the contract amortization type
    - contract_installment_start_date: a DateField for the contract installment start date
    - contract_installment_end_date: a DateField for the contract installment end date
    - contract_customer: a ModelChoiceField for the contract customer
    - contract_bcb_sgs_code: a ModelChoiceField for the contract BCB SGS code
    - contract_amortization_system: a ModelChoiceField for the contract amortization system
    - contract_file: a FileField for the contract file

The fields are defined with their respective widgets and attributes, such as class, placeholder, and label. The form also defines a field_order list to specify the order of the fields in the form."""

    
    class Meta:
        model = models.Contract
       
        fields = [
        'contract_number',
        'contract_name',
        'contract_description',
        'contract_start_date',
        'contract_end_date',
        'contract_value',
        'contract_interest_rate',
        'contract_term',
        'contract_term_unit',
        'contract_installment_value',
        'contract_installment_number',
        'contract_amortization_type',
        'contract_installment_start_date', 
        'contract_installment_end_date',
        'contract_installment_end_date', 
        'contract_customer', 
        'contract_bcb_sgs_code', 
        'contract_amortization_system',
        'contract_file',
        ]

    contract_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'accept': '*',
                'class': 'form-control',
                'label': 'Arquivo do contrato',
                
            }
        ),
        label='Arquivo do contrato',
        required=False
    )
    contract_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Número do contrato',
                'label': 'Número do contrato',
            }
        ),
        label='Número do contrato',
        required=True
    )
    contract_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome do contrato',
                'label': 'Nome do contrato',
            }
        ),
        label='Nome do contrato',
        required=True   
    )
    contract_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do contrato',
                'label': 'Descrição do contrato',
            }
        ),
        label='Descrição do contrato',
        required=False
    )
    contract_start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Data de início do contrato',
                'type': 'text',
                'label': 'Data de início do contrato',
            }
        ),
        label='Data de início do contrato',
        required=True
    )
    contract_amortization_type = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'placeholder': 'Tipo de amortização',
                'label': 'Tipo de amortização',
            }
        ),
        queryset=models.AmortizationType.objects.all(),
        label='Tipo de amortização',
        required=True
    )
    contract_interest_rate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0,10 = 10%',
                'label': 'Taxa de juros',
            }
        ),
        label='Taxa de juros',
        required=True
    )
    contract_value = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Valor do contrato',
                'label': 'Valor do contrato',
            }
        ),
        label='Valor do contrato',
        required=True
    )
    contract_term = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Prazo do contrato',
                'label': 'Prazo do contrato',
                

            }
        ),
        label='Prazo do contrato',
        required=True
    )
    contract_term_unit = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'placeholder': 'Unidade de prazo',
                'label': 'Unidade de prazo',
            }
        ),
        queryset=models.ContractTermUnit.objects.all(),
        label='Unidade de prazo',
        required=True
    )
    contract_end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Data de término do contrato',
                'type': 'text',
                'label': 'Data de término do contrato',
                
            },
        
        ),
        label='Data de término do contrato',
        required=True
    )
    
    contract_installment_value = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Valor da parcela',
                'label': 'Valor da parcela',
            }
        ),
        label='Valor da parcela',
        required=True
    )
    contract_installment_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Número de parcelas',
                'label': 'Número de parcelas',
            }
        ),
        label='Número de parcelas',
        required=True
    )
    contract_installment_start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Data de início das parcelas',
                'type': 'text',
                'label': 'Data de início das parcelas',

            }
        ),
        label='Data de início das parcelas',
        required=True
    )
    contract_installment_end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Data de término das parcelas',
                'type': 'text',
                'label': 'Data de término das parcelas',
            }
        ),
        label='Data de término das parcelas',
        required=True
    )
    
    contract_customer = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'placeholder': 'Cliente',
                'label': 'Cliente',
                
            }
        ),
        queryset=models.Customer.objects.all(),
        label='Cliente',
        required=True
    )
    contract_bcb_sgs_code = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Código SGS do BCB',
                'label': 'Código SGS do BCB',
            },
        ),
        label='Código SGS do BCB',
        required=False,
        queryset=models.BCBSGS.objects.all()
    )
    contract_amortization_system = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'placeholder': 'Sistema de amortização',
                'label': 'Sistema de amortização',
            }
        ),
        queryset=models.AmortizationSystem.objects.all(),
        label='Sistema de amortização',
        required=True
    )

    
        
    field_order = [
        'contract_number',
        'contract_name',
        'contract_description',
        'contract_start_date',
        'contract_end_date',
        'contract_value',
        'contract_interest_rate',
        'contract_term',
        'contract_term_unit',
        'contract_installment_value',
        'contract_installment_number',
        'contract_amortization_type',
        'contract_installment_start_date', 
        'contract_installment_end_date',
        'contract_customer', 
        'contract_bcb_sgs_code', 
        'contract_amortization_system',
        'contract_file',
    ]
        
   
