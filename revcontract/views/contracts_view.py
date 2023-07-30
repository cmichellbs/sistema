from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from revcontract.models import Contract
from main.utils import ContractAlternatives




def contracts(request):
    contracts = Contract.objects.all().order_by('pk')

    paginator = Paginator(contracts, 25)    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(request.user)
    context = {
        'page_obj': page_obj,
        'site_title': 'Contratos - ',
    }

    print(contracts)

    return render(request, 
                  'revcontract/contracts.html',
                  context)

def contract(request, contract_id):
    print(request.user)
    contract = get_object_or_404(Contract, pk=contract_id)
    context = {
        'contract': contract,
        'site_title': 'Contrato - ',
    }
    return render(request, 
                  'revcontract/contract.html',
                  context
                    )


def revisional(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    print(contract.contract_bcb_sgs_code)

    revision = ContractAlternatives(months = int(contract.contract_installment_number), 
                                    interest_rate=float(contract.contract_interest_rate)*100, 
                                    loan_amount = float(contract.contract_value), 
                                    monthly_payment = float(contract.contract_installment_value), 
                                    CODE = contract.contract_bcb_sgs_code.code, 
                                    date = str(contract.contract_start_date))
    
    df_price_bcb = revision.price_table(variant='bcb')
    df_price_bcb = df_price_bcb.to_html(classes='table table-striped table-hover', index=False, border=0, justify='center')
    df_price_effective = revision.price_table(variant='effective')
    df_price_effective = df_price_effective.to_html(classes='table table-striped table-hover', index=False, border=0, justify='center')
    df_price_nominal = revision.price_table(variant = 'nominal')
    df_price_nominal = df_price_nominal.to_html(classes='table table-striped table-hover', index=False, border=0, justify='center')

    df_sac_bcb = revision.sac_table(variant ='bcb')
    df_sac_bcb = df_sac_bcb.to_html(classes='table table-striped table-hover', index=False, border=0, justify='center')
    df_sac_effective = revision.sac_table(variant ='effective')
    df_sac_effective = df_sac_effective.to_html(classes='table table-striped table-hover', index=False, border=0, justify='center')
    df_sac_nominal = revision.sac_table(variant ='nominal')
    df_sac_nominal = df_sac_nominal.to_html(classes='table table-striped table-hover', index=False, border=0, justify='center')

    df_mejs_bcb = revision.mejs_table(variant ='bcb')
    df_mejs_bcb = df_mejs_bcb.to_html(classes='table table-striped table-hover', index=False, border=0, justify='center')
    df_mejs_effective = revision.mejs_table(variant ='effective')
    df_mejs_effective = df_mejs_effective.to_html(classes='table table-striped table-hover', index=False, border=0, justify='center')
    df_mejs_nominal = revision.mejs_table(variant ='nominal')
    df_mejs_nominal = df_mejs_nominal.to_html(classes='table table-striped table-hover', index=False, border=0, justify='center')




    context = {
        'contract': contract,
        'site_title': 'Contrato - ',
        'df_price_bcb': df_price_bcb,
        'df_price_effective': df_price_effective,
        'df_price_nominal': df_price_nominal,
        'df_sac_bcb': df_sac_bcb,
        'df_sac_effective': df_sac_effective,
        'df_sac_nominal': df_sac_nominal,
        'df_mejs_bcb': df_mejs_bcb,
        'df_mejs_effective': df_mejs_effective,
        'df_mejs_nominal': df_mejs_nominal,

    }
    return render(request, 
                  'revcontract/contract_revisional.html',
                  context
                    )
