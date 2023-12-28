from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Ticket)
admin.site.register(Airline)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Passenger)
