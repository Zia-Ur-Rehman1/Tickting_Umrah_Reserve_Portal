from django.shortcuts import render, redirect, get_object_or_404
from .models import  *
from .forms import CustomerForm
from django.db.models import  Sum, OuterRef, Subquery, F,DecimalField
from decimal import Decimal
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required

def customer_list(request):
    total_sale = Ticket.objects.filter(customer=OuterRef('pk')).values('customer').annotate(sum=Coalesce(Sum('sale'), Decimal(0))).values('sum')
    total_payment = Ledger.objects.filter(customer=OuterRef('pk')).values('customer').annotate(sum=Coalesce(Sum('payment'), Decimal(0))).values('sum')
    customers = Customer.objects.filter(user=request.user).annotate(
        total_purchase=Coalesce(Subquery(total_sale, output_field=DecimalField()), Decimal(0)),
        total_payment=Coalesce(Subquery(total_payment, output_field=DecimalField()), Decimal(0)),
        balance=Coalesce(F('opening_balance'), Decimal(0)) + F('total_purchase') - F('total_payment')
         ).order_by('name')
    total_balance = customers.aggregate(total_balance=Sum('balance'))['total_balance']
    return render(request, 'customer_list.html', {'customers': customers, 'total': total_balance, 'model_name': 'customer'})
@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            if 'save_and_add_another' in request.POST:
                return redirect(request.path)
            else:
                return redirect('customer_list')

    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {'form': form})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            if 'save_and_add_another' in request.POST:
                return redirect(request.path)
            else:
                return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_form.html', {'form': form})
