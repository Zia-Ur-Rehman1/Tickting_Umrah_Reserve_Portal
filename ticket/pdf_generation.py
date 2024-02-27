from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Image, TableStyle,Spacer
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
            return response
        else:
            # If the form is not valid, you may want to handle this case
            # For example, you can re-render the form with validation errors
            return render(request, 'generate_pdf.html', {'form': form})

    else:
        suppliers = Supplier.objects.all()
        customers = Customer.objects.all()
        form = PdfGenerationForm()
        return render(request, 'generate_pdf.html', {'form': form, 'suppliers': suppliers, 'customers': customers})
        

# def header(canvas, doc, table):
#     canvas.saveState()
#     w, h = table.wrapOn(canvas, doc.width, doc.topMargin)
#     table.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h)
#     canvas.restoreState()
    
def drawHeader(canvas, doc, start_at, end_at):
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
    company_name = "HASNAIN TRAVEL AND TOURS PRIVATE LIMITED"
    canvas.drawString(doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - 30, company_name)
    # Draw the image on the right end of the page
    img = Image('staticfiles/images/HT.png', width=50, height=50)
    img.drawOn(canvas, doc.width + doc.leftMargin - 30 , doc.height + doc.bottomMargin + doc.topMargin- 60 )
    # Draw the phone number on the next line
    phone_number = "Contact Us: 0300-1607055  Developed By: 03701601334"
    canvas.drawString(doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - 55, phone_number)
    canvas.drawString(doc.leftMargin-70, doc.height + doc.bottomMargin + doc.topMargin - 150, date)
    canvas.restoreState()
    
# Define the function to draw the header on later pages
def createPDF(request, pk, model, start_at, end_at):
    obj = get_obj(pk, model)
    combined_data = ledger_generate(obj, model, start_at, end_at)
    doc = SimpleDocTemplate("report.pdf", pagesize=A4)
    
    heading_style, purchase, payment = pdf_styles()
    img_path = "staticfiles/images/HT.png"  
    img = Image(img_path, height=35, width=35)  
    title = f"Name: {obj.name} <br/> Opening Balance: {obj.opening_balance} <br/> Total Balance: {combined_data[-1]['total']}"
    
    data = [[Paragraph("HASNAIN TRAVEL AND TOURS PRIVATE LIMITED", heading_style), img], ['0300-1607055', '']]

    table_data = []
    headers=['DATE','PNR', 'PASSENGER', 'PURCHASE', 'PAYMENT', 'BALANCE']
    table_data.append(headers)
    for entry in combined_data:
        if entry.get('pnr'):
            ticket_row = [
                entry['created_at'].strftime('%d %b '),
                entry['pnr'],
                entry['passenger'],
                Paragraph(f"Rs: {entry['purchase']}", purchase),  # Apply style to "payment" cell
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
    doc.build(elements, onFirstPage=partial(drawHeader, start_at=start_at, end_at=end_at))
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