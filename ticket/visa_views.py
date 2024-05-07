from django.shortcuts import render, redirect, get_object_or_404
from .forms import VisaForm, RiyalPriceForm, VisaSearchForm
from .models import Visa, RiyalPrice
from django.http import JsonResponse
from django.db.models.functions import TruncDate
def visa_list(request):
    riyal_price = RiyalPrice.objects.filter(user=request.user).last().price if RiyalPrice.objects.filter(user=request.user).exists() else 0
    
    visas = Visa.objects.filter(user=request.user).all()
    return render(request, 'Visa/visa_list.html', {'visas': visas, "price": riyal_price})
def visa_create(request):
    riyal_price = RiyalPrice.objects.filter(user=request.user).last().price if RiyalPrice.objects.filter(user=request.user).exists() else 0
    if request.method == 'POST':
        form = VisaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visa_list')
    else:
        
        form = VisaForm(user = request.user)
    return render(request, 'Visa/visa_form.html', {'form': form, 'price': riyal_price})


def visa_update(request, pk):
    riyal_price = RiyalPrice.objects.filter(user=request.user).last().price if RiyalPrice.objects.filter(user=request.user).exists() else 0
    visa = get_object_or_404(Visa, pk=pk)
    if request.method == 'POST':
        form = VisaForm(request.POST, instance=visa)
        if form.is_valid():
            form.save()
            return redirect('visa_list')
    else:
        form = VisaForm(instance=visa, user=request.user)
    return render(request, 'Visa/visa_form.html', {'form': form, "price": riyal_price})
def riyalprice_create(request):
    if request.method == 'POST':
        form = RiyalPriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visa_list')
    else:
        form = RiyalPriceForm()
    return render(request, 'Visa/riyal_form.html', {'form': form})


def get_visas(request):
    pass_num = request.GET.get('pass_num')
    visa = Visa.objects.get(user=request.user, pass_num=pass_num)
    visas = Visa.objects.filter(user=request.user).filter(created_at__date=TruncDate(visa.created_at)).values('id','pass_num', 'pass_name')
    return JsonResponse(list(visas), safe=False)