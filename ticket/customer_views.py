from django.shortcuts import render, redirect, get_object_or_404
from .models import  Customer
from .forms import CustomerForm
from django.db.models import  Sum

def customer_list(request):
    customers =  Customer.objects.annotate(total_purchase=Sum('ticket__sale'), total_payment=Sum('ledger__payment'))
    return render(request, 'customer_list.html', {'customers': customers, 'model_name': 'customer'})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_form.html', {'form': form})
