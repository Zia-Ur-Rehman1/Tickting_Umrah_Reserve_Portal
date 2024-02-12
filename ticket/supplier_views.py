from django.shortcuts import render, redirect, get_object_or_404
from .models import  Supplier
from .forms import  SupplierForm
from django.db.models import  Sum
def supplier_list(request):
    suppliers =  Supplier.objects.annotate(total_purchase=Sum('ticket__purchase')).values('id', 'name', 'total_purchase', 'opening_balance')
    return render(request, 'supplier_list.html', {'suppliers': suppliers, 'model_name': 'supplier' })

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier_list.html', {'form': form})

