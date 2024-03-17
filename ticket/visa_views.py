from django.shortcuts import render, redirect
from .forms import VisaForm, RialPriceForm
from .models import Visa, RialPrice

def visa_create(request):
    rial_price = RialPrice.objects.last().price
    if request.method == 'POST':
        form = VisaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = VisaForm(user = request.user)
    return render(request, 'Visa/visa_form.html', {'form': form, 'price': rial_price})
def rialprice_create(request):
    if request.method == 'POST':
        form = RialPriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RialPriceForm()
    return render(request, 'Visa/rial_form.html', {'form': form})