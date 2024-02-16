from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Supplier, Ledger, Customer
from django.db.models import Q
from django.db.models.functions import Coalesce
from .forms import LedgerForm

def ledger_list(request):
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

def supplier_ledger(request, pk, model_name):
    model_mapping = {
        'supplier': Supplier,
        'customer': Customer,
    }
    model = model_mapping.get(model_name)
    filter_condition = Q()
    obj = get_object_or_404(model, pk=pk)

    combined_data = []

    filter_condition = Q()
    filter_condition &= Q(supplier=obj) if model_name == 'supplier' else Q(customer=obj)
    # Add more conditions for other models if needed
    ticket_data = Ticket.objects.filter(filter_condition).values(
        'pnr', 'purchase', 'created_at', 'passenger')
    ledger_data = Ledger.objects.filter(filter_condition).values(
        'payment', 'payment_date')
    data = list(ticket_data) + list(ledger_data)

    combined_data.extend(data)
    combined_data = sorted(
    combined_data,
    key=lambda x: x.get('created_at') or x.get('payment_date', ''),
    reverse=True
    )
    total = obj.opening_balance
    for entry in combined_data:
        if 'purchase' in entry:
            total += entry['purchase']
        elif 'payment' in entry:
            total -= entry['payment']

        # Add the total to the current entry
        entry['total'] = total

    return render(request, 'supplier_ledger.html', {'data': combined_data, 'obj': obj} )
