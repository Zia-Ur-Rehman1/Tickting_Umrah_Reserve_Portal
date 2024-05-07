from django.shortcuts import render, redirect, get_object_or_404
from .forms import  BankForm
from .models import Bank,Ledger
from django.db.models import Prefetch


def banks(request):
    banks = Bank.objects.filter(user=request.user).all()
    return render(request, 'banks.html', {'banks': banks})
def bank_create(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('banks')
    else:
        form = BankForm(user=request.user)
    return render(request, 'partials/bank_form.html', {'form': form})

def bank_update(request, pk):
    bank = get_object_or_404(Bank, pk=pk)
    if request.method == 'POST':
        form = BankForm(request.POST, instance=bank)
        if form.is_valid():
            return redirect('banks')
    else:
        form = Bank(instance=Bank)
    return render(request, 'partials/bank_form.html', {'form': form})

