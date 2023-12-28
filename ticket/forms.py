# forms.py
from django import forms
from .models import Ticket, Airline, Passenger, Customer, Supplier
from django.core.validators import MinLengthValidator

class TicketForm(forms.ModelForm):
    airline_name = forms.CharField( required=False)
    passenger_name = forms.CharField( required=False)
    customer_name = forms.CharField(max_length=255, required=True)
    supplier_name = forms.CharField(max_length=255, required=True)
    purchase = forms.IntegerField(min_value=1, required=True)
    sale = forms.IntegerField(min_value=1, required=True)

        
    class Meta:
        model = Ticket
        fields = ['created_at', 'pnr', 'sector', 'sale', 'purchase', 'travel_date']
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date', 'class': 'form_input',}, format='%Y-%m-%d'),
            'travel_date': forms.DateInput(attrs={'type': 'date', 'class': 'form_input',}),
        }
    def save(self, commit=True):
        airline_name = self.cleaned_data['airline_name']
        passenger_name = self.cleaned_data['passenger_name']
        customer_name = self.cleaned_data['customer_name']
        supplier_name = self.cleaned_data['supplier_name']
        purchase = self.cleaned_data['purchase']
        sale = self.cleaned_data['sale']

        airline, _ = Airline.objects.get_or_create(name=airline_name)
        passenger, _ = Passenger.objects.get_or_create(name=passenger_name)
        customer, _ = Customer.objects.get_or_create(name=customer_name, sale=sale)
        supplier, _ = Supplier.objects.get_or_create(name=supplier_name, purchase=purchase)

        self.instance.airline = airline
        self.instance.passenger = passenger
        self.instance.customer = customer
        self.instance.supplier = supplier

        return super().save(commit)
    
    
class CsvGenerationForm(forms.Form):
    supplier_name = forms.CharField(required=False)
    customer_name = forms.CharField(required=False)
    start_at = forms.DateField(required=True)
    end_at = forms.DateField(required=True)
