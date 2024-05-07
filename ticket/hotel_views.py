from django.shortcuts import render, redirect, get_object_or_404
from .forms import  HotelForm, RoomRateForm, HotelVoucherForm,VisaSearchForm,TripForm
from .models import Hotel, RiyalPrice, RoomRate
from django.db.models import Prefetch
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.http import JsonResponse
def add_hotel(request):
    riyal_rate = RiyalPrice.objects.filter(user=request.user).last().price if RiyalPrice.objects.filter(user=request.user).exists() else 0
    RoomRateFormSet = inlineformset_factory(Hotel, RoomRate, form=RoomRateForm, extra=5)
    if request.method == "POST":
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save()
            formset = RoomRateFormSet(request.POST, instance=hotel)
            if formset.is_valid():
            
                instances = formset.save(commit=False)
                date_from = formset.forms[4].cleaned_data.get('date_from')
                date_to = formset.forms[4].cleaned_data.get('date_to')
                for instance in instances:
                    instance.date_from = date_from
                    instance.date_to = date_to
                    instance.pkr_price = instance.riyal_price * riyal_rate
                    instance.save()
                return redirect('hotel_list')
            else:
                print("Formset")
                print(formset.errors)
        else:
            print(form.errors.as_data())
            
    else:
        current_user = request.user
        initial_data = [{'room_type': i, 'user': current_user, 'riyal_rate': riyal_rate} for i in range(5)]
        form = HotelForm(user=request.user)
        formset = RoomRateFormSet(initial=initial_data)
    return render(request, 'partials/add_hotel.html', {'form': form, 'formset': formset, 'riyal_rate': riyal_rate})
def update_hotel(request, pk):
    riyal_rate = RiyalPrice.objects.filter(user=request.user).last().price if RiyalPrice.objects.filter(user=request.user).exists() else 0
    hotel = get_object_or_404(Hotel, id=pk)
    form = HotelForm(request.POST or None, instance=hotel)
    RoomRateFormSet = inlineformset_factory(Hotel, RoomRate, form=RoomRateForm, extra=(5 - hotel.roomrate_set.count()))
    formset = RoomRateFormSet(request.POST or None, instance=hotel)
    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.pkr_price = instance.riyal_price * riyal_rate
                instance.save()
            return redirect('hotel_list')
    return render(request, 'partials/add_hotel.html', {'form': form, 'formset': formset, 'riyal_rate': riyal_rate})
   
def hotel_list(request):
    room_rates = RoomRate.objects.filter(user=request.user).all().order_by('room_type')
    hotels = Hotel.objects.filter(user=request.user).prefetch_related(Prefetch('roomrate_set', queryset=room_rates, to_attr='rates'))
    context = {
        'hotels': hotels,
        'ROOM_CATEGORY': RoomRate.ROOM_CATEGORY,
    }
    return render(request, 'hotel_list.html', context)

