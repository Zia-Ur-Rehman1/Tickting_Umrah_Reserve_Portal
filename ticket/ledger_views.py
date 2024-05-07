from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Ticket, Supplier, Ledger, Customer,Bank
from django.db.models import Q
from .forms import LedgerForm
from django.contrib.auth.decorators import login_required
from sqids import Sqids
from datetime import timedelta
from django.core.paginator import Paginator
from PIL import Image
import pytesseract
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from datetime import datetime
from django.db.models import Prefetch
from pdfminer.high_level import extract_text
from io import BytesIO
def ledger_list(request):
    p = Paginator(Ledger.objects.filter(user=request.user).select_related('supplier', 'customer').all().order_by('supplier__name', 'customer__name', 'payment_date'), 100)
    page= request.GET.get('page')
    ledgers = p.get_page(page)
    return render(request, 'ledger_list.html', {'ledgers': ledgers })
@login_required
def ledger_create(request):
    if request.method == 'POST':
        form = LedgerForm(request.POST)
        if form.is_valid():
            form.save()
            sq = Sqids()
            if 'save_and_add_another' in request.POST:
                return redirect(request.path)
            else:
                if form.cleaned_data['customer'] is not None:
                    return redirect('supplier_ledger', pk=sq.encode([form.cleaned_data['customer'].id]), model_name='customer')
                elif form.cleaned_data['supplier'] is not None:
                    return redirect('supplier_ledger', pk=sq.encode([form.cleaned_data['supplier'].id]), model_name='supplier')
    else:
        form = LedgerForm(user= request.user)
    return render(request, 'ledger_form.html', {'form': form})

def ledger_update(request, pk):
    ledger = get_object_or_404(Ledger, pk=pk)
    
    if request.method == 'POST':
        form = LedgerForm(request.POST, instance=ledger)
        if form.is_valid():
            form.save()
            sq = Sqids()
            if 'save_and_add_another' in request.POST:
                return redirect(request.path)
            else:
                if form.cleaned_data['customer'] is not None:
                    return redirect('supplier_ledger', pk=sq.encode([form.cleaned_data['customer'].id]), model_name='customer')
                elif form.cleaned_data['supplier'] is not None:
                    return redirect('supplier_ledger', pk=sq.encode([form.cleaned_data['supplier'].id]), model_name='supplier')
    else:
        form = LedgerForm(instance=ledger, user=request.user)
    return render(request, 'ledger_form.html', {'form': form})

def supplier_ledger(request, pk, model_name):
    sq = Sqids()
    pk = sq.decode(pk)[0]
    obj = get_obj(pk, model_name)
    combined_data = ledger_generate(obj, model_name)
    if combined_data:
        return render(request, 'supplier_ledger.html', {'data': combined_data, 'obj': obj, 'total_balance': combined_data[-1]['total'], 'model_name': model_name} )
    else:
        messages.success(request, 'No data to show ')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def get_obj(pk, model_name):
    model_mapping = {
        'supplier': Supplier,
        'customer': Customer,
    }
    model = model_mapping.get(model_name)
    # Fetching all related Ticket and Ledger objects in a single query without custom ordering
    # combined_data = []
    # ticket_prefetch = Prefetch(
    #             'ticket_set',
    #             queryset=Ticket.objects.filter(created_at__range=(start_date, end_date)),
    #             to_attr='filtered_tickets'
    #     )
    # ledger_prefetch = Prefetch(
    #         'ledger_set',
    #         queryset=Ledger.objects.filter(payment_date__range=(start_date, end_date)),
    #         to_attr='filtered_ledgers'
    #     )
    # if model_name == 'supplier':
    #     obj = Supplier.objects.prefetch_related(ticket_prefetch, ledger_prefetch).get(id=pk)
    # else:
    #     obj = Customer.objects.prefetch_related(ticket_prefetch, ledger_prefetch).get(id=pk)
        
    # tickets = list(obj.ticket_set.all())
    # ledgers = list(obj.ledger_set.all())
    # combined_data.extend(tickets)
    # combined_data.extend(ledgers)
    
    obj = get_object_or_404(model, pk=pk)
    return obj
def ledger_generate(obj, model_name, start_at=None, end_at=None):
    combined_data = []

    filter_condition = Q()
    filter_condition &= Q(supplier=obj) if model_name == 'supplier' else Q(customer=obj)
    # Add more conditions for other models if needed
    if start_at:
        end_at += timedelta(days=1)
        ticket_data = Ticket.objects.filter(filter_condition, created_at__range=(start_at,end_at)).values(
            'pnr', 'purchase', 'sale', 'created_at', 'passenger', 'id', 'supplier__name','customer__name')
        ledger_data = Ledger.objects.filter(filter_condition, payment_date__range=(start_at,end_at)).values(
            'payment', 'payment_date', 'id', 'description')
    else:
        ticket_data = Ticket.objects.filter(filter_condition).values(
            'pnr', 'purchase', 'sale', 'created_at', 'passenger', 'id', 'supplier__name','customer__name')
        ledger_data = Ledger.objects.filter(filter_condition).values(
            'payment', 'payment_date', 'id', 'description')

    combined_data.extend(ticket_data)
    combined_data.extend(ledger_data)
    combined_data = sorted(
    combined_data,
    key=lambda x: x.get('created_at') or x.get('payment_date', '')    )
    total = obj.opening_balance
    for entry in combined_data:
        if model_name == 'supplier' and 'purchase' in entry:
            total += entry['purchase']
        elif model_name == 'customer' and 'sale' in entry:
            total += entry['sale']
        elif 'payment' in entry:
            total -= entry['payment']
        entry['total'] = total
    return combined_data
@csrf_exempt
def parse_file(request):
    if request.method == "POST":
        file = request.FILES["file"]
        price= 0
        django_date = None
        try:
            img = Image.open(file)
            config = '--psm 6 --oem 1 -l eng'
            text = pytesseract.image_to_string(img, lang='eng', config=config)
            original= text
            lines = text.split('\n')
            lines = list(filter(lambda line: line.strip(), lines))
            # UBL
            if 'www.ubldigital.com' in text:
                price= re.findall(r'\d+', lines[9].replace(',', ''))
                formatted_data={
                    'Bank': 'UBL',
                    'From': lines[2],
                    'From Account': lines[4],
                    'To': lines[5].replace('To ', ''),
                    'To IBAN': lines[6],
                }
                django_date= get_date(lines[1], "%d %B, %Y %I:%M %p")
                text = '\n'.join(f'{key}: {value}' for key, value in formatted_data.items())
            # # HBL       
            elif 'via HBL Digital' in text:
                formatted_data = {
                       'Bank': 'HBL',
                       'From': lines[8],
                       'To': lines[10],
                       'To IBAN': lines[12],
                }
                django_date= get_date(lines[4], '%m/%d/%Y %I:%M:%S %p')
                price = lines[6].strip()
                text = '\n'.join(f'{key}: {value}' for key, value in formatted_data.items())
            # Meezan
            elif "Meezan Bank" in text or "statement in next workina dav hit halance will" in text :
                formatted_data = {
                       'Bank': 'Meezan',
                       'From': lines[1],
                       'From Account': lines[2],
                       'To': lines[6][:-2],
                       'To IBAN': lines[7],
                }
                price= re.findall(r'\d+', lines[4].replace(',', ''))
                django_date= get_date(lines[9], "%d %b %Y %I:%M %p")
                text = '\n'.join(f'{key}: {value}' for key, value in formatted_data.items())
            
            # Alfalah
            elif "Transaction Type Interbranch" in text:
                formatted_data = {
                       'Bank': 'Alfalah',
                       'From': lines[7][5:],
                       'From Account': lines[8][13:],
                       'To': lines[5][3:],
                       'To IBAN': lines[6][16:],
                }
                price= re.findall(r'\d+', lines[-1].replace(',', ''))
                django_date= get_date(lines[3], "%d %B %Y | %H:%M %p")
                text = '\n'.join(f'{key}: {value}' for key, value in formatted_data.items())
            else:
                text = '\n'.join(lines)
            return JsonResponse({'status': 'success', 'text': text, 'price': price,'date': django_date,'original': original }, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e), 'original': original}, status=500)

def get_date(value, format):
    try:
        date_time_obj = datetime.strptime(value, format)
        django_date = date_time_obj.strftime('%Y-%m-%d %H:%M')
        return django_date
    except ValueError:
        return None


# import pdfquery

# def extract_text_with_bbox(file_path):
#     pdf = pdfquery.PDFQuery(file_path)
#     pdf.load()

#     results = []

#     for page_num in range(len(pdf.tree.xpath('//LTPage'))):
#         page = pdf.get_layout(page_num)
#         for element in page:
#             if isinstance(element, pdfquery.layout.LTTextBoxHorizontal):
#                 results.append({
#                     'page': page_num + 1,
#                     'bbox': element.bbox,
#                     'text': element.get_text()
#                 })

#     return results

# # Usage
# for pdf in pdf_list:
#     results = extract_text_with_bbox(pdf)
#     for result in results:
#         print(f"Page: {result['page']}, BBox: {result['bbox']}, Text: {result['text']}")
