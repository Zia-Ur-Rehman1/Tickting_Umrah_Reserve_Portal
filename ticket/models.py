from django.db import models
from django.utils import timezone
# Create your models here.

    
class Customer(models.Model):
    name = models.CharField(max_length=255)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_balance(self):
        total_purchase = Ticket.objects.filter(customer=self).aggregate(models.Sum('purchase'))['purchase__sum'] or 0
        total_payment = Ledger.objects.filter(customer=self).aggregate(models.Sum('payment'))['payment__sum'] or 0
        balance = self.opening_balance + total_purchase - total_payment

        return balance
    def __str__(self):
        return f"{self.name}"

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def calculate_balance(self):
        total_purchase = Ticket.objects.filter(supplier=self).aggregate(models.Sum('purchase'))['purchase__sum'] or 0
        total_payment = Ledger.objects.filter(supplier=self).aggregate(models.Sum('payment'))['payment__sum'] or 0
        balance = self.opening_balance + total_purchase - total_payment

        return balance
    def __str__(self):
        return f"{self.name}"

class Ticket(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    pnr = models.CharField(max_length=10, blank=False, null=False)
    sector = models.CharField(max_length=100, blank= True, null=True)
    passenger = models.CharField(max_length=100, blank= True, null=True)
    travel_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    airline = models.CharField(max_length=100, blank= True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=False, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False, null=False)
    sale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return (
        f"Ticket with PNR: {self.airline}<br>"
        f"Travel Date: {self.travel_date}<br>"
        f"Supplier: {self.supplier}<br>"
        f"Customer: {self.customer}<br>"
        f"Passenger: {self.passenger}"
        )

        
class Ledger(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateTimeField(default=timezone.now)
    description= models.TextField( blank=True, null=True, default="")
    
def __str__(self):
    return f"  {self.payment} to {self.supplier} on {self.payment_date}"