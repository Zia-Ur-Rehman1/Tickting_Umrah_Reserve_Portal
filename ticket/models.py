from django.db import models
from django.utils import timezone
# Create your models here.
class Airline(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Passenger(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=255)
    sale = models.PositiveIntegerField( blank=False, null=False)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    purchase = models.PositiveIntegerField( blank=False, null=False)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    created_at = models.DateField(default=timezone.now)
    pnr = models.CharField(max_length=10, blank=False, null=False)
    sector = models.CharField(max_length=100, blank= True, null=True)
    travel_date = models.DateField()
    airline = models.ForeignKey(Airline, on_delete=models.PROTECT, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, blank=False, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=False, null=False)
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT, blank= True, null=True)

    def __str__(self):
        return f"{self.created_at} - {self.pnr} - {self.airline} - {self.travel_date}"

