# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket
from .forms import TicketForm, CsvGenerationForm
import csv
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone

def ticket_list(request):
    tickets = Ticket.objects.all()
    data = tickets.filter(travel_date__lte=timezone.now() + timedelta(days=10)).values_list('pnr','travel_date')

    message_list = messages.get_messages(request)
    return render(request, 'ticket_list.html', {'tickets': tickets, 'message_list': message_list, 'data': data})

def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
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
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'ticket_form.html', {'form': form})

def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('ticket_list')
    return render(request, 'ticket_confirm_delete.html', {'ticket': ticket})

def generateCSV(request):
    if request.method == 'POST':
  
        form = CsvGenerationForm(request.POST)
        if form.is_valid():
            # Process form data, for example, save to the database
            supplier_name = form.cleaned_data['supplier_name']
            customer_name = form.cleaned_data['customer_name']
            start_at = form.cleaned_data['start_at']
            end_at = form.cleaned_data['end_at']
            tickets = Ticket.objects.filter(created_at__gte=start_at, 
                                  created_at__lte=end_at).filter(Q(supplier__name__icontains=supplier_name) 
                                                                | Q(supplier=None)).filter(Q(customer__name__icontains=customer_name)
                                                                                           | Q(customer=None))
            if tickets:
                return generate_csv(tickets)
            else:
                messages.warning(request, 'No matching tickets found.')
                return redirect('ticket_list')
        else:
            return redirect('ticket_list')

def generate_csv(tickets):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tickets_new.csv"'

                # Create a CSV writer
    csv_writer = csv.writer(response)

                # Write header
    csv_writer.writerow(['PNR', 'Sector', 'Travel Date', 'Airline', 'Supplier', 'Customer'])

    
                # Write data rows
    for ticket in tickets:
        csv_writer.writerow([
            ticket.pnr,
            ticket.sector,
            ticket.travel_date,
            ticket.airline.name if ticket.airline else '',
            ticket.supplier.name if ticket.supplier else '',
            ticket.customer.name if ticket.customer else ''
        ])

    return response
def search(request):
    query = request.GET.get('query')

    results = Ticket.objects.filter(
        Q(pnr__icontains=query) |
        Q(supplier__name__icontains=query) |
        Q(customer__name__icontains=query) 
    )
    if results:
        return render(request, 'ticket_list.html', {'tickets': results})
    else:
        messages.warning(request, 'No matching tickets found.')
        return redirect('ticket_list')