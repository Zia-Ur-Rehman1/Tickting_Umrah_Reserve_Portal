# forms.py
from django import forms
from .models import *
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Row,Column
class TicketForm(forms.ModelForm):
    airline= forms.CharField( required=False)
    passenger = forms.CharField( required=False)
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=True, widget=forms.Select())
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=True, widget=forms.Select())
    issued_by = forms.ModelChoiceField(queryset=Issued.objects.all(), required=False, widget=forms.Select())
    travel_date = forms.DateField(required=False)
    return_date = forms.DateField(required=False)
    sale = forms.DecimalField(localize=True)
    purchase = forms.DecimalField(localize=True)
    ticket_type = forms.ChoiceField(required=True, choices=Ticket.TICKET_TYPES)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TicketForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['customer'].queryset = Customer.objects.filter(user=user)
            self.fields['supplier'].queryset = Supplier.objects.filter(user=user)
            self.fields['issued_by'].queryset = Issued.objects.filter(user=user)
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
class DateForm(forms.Form):
    start_at = forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'}), label="From" )
    end_at = forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'}), label="Today")
    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('profit')
        self.helper.add_input(Submit('submit', 'Submit', css_class='bg-blue-500 hover:bg-blue-700 text-white font-bold ml-8 py-2 px-4 rounded mt-2'))
    
class LedgerForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False, widget=forms.Select())
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False, widget=forms.Select())
    bank = forms.ModelChoiceField(queryset=Bank.objects.all(), required=True, widget=forms.Select())
    
    payment=forms.DecimalField(localize=True)
    description = forms.Textarea()
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LedgerForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['customer'].queryset = Customer.objects.filter(user=user)
            self.fields['supplier'].queryset = Supplier.objects.filter(user=user)
            self.fields['bank'].queryset = Bank.objects.filter(user=user)
  
    class Meta:
        model = Ledger
        fields = '__all__'
        widgets = {
            'payment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form_input'}),
             'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
             'transaction_type': forms.RadioSelect,
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
    def get_model_name(self):
        return 'Supplier'
class CustomerForm(forms.ModelForm):
    name = forms.CharField(required= True)
    opening_balance = forms.DecimalField(localize=True)
    class Meta:
        model = Customer  # Specify the model here
        fields = ['name', 'opening_balance', 'user']
        widgets = {
             'user': forms.TextInput(attrs={'type': 'hidden'}),
                 }
    def get_model_name(self):
        return 'Customer'


class UploadForm(forms.Form):
    file = forms.FileField(label='Upload File')
    
class VisaForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False, widget=forms.Select())
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False, widget=forms.Select())
    duration = forms.ChoiceField(required=True, choices=Visa.DURATION_TYPE)
    visa_type = forms.ChoiceField(required=True, choices=Visa.VISA_TYPE)
    sale = forms.DecimalField(localize=True)
    purchase = forms.DecimalField(localize=True)
    sale_pkr = forms.DecimalField(localize=True)
    purchase_pkr = forms.DecimalField(localize=True)
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
            'visa_type': forms.Select(choices=Visa.VISA_TYPE),
            'duration': forms.Select(choices=Visa.DURATION_TYPE),
            
        }
        
class RiyalPriceForm(forms.ModelForm):
    
    class Meta:
        model = RiyalPrice
        fields = '__all__'

     
class HotelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(HotelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        # self.helper.form_action = reverse('hotel_create')
        # self.helper.add_input(Submit('submit', 'Submit', css_class='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-8'))
        
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user
    class Meta:
        model = Hotel
        fields = '__all__'
class BankForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BankForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        if user:
            self.fields['user'].widget = forms.HiddenInput()
            self.fields['user'].initial = user

    class Meta:
        model= Bank
        fields = '__all__'


class HotelVoucherForm(forms.Form):
    city = forms.ChoiceField(choices=[('', '---------')] + (Hotel.CITY_CHOICES))
    hotel = forms.ChoiceField()
    room = forms.ChoiceField()
    start_at = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}), label="From" )
    end_at = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}), label="To")
    nights = forms.IntegerField(required=False, label="Nights",widget=forms.NumberInput(attrs={'readonly': 'readonly' }))
    def __init__(self, *args, **kwargs):
        super(HotelVoucherForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('hotel', css_class='form-group col-md-6 mb-0'),
                Column('room', css_class='form-group col-md-6 mb-0'),
                Column('start_at', css_class='form-group col-md-6 mb-0'),
                Column('end_at', css_class='form-group col-md-6 mb-0'),
                Column('nights', css_class='form-group col-md-6 mb-0'),
                css_class='grid grid-cols-4 lg:grid-cols-6 md:grid-cols-6 gap-x-8 gap-y-6 sm:grid-cols-2'
                
            ),
        )
        if self.initial.get('city') is not  None:
            self.fields['hotel'].choices = [(hotel.id, hotel.hotel_name) for hotel in Hotel.objects.filter(city=self.initial['city'])]
        if self.initial.get('hotel') is not None:
            self.fields['room'].choices = [(room.id, room.get_room_type_display()) for room in RoomRate.objects.filter(hotel=self.initial['hotel'])]
class TransportForm(forms.Form):
    transport = forms.TypedChoiceField(
        required=False,
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.RadioSelect,
        initial=False,
        label="Want Company Transport?"
    )    
class VisaSearchForm(forms.Form):
    visa = forms.ModelMultipleChoiceField(queryset=Visa.objects.all(), required=False, widget=forms.SelectMultiple())
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        initial_visas = kwargs.get('initial', {}).get('visa', [])
        used_visas = Voucher.objects.filter(user=user).values_list('visas', flat=True).distinct()
        if initial_visas:
            self.fields['visa'].initial = initial_visas
            initial_visas = initial_visas.values_list('id', flat=True) 
            used_visas = [visa_id for visa_id in used_visas if visa_id not in initial_visas]

        self.fields['visa'].queryset =Visa.objects.filter(user=user).exclude(id__in=used_visas)
        
class TripForm(forms.Form):
    flight = forms.CharField(max_length=100, required=True)
    sector = forms.CharField(max_length=100, required=True)
    departure = forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'}) )
    arrival = forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('flight', css_class='form-group col-md-6 mb-0'),
                Column('sector', css_class='form-group col-md-6 mb-0'),
                Column('departure', css_class='form-group col-md-6 mb-0'),
                Column('arrival', css_class='form-group col-md-6 mb-0'),
                css_class='grid grid-cols-4 lg:grid-cols-6 md:grid-cols-6 gap-x-8 gap-y-6 sm:grid-cols-2'
                
            ),
        )
class RoomRateForm(forms.ModelForm):
    riyal_rate = forms.DecimalField(required=False,widget=forms.HiddenInput())
    pkr_price = forms.DecimalField(required=False,widget=forms.HiddenInput())
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), required=False, widget=forms.Select())
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    room_type = forms.ChoiceField(choices=RoomRate.ROOM_CATEGORY, required=False, widget=forms.Select())
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RoomRateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user
        if user:
           self.fields['hotel'].queryset = Hotel.objects.filter(user=user)
    
    class Meta:
        model = RoomRate
        fields = '__all__'
