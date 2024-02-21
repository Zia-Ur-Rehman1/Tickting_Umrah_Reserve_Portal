from django.http import FileResponse, HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .ledger_views import *
from .forms import PdfGenerationForm
from django.contrib import messages

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
        

            
def createPDF(request, pk, model, start_at, end_at):
    obj = get_obj(pk, model)
    combined_data = ledger_generate(obj, model, start_at, end_at)
    doc = SimpleDocTemplate("report.pdf", pagesize=A4)
    
    # Define the table data
    table_data = []
    header_content = f"Name: {obj.name} <br/> Opening Balance: {obj.opening_balance} <br/> Total Balance: {combined_data[-1]['total']}"

    headers=['DATE','PNR', 'PASSENGER', 'PURCHASE', 'PAYMENT', 'PAY DATE', 'BALANCE']
    table_data.append(headers)
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
        textColor=colors.white,
        fontSize=10,
        backColor=colors.HexColor('#EF4444'),
        borderColor=colors.HexColor('#EF4444'),
		alignment=1
    )
    payment_date = ParagraphStyle(
                'payment_date',
                parent=styles['BodyText'],
                textColor=colors.black,
                fontSize=10,
                backColor=colors.HexColor('#4ADE80'),
                borderColor=colors.HexColor('#4ADE80'),
				alignment=1
            )

    for entry in combined_data:
        if entry.get('pnr'):
            ticket_row = [
                entry['created_at'].strftime('%d %b '),
                entry['pnr'],
                entry['passenger'],
                Paragraph(f"Rs: {entry['purchase']}", purchase),  # Apply style to "payment" cell
                '', '',  # Leave these cells empty
                f"Rs: {entry['total']}"
            ]
            table_data.append(ticket_row)
        else:
            ledger_row = [
                '',  # Leave PNR cell empty for Ledger
                '', '', '',  # Leave these cells empty
                 Paragraph(f"Rs: {entry['payment']}", payment_date),  # Apply style to "payment" cell
                Paragraph(entry['payment_date'].strftime('%d %b '), payment_date),  # Apply style to "payment date" cell
                f"Rs: {entry['total']}"
            ]
            table_data.append(ledger_row)

    # Create the table
    table = Table(table_data, style=[
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor("#F6F6F6"), colors.white]),
    	('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#F9FAFB")),
    	('AUTOCOLWIDTH', (0, 0), (-1, -1))
    ], colWidths=[0.7*inch, 1*inch, 2.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1.3*inch])

    elements = [
        Paragraph(header_content, heading_style),  # Header content
        table,  # The table
    ]
    doc.build(elements)
    file_reponse = FileResponse(open("report.pdf", "rb"), as_attachment=True, filename='report.pdf')
    return file_reponse