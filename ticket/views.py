# views.py
from django.shortcuts import render, redirect, get_object_or_404
from ticket_management import settings
from .models import Ticket
from .forms import TicketForm
from django.utils.timezone import activate
from django.db.models import Q, F, ExpressionWrapper, fields
from django.contrib import messages
from datetime import timedelta, datetime
from django.utils import timezone
from .ledger_views import *
from .supplier_views import *
from .customer_views import *
from .csv_manipulation import *
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
    tickets = Ticket.objects.filter(user=request.user).select_related('supplier', 'customer')
    urgent_ticket = tickets.filter(travel_date__range=(timezone.now(), timezone.now() + timedelta(days=3))).count()
    p = Paginator(tickets.order_by('-created_at'), 20) 
    page= request.GET.get('page')
    tickets = p.get_page(page)
    # profit = tickets.aggregate(profit=Sum(F('sale') - F('purchase')))['profit']
    return render(request, 'ticket_list.html', {'tickets': tickets,  'urgent_ticket': urgent_ticket})


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
        # Add other fields...
    }
    return JsonResponse(data)
@login_required
def ticket_create(request):
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, pk=request.POST.get('ticket-id')) if request.POST.get('ticket-id') else None
        form = TicketForm(request.POST, instance=ticket) if ticket else TicketForm(request.POST)
        if form.is_valid():
            pnr = request.POST.get('pnr')
            form.save()
            status = 200 if ticket else 201
            message = 'Ticket Updated Succefully for PNR:  ' + pnr if ticket else 'Ticket created successfully for PNR: ' + pnr
            return JsonResponse({'status': status, 'message': message }, status=status)
    else:
        form = TicketForm()
        suppliers = Supplier.objects.filter(user=request.user).all()
        customers = Customer.objects.filter(user=request.user).all()
    return render(request, 'ticket_form.html', {'form': form, 'suppliers': suppliers, 'customers': customers})

def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = TicketForm(instance=ticket)
        suppliers = Supplier.objects.filter(user=request.user).all()
        customers = Customer.objects.filter(user=request.user).all()
    return render(request, 'ticket_form.html', {'form': form, 'suppliers': suppliers, 'customers': customers})

@csrf_exempt
def delete_record(request, pk, model_name):
    model_mapping = {
        'supplier': Supplier,
        'customer': Customer,
        'ledger': Ledger,
        'ticket': Ticket,
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
    urgent_tickets = Ticket.objects.filter(user=request.user).filter(travel_date__range=(timezone.now(),timezone.now() + timedelta(days=3)))
    data = urgent_tickets.annotate(
    days=ExpressionWrapper(
        F('travel_date') - timezone.now(),
        output_field=fields.DurationField()
    )
    )
    return render(request, 'urgent_tickets.html', {'tickets': data})
    
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

