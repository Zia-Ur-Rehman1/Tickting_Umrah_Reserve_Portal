import csv
from datetime import datetime
from ticket.forms import CsvGenerationForm, UploadForm
from ticket.models import Supplier, Ticket, Customer
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import  redirect, render
import pdb
import io
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
    csv_writer = csv.writer(response)
    csv_writer.writerow(['Date', 'Passenger Name', 'Sector', 'PNR/V#', 'Supplier', 'Customer', 'Air Line', 'Travel Date', 'Sale', 'Purchase'])
    for ticket in tickets:
        csv_writer.writerow([
            ticket.created_at.strftime('%d-%b') if ticket.created_at else '',
            ticket.passenger if ticket.passenger else '',
            ticket.sector,
            ticket.pnr,
            ticket.supplier.name if ticket.supplier else '',
            ticket.customer.name if ticket.customer else '',
            ticket.airline if ticket.airline else '',
            ticket.travel_date.strftime('%d-%b') if ticket.travel_date else 'Void',
            ticket.sale if ticket.sale else '',
            ticket.purchase if ticket.purchase else '',
        ])

    return response
def process_csv_data(file):
    file = io.TextIOWrapper(file, encoding='utf-8')
    reader = csv.reader(file)
    for row in reader:
        if row is None:
            continue
        date = parse_date(row[0])
        passenger_name = row[1]
        sector = row[2]
        pnr = row[3]
        supplier_name = row[4]
        customer_name = row[6]
        airline = row[7]
        travel_date = parse_date(row[8])
        deal = row[9]
        purchase = row[11]
        ticket = Ticket.objects.filter(pnr=pnr).first()
        if not ticket:
            supplier, _ = Supplier.objects.get_or_create(name=supplier_name)
            customer, _ = Customer.objects.get_or_create(name=customer_name)
        try:
            ticket = Ticket.objects.create(
                created_at=date,
                passenger=passenger_name if passenger_name else None,
                sector=sector if sector else None,
                pnr=pnr,
                supplier=supplier,
                customer=customer,
                airline=airline if airline else None,
                travel_date=travel_date if travel_date and travel_date != "VOID" else None,
                sale=deal if deal else 0,
                purchase=purchase if purchase else 0
            )
            ticket.save()
    # Continue with the rest of the code if the Ticket object creation is successful
    # ...
        except Exception as e:
            # Handle the exception appropriately
            print(f"An error occurred: {str(e)}")
            print(f"Error occurred for the following values: passenger_name={passenger_name}, sector={sector}, pnr={pnr}, supplier={supplier}, customer={customer}, airline={airline}, travel_date={travel_date}, deal={deal}, purchase={purchase}")
                # Save the Ticket instance
def parse_date(date_str):
    # Get the current year
    current_year = datetime.now().year
    
    # Append the current year to the date string
    date_str_with_year = f"{date_str}-{current_year}"
    
    # Define the format of the date string
    date_format = '%d-%b-%Y'  # Example format: '1-Jan-2022'
    
    try:
        # Parse the date string into a datetime object
        parsed_date = datetime.strptime(date_str_with_year, date_format)
        return parsed_date
    except ValueError:
        # Handle the case where the date string is not in the expected format
        return None
def upload_csv(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            
            # process_csv_data(file)
            match_csvs(file)
            # Handle any further actions or redirect to a success page
    else:
        form = UploadForm()
    return render(request, "upload.html", {"form": form})

def match_csvs(file):
    file = io.TextIOWrapper(file, encoding='utf-8')
    reader = csv.reader(file)
    for row in reader:
        if row is None or row[2] is None or row[4] == '-':
            continue
        values = row[3].split()
        if len(values) >= 8:
            pnr = row[3].split()[8]
            ticket = Ticket.objects.filter(pnr=pnr).first()
            if ticket:
                if ticket.purchase == round(float(row[4])):
                    continue
                else:
                    print(f"PNR {ticket.pnr} matched but value mismatch: {ticket.purchase} != {row[4]}")