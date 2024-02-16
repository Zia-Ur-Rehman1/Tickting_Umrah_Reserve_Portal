# views.py
from django.shortcuts import render, redirect, get_object_or_404
from ticket_management import settings
from .models import Ticket
from .forms import TicketForm
from django.utils.timezone import activate
from django.db.models import Q, F, ExpressionWrapper, fields
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from .ledger_views import *
from .supplier_views import *
from .customer_views import *
from .csv_manipulation import *
activate(settings.TIME_ZONE)

def ticket_list(request):
    tickets = Ticket.objects.all().order_by('-created_at')
    urgent_tickets = tickets.filter(travel_date__range=(timezone.now(),timezone.now() + timedelta(days=3))).count()

    message_list = messages.get_messages(request)
    return render(request, 'ticket_list.html', {'tickets': tickets, 'message_list': message_list, 'urgent_tickets': urgent_tickets})


def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            airline = cleaned_data['airline']
            passenger = cleaned_data['passenger']
            print (airline)
            print(passenger)
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'ticket_form.html', {'form': form})

def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            airline = cleaned_data['airline']
            passenger = cleaned_data['passenger']
            print (airline)
            print(passenger)
          
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'ticket_form.html', {'form': form})

def delete_record(request, pk, model_name):
    model_mapping = {
        'supplier': Supplier,
        'customer': Customer,
        'ledger': Ledger,
        'ticket': Ticket,
    }
    model = model_mapping.get(model_name)

    obj = get_object_or_404(model, pk=pk)
    model_list = model_name + '_list'
    if request.method == 'POST':
        obj.delete()
        return redirect(model_list)
    return render(request, 'obj_confirm_delete.html', {'obj': obj, 'model_name': model_name, 'model_list': model_list})

def urgent_tickets(request):
    urgent_tickets = Ticket.objects.filter(travel_date__range=(timezone.now(),timezone.now() + timedelta(days=3)))
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
        Q(pnr__contains=query) |
        Q(supplier__name__icontains=query) |
        Q(customer__name__icontains=query) 
    )
    if results:
        return render(request, 'ticket_list.html', {'tickets': results})
    else:
        messages.warning(request, 'No matching tickets found.')
        return redirect('ticket_list')
