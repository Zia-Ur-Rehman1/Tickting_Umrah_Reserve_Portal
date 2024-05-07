from django.http import JsonResponse
from .forms import HotelVoucherForm,VisaSearchForm,TripForm, TransportForm
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch

from .models import Voucher,HotelBooking,Trip,Visa,Hotel,RoomRate
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render
from .models import Voucher, Visa, Hotel, RoomRate, HotelBooking, Trip
from .forms import HotelVoucherForm, TripForm, VisaSearchForm, TransportForm
from django.db import transaction
def extract_data(request, voucher):
    query_dict = request.POST  # or request.GET
    visas = query_dict.getlist('visa')
    transport = query_dict.get('transport')
    if voucher is None:
        voucher = Voucher.objects.create(user=request.user, transport=transport)
        

    hotels = [
        HotelBooking(
            voucher=voucher,
            hotel=Hotel.objects.get(id=query_dict.get(f'hotels-{i}-hotel')),
            room = RoomRate.objects.get(id=query_dict.get(f'hotels-{i}-room')),
            check_in=query_dict.get(f'hotels-{i}-start_at'),
            check_out=query_dict.get(f'hotels-{i}-end_at'),
            nights=query_dict.get(f'hotels-{i}-nights'),
        )
        for i in range(3) if query_dict.get(f'hotels-{i}-hotel') and query_dict.get(f'hotels-{i}-hotel') != '-1'
    ]

    trips = [
        Trip(
            voucher=voucher,
            flight=query_dict.get(f'trips-{i}-flight'),
            sector=query_dict.get(f'trips-{i}-sector'),
            departure=query_dict.get(f'trips-{i}-departure'),
            arrival=query_dict.get(f'trips-{i}-arrival'),
        )
        for i in range(2) if all(query_dict.get(f'trips-{i}-{field}') for field in ['flight', 'sector', 'departure', 'arrival'])
    ]

    return {
        'visas': visas,
        'hotels': hotels,
        'trips': trips,
        'transport': transport,
        'voucher': voucher,
    }
@transaction.atomic
def create_voucher(request):
    if request.method == 'POST':
        data = extract_data(request, voucher=None)
        voucher = data['voucher']
        # Bulk add visas to the voucher
        visa_ids = data['visas']
        if visa_ids:
            voucher.visas.add(*Visa.objects.filter(id__in=visa_ids))
        HotelBooking.objects.bulk_create(data['hotels'])
        created_trips = Trip.objects.bulk_create(data['trips'])
        voucher.trip.add(*created_trips)
        return JsonResponse({ 'message': "Voucher Created Successfully" }, status=201)
    else:
        HotelFormSet = formset_factory(HotelVoucherForm, extra=3)
        TripFormSet = formset_factory(TripForm, extra=2)
        hotel_formset = HotelFormSet(prefix='hotels')
        trip_formset = TripFormSet(prefix='trips')
        visa_form = VisaSearchForm(user=request.user)
        transport_form = TransportForm()
        return render(request, 'hotel/hotel_voucher.html', {'hotel_formset': hotel_formset, 'visa_form': visa_form, 'trip_formset': trip_formset, 'transport_form': transport_form})

@transaction.atomic
def update_voucher(request, pk):
    voucher = get_object_or_404(Voucher, pk=pk)
    
    if request.method == 'POST':
        data = extract_data(request, voucher=voucher)
        voucher.transport = data['transport']
        voucher.save()
        # Clear existing visas and add new ones
        voucher.visas.clear()
        voucher.visas.add(*Visa.objects.filter(id__in=data['visas']))
        # remove and create hotel bookings
        voucher.hotelbooking_set.all().delete()
        HotelBooking.objects.bulk_create(data['hotels'])
        voucher.trip.all().delete()
        created_trips = Trip.objects.bulk_create(data['trips'])
        voucher.trip.add(*created_trips)
        return JsonResponse({ 'message': "Voucher Updated Successfully" }, status=200)
    
    else:
        HotelFormSet = formset_factory(HotelVoucherForm, extra=3 - voucher.hotelbooking_set.count())
        TripFormSet = formset_factory(TripForm, extra=2 - voucher.trip.count())
        
        hotel_formset = HotelFormSet(
            prefix='hotels',
            initial=[{
                'city': hb.hotel.city,
                'hotel': hb.hotel.id,
                'room': hb.room.id,
                'start_at': hb.check_in,
                'end_at': hb.check_out,
                'nights': hb.nights
            } for hb in voucher.hotelbooking_set.all()]
        )
        
        trip_formset = TripFormSet(
            prefix='trips',
            initial=[{
                'flight': t.flight,
                'sector': t.sector,
                'departure': t.departure,
                'arrival': t.arrival
            } for t in voucher.trip.all()]
        )
        visa_form = VisaSearchForm(initial={'visa': voucher.visas.all()}, user=request.user)

        transport_form = TransportForm(initial={'transport': voucher.transport})

        
        return render(request, 'hotel/hotel_voucher.html', {
            'hotel_formset': hotel_formset,
            'visa_form': visa_form,
            'trip_formset': trip_formset,
            'transport_form': transport_form,
            'voucher_id': voucher.id,
        })
    
def load_hotels(request):
    city = request.GET.get('city')
    hotels = Hotel.objects.filter(user=request.user).filter(city=city).values('id', 'hotel_name')
    hotel_list = list(hotels)
    # return render(request,'hotel/hotel_voucher.html', {'hotels': hotels})
    return JsonResponse(hotel_list, safe=False)
def load_rooms(request):
    hotel = request.GET.get('hotel')
    rooms = RoomRate.objects.filter(user=request.user).filter(hotel=hotel).values('id', 'room_type', 'date_from','date_to','riyal_price','riyal_rate','pkr_price')
    room_list = list(rooms)
    return JsonResponse(room_list, safe=False)

def vouchers(request):
    vouchers = Voucher.objects.filter(user=request.user).prefetch_related(
        'visas',
        'trip',
        Prefetch('hotelbooking_set', queryset=HotelBooking.objects.select_related('hotel', 'room')),
    )
    # Pass the data to the template context
    context = {
        'vouchers': vouchers,
    }
    return render(request, 'partials/voucher.html',  context)

