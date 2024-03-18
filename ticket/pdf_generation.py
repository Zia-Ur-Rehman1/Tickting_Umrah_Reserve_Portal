from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .ledger_views import *
from .forms import PdfGenerationForm
from functools import partial
def generatePDF(request):
    if request.method == 'POST':
        form = PdfGenerationForm(request.POST)
        if form.is_valid():
            # Process form data, for example, save to the database
            supplier = form.cleaned_data['supplier']
            customer = form.cleaned_data['customer']
            start_at = form.cleaned_data['start_at']
            end_at = form.cleaned_data['end_at']
            if supplier:
                model = 'supplier'
                response = createPDF(request, supplier, model, start_at, end_at)
            else:
                model = 'customer'
                response = createPDF(request, customer, model, start_at, end_at)
            if response is None:
                messages.error(request, 'No Data Found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.success(request, 'Pdf generated Succefully')
                return response
        else:
            return render(request, 'generate_pdf.html', {'form': form})

    else:
        suppliers = Supplier.objects.filter(user=request.user).all()
        customers = Customer.objects.filter(user=request.user).all()
        form = PdfGenerationForm()
        return render(request, 'generate_pdf.html', {'form': form, 'suppliers': suppliers, 'customers': customers})
        
def drawHeader(canvas, doc, start_at, end_at, user=None):
    start_date_str = start_at.strftime("%d %b")
    end_date_str = end_at.strftime("%d %b")
    date = f"From: {start_date_str} To: {end_date_str}"
    canvas.setFillColor(colors.lightblue)
    canvas.setStrokeColor(colors.lightblue)
    # Draw a rectangle that covers the whole page
    header_height = 70  # Adjust this value to match your header's height
    canvas.rect(0, doc.height + doc.bottomMargin + doc.topMargin - header_height, doc.width + 2*doc.leftMargin, header_height, fill=True)
    
    canvas.saveState()
    canvas.setFont('Times-Bold',16)
    # Draw the company name
    canvas.setFillColor(colors.black)
    if user.id == 2:
        company_name = "HASNAIN TRAVEL AND TOURS PRIVATE LIMITED"
    else:
        company_name = "KARWAN E HASSAN HAJJ AND UMRAH SERVICES"
        
    canvas.drawString(doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - 30, company_name)
    # Draw the image on the right end of the page
    if user.id == 2:
        img = Image('ticket/static/ticket/images/HT.png', width=50, height=50)
    else:
        img = Image('ticket/static/ticket/Karwan.jpg', width=50, height=50)
    img.drawOn(canvas, doc.width + doc.leftMargin - 30 , doc.height + doc.bottomMargin + doc.topMargin- 60 )
    # Draw the phone number on the next line
    if user.id == 2:
        number = '0300-1607055'
    else:
        number = '+92 300 7364951'
    phone_number = f"Contact Us: {number}  Developed By: 03701601334"
    canvas.drawString(doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - 55, phone_number)
    canvas.drawString(doc.leftMargin-70, doc.height + doc.bottomMargin + doc.topMargin - 150, date)
    canvas.restoreState()
    
# Define the function to draw the header on later pages
def createPDF(request, pk, model, start_at, end_at):
    obj = get_obj(pk, model)
    combined_data = ledger_generate(obj, model, start_at, end_at)
    if not combined_data:
        return None
    doc = SimpleDocTemplate("report.pdf", pagesize=A4)
    
    heading_style, purchase, payment = pdf_styles()
    title = f"Name: {obj.name} <br/> Opening Balance: {obj.opening_balance} <br/> Closing Balance: {combined_data[-1]['total']}"
    
    table_data = []
    headers=['DATE','PNR', 'PASSENGER', 'PURCHASE', 'PAYMENT', 'BALANCE']
    table_data.append(headers)
    for entry in combined_data:
        if entry.get('pnr'):
            message = str(entry['purchase']) if model == 'supplier' else str(entry['sale'])
            ticket_row = [
                entry['created_at'].strftime('%d %b '),
                entry['pnr'],
                entry['passenger'],
                Paragraph(f"Rs: {message}", purchase), 
                 '',  # Leave these cells empty
                f"Rs: {entry['total']}"
            ]
            table_data.append(ticket_row)
        else:
            ledger_row = [
                entry['payment_date'].strftime('%d %b'),
                '', '', '',  # Leave these cells empty
                 Paragraph(f"Rs: {entry['payment']}", payment),
                f"Rs: {entry['total']}"
            ]
            table_data.append(ledger_row)

    # Create the table
    table = Table(table_data, style=[
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    	('GRID', (0, 0), (-1, -1), 1, colors.black),
    	('AUTOCOLWIDTH', (0, 0), (-1, -1))
    ], colWidths=[0.7*inch, 1*inch, 2.5*inch, 1.3*inch, 1.3*inch, 1.5*inch],
    	rowHeights=0.5*inch)
    elements = []
    elements.append(Paragraph(title, heading_style))
    elements.append(table)
    doc.build(elements, onFirstPage=partial(drawHeader, start_at=start_at, end_at=end_at, user=request.user))
    file_reponse = FileResponse(open("report.pdf", "rb"), as_attachment=True, filename='report.pdf')
    return file_reponse

def pdf_styles():
    styles = getSampleStyleSheet()
    
    heading_style = ParagraphStyle(
        'heading_style',
        parent=styles['Heading1'],
        fontSize=14,  # Adjust the font size as needed
        spaceAfter=12,  # Add some space after the paragraph
        alignment=1  # Center alignment (0=left, 1=center, 2=right)
    )
    purchase = ParagraphStyle(
        'purchase',
        parent=styles['BodyText'],
        textColor=colors.HexColor('#FA4646'),
        fontSize=12,
		alignment=1
    )
    payment = ParagraphStyle(
                'payment',
                parent=styles['BodyText'],
                textColor=colors.HexColor('#4ADE80'),
                fontSize=12,
				alignment=1
            )
    return heading_style, purchase, payment