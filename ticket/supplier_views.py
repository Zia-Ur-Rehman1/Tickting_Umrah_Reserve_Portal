from django.shortcuts import render, redirect, get_object_or_404
from .models import  Supplier, Ledger, Ticket
from .forms import  SupplierForm
from django.db.models import  Sum, OuterRef, Subquery, F,DecimalField
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce
def supplier_list(request):
    total_purchase = Ticket.objects.filter(user=request.user).filter(supplier=OuterRef('pk')).order_by().values('supplier').annotate(sum=Coalesce(Sum('purchase'), Decimal(0))).values('sum')
    total_payment = Ledger.objects.filter(user=request.user).filter(supplier=OuterRef('pk')).order_by().values('supplier').annotate(sum=Coalesce(Sum('payment'), Decimal(0))).values('sum')

    suppliers = Supplier.objects.filter(user=request.user).exclude(name='CC').annotate(
        total_purchase=Coalesce(Subquery(total_purchase, output_field=DecimalField()), Decimal(0)),
        total_payment=Coalesce(Subquery(total_payment, output_field=DecimalField()), Decimal(0)),
        balance=Coalesce(F('opening_balance'), Decimal(0)) + F('total_purchase') - F('total_payment')
    ).order_by('name')
    total_balance = suppliers.aggregate(total_balance=Sum('balance'))['total_balance']
    return render(request, 'supplier_list.html', {'suppliers': suppliers,'total': total_balance, 'model_name': 'supplier' })

@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            if 'save_and_add_another' in request.POST:
                return redirect(request.path)
            else:
                return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier_form.html', {'form': form})

def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            if 'save_and_add_another' in request.POST:
                return redirect(request.path)
            else:
                return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier_form.html', {'form': form})

