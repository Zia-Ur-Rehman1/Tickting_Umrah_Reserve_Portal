# forms.py
from django import forms
from .models import Ticket, Customer, Supplier, Ledger
class TicketForm(forms.ModelForm):
    airline= forms.CharField( required=False)
    passenger = forms.CharField( required=False)
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=True, widget=forms.Select(attrs={'class': 'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=True, widget=forms.Select(attrs={'class': 'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    travel_date = forms.DateField(required=False)
        
    class Meta:
        model = Ticket
        fields = ['passenger','airline','supplier', 'customer','created_at', 'pnr', 'sector', 'sale', 'purchase', 'travel_date']
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form_input'}),
            'travel_date': forms.DateInput(attrs={'type': 'date', 'class': 'form_input',}),
        }
    
class CsvGenerationForm(forms.Form):
    supplier_name = forms.CharField(required=False)
    customer_name = forms.CharField(required=False)
    start_at = forms.DateField(required=True)
    end_at = forms.DateField(required=True)

class LedgerForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False, widget=forms.Select(attrs={'class': 'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    supplier =forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False, widget=forms.Select(attrs={'class': 'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    payment=forms.IntegerField(required=True)
    class Meta:
        model = Ledger
        fields = ['supplier', 'customer', 'payment', 'payment_date']
        widgets = {
            'payment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form_input'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        supplier = cleaned_data.get('supplier')

        if customer is None and supplier is None:
            raise forms.ValidationError("Either 'customer' or 'supplier' must be selected.")
        
        return cleaned_data

class SupplierForm(forms.ModelForm):
    name = forms.CharField(required= True)
    opening_balance = forms.IntegerField(required= False)
    
    class Meta:
        model = Supplier  # Specify the model here
        fields = ['name', 'opening_balance']  #

class CustomerForm(forms.ModelForm):
    name = forms.CharField(required= True)
    opening_balance = forms.IntegerField(required= False)
    class Meta:
        model = Customer  # Specify the model here
        fields = ['name', 'opening_balance']  #


class UploadForm(forms.Form):
    file = forms.FileField(label='Upload File')