from django.db import models
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

class Ticket(models.Model):
    TICKET_TYPES = [
        ('IS', 'Issues'),
        ('RF', 'Refund'),
        ('RI', 'ReIssue'),
        ('VO', 'Void'),
    ]
    # number=models.PositiveIntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    pnr = models.CharField(max_length=100, blank=False, null=False)
    sector = models.CharField(max_length=255, blank= True, null=True)
    passenger = models.CharField(max_length=255, blank= True, null=True)
    travel_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    airline = models.CharField(max_length=255, blank= True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=False, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False, null=False)
    sale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ticket_type = models.CharField(max_length=2,choices=TICKET_TYPES,default='Issues', blank=False, null=False)
    # narration= models.TextField(blank=True, null=True, default="")
    def __str__(self):
        return (
        f"Ticket with PNR: {self.pnr}<br>"
        f"Travel Date: {self.travel_date}<br>"
        f"Supplier: {self.supplier}<br>"
        f"Customer: {self.customer}<br>"
        f"Passenger: {self.passenger}"
        )

        
class Ledger(models.Model):
    Status_Choices = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateTimeField(default=timezone.now)
    description= models.TextField( blank=True, null=True, default="")
    # status = models.CharField(max_length=1,choices=Status_Choices,default='P', blank=False, null=False)
    
def __str__(self):
    return f"By {self.user}  {self.payment} to {self.supplier} on {self.payment_date}"

class RialPrice(models.Model):
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
    ]
    DURATION_TYPE = [
        ('36', '36 Hours'),
        ('96', '96 Hours'),
        ('1m', '1 Month'),
        ('2m', '2 Months'),
        ('3m', '3 Months'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rial_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 )
    pkr_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    sale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    visa_type = models.CharField(max_length = 2, choices=VISA_TYPE, blank= False, null= False)
    duration = models.CharField(max_length=2, choices=DURATION_TYPE, blank = False, null = False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Rail {self.rial_price} PKR {self.pkr_price}  Visa {self.visa_type} Duration {self.duration} Sale {self.sale} Purchase {self.purchase}"