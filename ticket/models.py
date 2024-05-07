from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name}"

class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.name}"
class Issued(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issued_by=models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.issued_by}"

class Ticket(models.Model):
    TICKET_TYPES = [
        ('IS', 'Issues'),
        ('RF', 'Refund'),
        ('RI', 'ReIssue'),
        ('VO', 'Void'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    pnr = models.CharField(max_length=100, blank=False, null=False)
    sector = models.CharField(max_length=255, blank= True, null=True)
    passenger = models.CharField(max_length=255, blank= True, null=True)
    travel_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    airline = models.CharField(max_length=255, blank= True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=False, null=False, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False, null=False, db_index=True)
    sale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ticket_type = models.CharField(max_length=2,choices=TICKET_TYPES,default='Issues', blank=False, null=False)
    narration= models.TextField(blank=True, null=True, default="")
    excel_id= models.PositiveIntegerField(null=True, blank=True, default=0)
    issued_by=models.ForeignKey(Issued, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return (
        f"Ticket with PNR: {self.pnr}<br>"
        f"Travel Date: {self.travel_date}<br>"
        f"Supplier: {self.supplier}<br>"
        f"Customer: {self.customer}<br>"
        f"Passenger: {self.passenger}"
        )

class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

class Ledger(models.Model):
    Status_Choices = [
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Rejected'),
    ]
    TRANSACTION_TYPE=[
        (0, 'Debit'),
        (1, 'Credit'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, blank=True, null=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True, db_index=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateTimeField(default=timezone.now)
    description= models.TextField( blank=True, null=True, default="")
    status = models.SmallIntegerField(choices=Status_Choices,default=1, blank=True, null=True)
    transaction_type = models.SmallIntegerField(choices=TRANSACTION_TYPE, blank=True,null=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='ledgers', null=True, blank=True, db_index=True)
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.bank:
            if self.transaction_type == self.DEBIT:
                if self.bank.balance < self.payment:
                    raise ValidationError("Insufficient balance in bank.")
                else:
                    self.bank.balance -= self.payment
            elif self.transaction_type == self.CREDIT:
                self.bank.balance += self.payment
            self.bank.save()
        super().save(*args, **kwargs)
def __str__(self):
    return f"By {self.user}  {self.payment} to {self.supplier} on {self.payment_date}"

class RiyalPrice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)
    
    def __str__(self):
        return f"Price {self.price}"
class Visa(models.Model):
    VISA_TYPE = [
        ('DV', 'Dubai Visit'),
        ('SV', 'Saudia Visit'),
        ('DW', 'Dubai Work'),
        ('SW', 'Saudia Work'),
        ('UV', 'Umrah Visa' ), 
        ('HV', 'Hajj Visa' ), 
    ]
    DURATION_TYPE = [
        ('36', '36 Hours'),
        ('96', '96 Hours'),
        ('1m', '1 Month'),
        ('2m', '2 Months'),
        ('3m', '3 Months'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    riyal_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 )
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, blank=True, null=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True, db_index=True)
    sale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    sale_pkr = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    purchase_pkr = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    pass_name= models.CharField(max_length=255, blank=True, null= True)
    pass_num= models.CharField(max_length=10, blank=True, null= True, db_index=True)

    visa_type = models.CharField(max_length = 2, choices=VISA_TYPE, blank= False, null= False)
    duration = models.CharField(max_length=2, choices=DURATION_TYPE, blank = False, null = False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pass_name} / {self.pass_num}"
class Hotel(models.Model):
    CITY_CHOICES = [
        (0, 'Madinah'),
        (1, 'Makkah'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    area= models.CharField(max_length=255, blank=True, null=True)
    distance = models.PositiveIntegerField()
    city = models.SmallIntegerField( choices=CITY_CHOICES, blank=True, null=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.get_city_display()} {self.hotel_name} {self.area} {self.distance}m  "
class RoomRate(models.Model):
    ROOM_CATEGORY = [
        (0, 'Private'),
        (1, 'Sharing'),
        (2, 'Quadripple'),
        (3, 'Tripple'),
        (4, 'Double'),
    ]
    room_type = models.SmallIntegerField( choices=ROOM_CATEGORY, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel= models.ForeignKey(Hotel, on_delete=models.CASCADE)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    riyal_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 )
    riyal_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 )
    pkr_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Price for {self.get_room_type_display()} on {self.date_from} to {self.date_to} is {self.pkr_price} with {self.riyal_rate}"        
class Trip(models.Model):
    flight= models.CharField(max_length=10)
    sector= models.CharField(max_length=50)
    departure = models.DateField(blank=True, null=True)
    arrival = models.DateField(blank=True, null=True)
    
class HotelBooking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    voucher = models.ForeignKey('Voucher', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()    
    nights = models.PositiveIntegerField()
class Voucher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotels = models.ManyToManyField(Hotel, through=HotelBooking)
    visas = models.ManyToManyField(Visa, db_index=True)
    trip = models.ManyToManyField(Trip)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    transport = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        # Delete associated trips
        self.trip.all().delete()
        super().delete(*args, **kwargs)