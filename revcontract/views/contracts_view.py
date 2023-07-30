from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from revcontract.models import Contract




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
