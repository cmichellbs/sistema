from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from revcontract.models import Contract




def contracts(request, paginagion = 10):
    contracts = Contract.objects.all().order_by('pk')

    paginator = Paginator(contracts, paginagion)    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Contratos - ',
    }

    print(contracts)

    return render(request, 
                  'revcontrato/contracts_list.html',
                  context)
