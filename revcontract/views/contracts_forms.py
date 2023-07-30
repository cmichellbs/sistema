from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from revcontract.forms import ContractFormCreate, ContractFormUpdate
from revcontract.models import Contract
# homologar ferramenta de calculo de parcelas para ganhar muito dinheiro

def create(request):
    print(request.user)
    form_action = reverse('revcontract:create')

    if request.method == 'POST':
        form = ContractFormCreate(request.POST, request.FILES)
        
        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            contract = form.save(commit=False)
            contract.contract_owner = request.user
            contract.contract_created_by = request.user
            contract.save()
            return redirect('revcontract:contract', contract_id=contract.pk)

        return render(
            request,
            'revcontract/create.html',
            context
        )

    context = {
        'form': ContractFormCreate(),
        'form_action': form_action,
    }

    return render(
        request,
        'revcontract/create.html',
        context
    )

def update(request, contract_id):
    contract = get_object_or_404(
        Contract, pk=contract_id
    )
    form_action = reverse('revcontract:update', args=(contract_id,))

    if request.method == 'POST':
        form = ContractFormUpdate(request.POST, request.FILES, instance=contract)

                

        if form.is_valid():
            contract = form.save()
            return redirect('revcontract:contract', contract_id=contract.pk)

        return render(
            request,
            'revcontract/create.html',
            context
        )

    context = {
        'form': ContractFormUpdate(instance=contract),
        'form_action': form_action,
    }

    return render(
        request,
        'revcontract/create.html',
        context
    )