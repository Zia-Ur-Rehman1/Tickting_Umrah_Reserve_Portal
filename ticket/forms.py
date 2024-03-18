# forms.py
from django import forms
from .models import Ticket, Customer, Supplier, Ledger, Visa, RialPrice
class TicketForm(forms.ModelForm):
    airline= forms.CharField( required=False)
    passenger = forms.CharField( required=False)
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=True, widget=forms.Select())
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=True, widget=forms.Select())
    travel_date = forms.DateField(required=False)
    return_date = forms.DateField(required=False)
    sale = forms.DecimalField(localize=True)
    purchase = forms.DecimalField(localize=True)
    ticket_type = forms.ChoiceField(required=True, choices=Ticket.TICKET_TYPES)
    # narration = forms.Textarea()
    # number = forms.IntegerField(required=False)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TicketForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['customer'].queryset = Customer.objects.filter(user=user)
            self.fields['supplier'].queryset = Supplier.objects.filter(user=user)
    class Meta:
        model = Ticket
        fields= '__all__'
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form_input'}),
            'travel_date': forms.DateInput(attrs={'type': 'date', 'class': 'form_input'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form_input'}),
            'ticket_type': forms.Select(choices=Ticket.TICKET_TYPES),
        }
    
class CsvGenerationForm(forms.Form):
    supplier_name = forms.CharField(required=False)
    customer_name = forms.CharField(required=False)
    start_at = forms.DateField(required=True)
    end_at = forms.DateField(required=True)

class PdfGenerationForm(forms.Form):
    supplier = forms.CharField(required=False)
    customer = forms.CharField(required=False)
    start_at = forms.DateField(required=True)
    end_at = forms.DateField(required=True)

class LedgerForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False, widget=forms.Select())
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False, widget=forms.Select())
    payment=forms.DecimalField(localize=True)
    description = forms.Textarea()
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LedgerForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['customer'].queryset = Customer.objects.filter(user=user)
            self.fields['supplier'].queryset = Supplier.objects.filter(user=user)
  
    class Meta:
        model = Ledger
        fields = '__all__'
        widgets = {
            'payment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form_input'}),
             'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
    def clean(self):
        super(LedgerForm, self).clean()
        customer = self.cleaned_data.get('customer')
        supplier = self.cleaned_data.get('supplier')
        if customer is None and supplier is None:
            raise forms.ValidationError("Either 'customer' or 'supplier' must be selected.")
        return self.cleaned_data


class SupplierForm(forms.ModelForm):
    name = forms.CharField(required= True)
    opening_balance = forms.DecimalField(localize=True)
    
    class Meta:
        model = Supplier  # Specify the model here
        fields = ['name', 'opening_balance', 'user']
        widgets = {
             'user': forms.TextInput(attrs={'type': 'hidden'}),
                 }

class CustomerForm(forms.ModelForm):
    name = forms.CharField(required= True)
    opening_balance = forms.DecimalField(localize=True)
    class Meta:
        model = Customer  # Specify the model here
        fields = ['name', 'opening_balance', 'user']
        widgets = {
             'user': forms.TextInput(attrs={'type': 'hidden'}),
                 }


class UploadForm(forms.Form):
    file = forms.FileField(label='Upload File')
    
class VisaForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False, widget=forms.Select())
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False, widget=forms.Select())
    duration = forms.ChoiceField(required=True, choices=Visa.DURATION_TYPE)
    visa_type = forms.ChoiceField(required=True, choices=Visa.VISA_TYPE)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VisaForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['customer'].queryset = Customer.objects.filter(user=user)
            self.fields['supplier'].queryset = Supplier.objects.filter(user=user)

    class Meta:
        model = Visa
        fields = '__all__'
        widgets= {
            'visa_tyoe': forms.Select(choices=Visa.VISA_TYPE),
            'duration': forms.Select(choices=Visa.DURATION_TYPE),
            
        }
        
class RialPriceForm(forms.ModelForm):
    
    class Meta:
        model = RialPrice
        fields = '__all__'