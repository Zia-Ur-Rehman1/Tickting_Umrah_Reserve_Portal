from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Ticket, Supplier, Ledger, Customer
from django.db.models import Q
from .forms import LedgerForm
from django.contrib.auth.decorators import login_required
from sqids import Sqids
from datetime import timedelta
from django.core.paginator import Paginator

def ledger_list(request):
   
    p = Paginator(Ledger.objects.filter(user=request.user).select_related('supplier', 'customer').all().order_by('payment_date'), 100)
    page= request.GET.get('page')
    ledgers = p.get_page(page)
    return render(request, 'ledger_list.html', {'ledgers': ledgers })
@login_required
def ledger_create(request):
    if request.method == 'POST':
        form = LedgerForm(request.POST)
        if form.is_valid():
            form.save()
            if 'save_and_add_another' in request.POST:
                return redirect(request.path)
            else:
                return redirect('ledger_list')

    else:
        form = LedgerForm(user= request.user)
    return render(request, 'ledger_form.html', {'form': form})

def ledger_update(request, pk):
    ledger = get_object_or_404(Ledger, pk=pk)
    
    if request.method == 'POST':
        form = LedgerForm(request.POST, instance=ledger)
        if form.is_valid():
            form.save()
            if 'save_and_add_another' in request.POST:
                return redirect(request.path)
            else:
                return redirect('ledger_list')
    else:
        form = LedgerForm(instance=ledger, user=request.user)
    return render(request, 'ledger_form.html', {'form': form})

def supplier_ledger(request, pk, model_name):
    sq = Sqids()
    pk = sq.decode(pk)[0]
    obj = get_obj(pk, model_name)
    combined_data = ledger_generate(obj, model_name)
    if combined_data:
        return render(request, 'supplier_ledger.html', {'data': combined_data, 'obj': obj, 'total_balance': combined_data[-1]['total'], 'model_name': model_name} )
    else:
        messages.success(request, 'No data to show ')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def get_obj(pk, model_name):
    model_mapping = {
        'supplier': Supplier,
        'customer': Customer,
    }
    model = model_mapping.get(model_name)
    obj = get_object_or_404(model, pk=pk)
    return obj
def ledger_generate(obj, model_name, start_at=None, end_at=None):
    combined_data = []

    filter_condition = Q()
    filter_condition &= Q(supplier=obj) if model_name == 'supplier' else Q(customer=obj)
    # Add more conditions for other models if needed
    if start_at:
        end_at += timedelta(days=1)
        ticket_data = Ticket.objects.filter(filter_condition, created_at__range=(start_at,end_at)).values(
            'pnr', 'purchase', 'sale', 'created_at', 'passenger', 'id')
        ledger_data = Ledger.objects.filter(filter_condition, payment_date__range=(start_at,end_at)).values(
            'payment', 'payment_date', 'id', 'description')
    else:
        ticket_data = Ticket.objects.filter(filter_condition).values(
            'pnr', 'purchase', 'sale', 'created_at', 'passenger', 'id')
        ledger_data = Ledger.objects.filter(filter_condition).values(
            'payment', 'payment_date', 'id', 'description')

    combined_data.extend(ticket_data)
    combined_data.extend(ledger_data)
    combined_data = sorted(
    combined_data,
    key=lambda x: x.get('created_at') or x.get('payment_date', '')    )
    total = obj.opening_balance
    previous = total
    for entry in combined_data:
        if model_name == 'supplier' and 'purchase' in entry:
            total += entry['purchase']
        elif model_name == 'customer' and 'sale' in entry:
            total += entry['sale']
        elif 'payment' in entry:
            total -= entry['payment']
        entry['total'] = total
        previous = entry['total']
    return combined_data