from django import forms
from revcontract.models import BCBSGS

class DataFrameForm(forms.Form):
    months = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nr. de meses',
            'min': 1,}
            ),
        label='Nr. de Meses', 
        min_value=1, 
        )
    interest_rate = forms.FloatField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Taxa de juros mensal',
            'min': 0,}
            ),
        label='Taxa de Juros Mensal',
        min_value=0,
        )
    loan_amount = forms.FloatField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Valor do empréstimo',
            'min': 0,}
            ),
        label='Valor do Empréstimo',
        min_value=0,
        )
    monthly_payment = forms.FloatField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Valor da parcela',
            'min': 0,}
            ),
        label='Valor da Parcela',
        min_value=0,
        )
    bcb_code = forms.ModelChoiceField(
        queryset=BCBSGS.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Código BCB',
            'min': 0,}
            ),
        label='Código BCB',
        )
    date = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'dd/mm/aaaa',
            'type':'date',
            }
            ),
        label='Data do contrato',
        )


    