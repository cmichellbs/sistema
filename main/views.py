from django.shortcuts import render
from .forms import DataFrameForm
from main.utils import ContractAlternatives
import pandas as pd
from .utils import convert_date_format
# Create your views here.


def homepage(request):
    return render(request, 'main/homepage.html')


def calculo_rapido(request):

    if request.method == 'POST':
        form = DataFrameForm(request.POST)
        if form.is_valid():
            months = form.cleaned_data['months']
            interest_rate = form.cleaned_data['interest_rate']
            loan_amount = form.cleaned_data['loan_amount']
            monthly_payment = form.cleaned_data['monthly_payment']
            date = form.cleaned_data['date']
            date = str(date)
            CODE = int(str(form.cleaned_data['bcb_code']).split()[0])
            contract = ContractAlternatives(
                months, interest_rate, loan_amount, monthly_payment, CODE,date)
            print(date)
            df = contract.resume_table()
            df = df.to_html(classes='table table-striped table-hover', index=False, border=0, justify='center')
            context = {
                # 'form': form,
                'df': df,
            }
            return render(request, 'main/calculo-rapido-result.html', context)
    context = {
        'form': DataFrameForm(),
        # 'df_price': pd.DataFrame(),
    }

    return render(request, 'main/calculo-rapido-form.html', context)
