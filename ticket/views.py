# views.py
from django.shortcuts import render, redirect, get_object_or_404
from ticket_management import settings
from .models import Ticket
from .forms import TicketForm, DateForm
from django.utils.timezone import activate
from django.db.models import Q, F,Sum, DecimalField,OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from .ledger_views import *
from .supplier_views import *
from .customer_views import *
from .csv_manipulation import *
from .visa_views import *
from .hotel_views import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
activate(settings.TIME_ZONE)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, 'Logged in Successfully')
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login.html')
def logout_user(request):
    messages.info(request, 'You Are Logged Out')
    logout(request)
    return redirect('login')

@login_required
def index(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user).select_related('supplier', 'customer', 'issued_by')
    urgent_ticket_id_list = tickets.filter(travel_date__range=(timezone.now(), timezone.now() + timedelta(days=3))).values_list('id', flat=True)
    request.session['urgent_ticket_ids'] =list(urgent_ticket_id_list)
    p = Paginator(tickets.order_by('-created_at'), 50) 
    page= request.GET.get('page')
    tickets = p.get_page(page)
    # profit = tickets.aggregate(profit=Sum(F('sale') - F('purchase')))['profit']
    return render(request, 'ticket_list.html', {'tickets': tickets,  'urgent_ticket': urgent_ticket_id_list})


@require_GET
def get_ticket(request):
    pnr = request.GET.get('pnr')
    ticket = Ticket.objects.filter(user=request.user).filter(pnr=pnr).last()
    data = {
        'ticket_type': ticket.ticket_type,
        'sector': ticket.sector if ticket.sector else 'None',
        'passenger': ticket.passenger,
        'travel_date': (ticket.travel_date + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S') if ticket.travel_date else None,
        'airline': ticket.airline if ticket.airline else 'None',
        'supplier': ticket.supplier.id,
        'customer': ticket.customer.id,
        'sale': ticket.sale,
        'purchase': ticket.purchase,
        'narration': ticket.narration,
        'excel_id': ticket.excel_id,
    }
    return JsonResponse(data)
@login_required
def ticket_create(request):
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, pk=request.POST.get('ticket-id')) if request.POST.get('ticket-id') else None
        form = TicketForm(request.POST, instance=ticket) if ticket else TicketForm(request.POST)
        if form.is_valid():
            pnr = request.POST.get('pnr')
            # instance = form.save(commit=False)
            # travel_date = form.cleaned_data['travel_date']
            # instance.travel_date = datetime.strptime(travel_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            # instance.save()
            form.save()
            status = 200 if ticket else 201
            message = 'Ticket Updated Succefully for PNR:  ' + pnr if ticket else 'Ticket created successfully for PNR: ' + pnr
            return JsonResponse({'status': status, 'message': message }, status=status)
    else:
        form = TicketForm(user=request.user)
    return render(request, 'ticket_form.html', {'form': form})

def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk ,user=request.user)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = TicketForm(instance=ticket, user=request.user)
    return render(request, 'ticket_form.html', {'form': form})

@csrf_exempt
def delete_record(request, pk, model_name):
    model_mapping = {
        'supplier': Supplier,
        'customer': Customer,
        'ledger': Ledger,
        'ticket': Ticket,
        'visa': Visa,
        'hotel': Hotel,
        'room_rate': RoomRate,
        'voucher': Voucher,
    }
    model = model_mapping.get(model_name)
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            return JsonResponse({'status': 'success', 'message': 'Record deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def urgent_tickets(request):
    urgent_ticket_ids = request.session.get('urgent_ticket_ids', [])
    urgent_tickets = Ticket.objects.filter(id__in=urgent_ticket_ids).select_related('supplier', 'customer', 'issued_by')
    # data = urgent_tickets.annotate(
    # days=ExpressionWrapper(
    #     F('travel_date') - timezone.now(),
    #     output_field=fields.DurationField()
    # )
    # )
    return render(request, 'urgent_tickets.html', {'tickets': urgent_tickets})
    
def search(request):
    query = request.GET.get('query')
    results = Ticket.objects.filter(
        Q(user=request.user) &(
        Q(pnr__contains=query) |
        Q(supplier__name__icontains=query) |
        Q(customer__name__icontains=query) 
    )
    )
    if results:
        return render(request, 'ticket_list.html', {'tickets': results})
    else:
        messages.warning(request, 'No matching tickets found.')
        return redirect('index')

def calculate_percentage_difference(sales, purchases):
    if purchases != 0 and sales != 0:
        return round(((sales - purchases) / purchases) * 100,2)
    else:
        return 0
def profit(request):
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            start_at = form.cleaned_data['start_at']
            end_at = form.cleaned_data['end_at']
            daily_profit, dp,monthly_profit,mp, customers= calculate_profit(request, start_at, end_at)
    else:
        form = DateForm()
        start_at = timezone.now().date().replace(day=1)
        end_at=timezone.now().date()
        daily_profit, dp,monthly_profit,mp, customers= calculate_profit(request, start_at, end_at)
        
    return render(request, 'profit.html', {'form':form, 'monthly_profit': monthly_profit, 'daily_profit': daily_profit, 'mp': mp, 'dp': dp, 'customers': customers})

def calculate_profit(request, start_at=None, end_at=None):
    today = end_at
    start_month = start_at
    total_sale = Ticket.objects.filter(user=request.user).filter(created_at__date__gte=start_month, created_at__date__lte=today).filter(customer=OuterRef('pk')).values('customer').annotate(sum=Coalesce(Sum('sale'), Decimal(0))).values('sum')
    total_purchase = Ticket.objects.filter(user=request.user).filter(created_at__date__gte=start_month, created_at__date__lte=today).filter(customer=OuterRef('pk')).values('customer').annotate(sum=Coalesce(Sum('purchase'), Decimal(0))).values('sum')
    total_payment = Ledger.objects.filter(user=request.user).filter(payment_date__date__gte=start_month, payment_date__date__lte=today).filter(customer=OuterRef('pk')).values('customer').annotate(sum=Coalesce(Sum('payment'), Decimal(0))).values('sum')

# Get all customers and annotate with total sales, purchases, and profit (sales - purchases)
    customers = Customer.objects.filter(user=request.user).annotate(
        total_sale=Subquery(total_sale, output_field=DecimalField()),
        total_purchase=Subquery(total_purchase, output_field=DecimalField()),
        total_payment=Coalesce(Subquery(total_payment, output_field=DecimalField()), Decimal(0)),
        
    ).annotate(
        profit=F('total_sale') - F('total_purchase'),
        balance=F('opening_balance') + F('total_sale') - F('total_payment')
    ).order_by('name')
    
    monthly_profit = Ticket.objects.filter(user=request.user).filter(created_at__date__gte=start_month, created_at__date__lte=today).aggregate(total_sale=Coalesce(Sum('sale'),0,output_field=DecimalField()), total_purchase=Coalesce(Sum('purchase'),0,output_field=DecimalField()))
    mp = calculate_percentage_difference(monthly_profit['total_sale'], monthly_profit['total_purchase'])
    monthly_profit = monthly_profit['total_sale'] - monthly_profit['total_purchase']
    
    daily_profit = Ticket.objects.filter(user=request.user).filter(created_at__date=today).aggregate(total_sale=Coalesce(Sum('sale'),0,output_field=DecimalField()), total_purchase=Coalesce(Sum('purchase'),0,output_field=DecimalField()))
    dp = calculate_percentage_difference(daily_profit['total_sale'], daily_profit['total_purchase'])
    daily_profit = daily_profit['total_sale'] - daily_profit['total_purchase']
    return daily_profit, dp,monthly_profit,mp, customers