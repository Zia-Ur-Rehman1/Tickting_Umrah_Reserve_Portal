from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Supplier, Ledger, Customer
from django.db.models import Sum, F, ExpressionWrapper, fields
from django.db.models.functions import Coalesce
from .forms import LedgerForm
import json

def ledger_list(request):
    data = json.loads(request.GET.get('data', '{}'))
    if 'sup' in data:
        ledgers= Ledger.objects.filter(supplier=data['sup'])
    elif 'cus' in data:
        ledgers= Ledger.objects.filter(customer=data['cus'])
    else:
        ledgers = Ledger.objects.all()
    return render(request, 'ledger_list.html', {'ledgers': ledgers })

def ledger_create(request):
    if request.method == 'POST':
        form = LedgerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ledger_list')
    else:
        form = LedgerForm()
    return render(request, 'ledger_form.html', {'form': form})

def ledger_update(request, pk):
    ledger = get_object_or_404(Ledger, pk=pk)
    if request.method == 'POST':
        form = LedgerForm(request.POST, instance=ledger)
        if form.is_valid():
            form.save()
            return redirect('ledger_list')
    else:
        form = LedgerForm(instance=ledger)
    return render(request, 'ledger_form.html', {'form': form})

def supplier_ledger(request, pk):
    supplier = Supplier.objects.get(id=pk)
    combined_data = []

    ticket_data = Ticket.objects.filter(supplier=supplier).values(
        'pnr', 'purchase', 'created_at', 'passenger')
    ledger_data = Ledger.objects.filter(supplier=supplier).values(
        'payment', 'payment_date')
    supplier_data = list(ticket_data) + list(ledger_data)

    combined_data.extend(supplier_data)
    combined_data = sorted(
    combined_data,
    key=lambda x: x.get('created_at') or x.get('payment_date', ''),
    reverse=True
    )
    total = supplier.opening_balance
    for entry in combined_data:
        if 'purchase' in entry:
            total += entry['purchase']
        elif 'payment' in entry:
            total -= entry['payment']

        # Add the total to the current entry
        entry['total'] = total

    return render(request, 'supplier_ledger.html', {'data': combined_data, 'supplier': supplier} )
