"""
URL configuration for ticket_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ticket.views import ticket_list, ticket_create, ticket_update, ticket_delete, generateCSV, search, ledger_create, ledger_list,ledger_update,supplier_list,supplier_create, supplier_update, customer_create, customer_list,customer_update, supplier_ledger
from ticket.csv_manipulation import upload_csv
urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('tickets/', ticket_list, name='ticket_list'),
    path('tickets/csv', generateCSV, name='get_csv'),
    path('tickets/create/', ticket_create, name='ticket_create'),
    path('tickets/<int:pk>/update/', ticket_update, name='ticket_update'),
    path('tickets/<int:pk>/delete/', ticket_delete, name='ticket_delete'),
    path('tickets/search/', search, name='search'),
    path('ledgers/', ledger_list, name='ledger_list'),
    path('ledgers/create/', ledger_create, name='ledger_create'),
    path('ledgers/<int:pk>/update/', ledger_update, name='ledger_update'),
    # path('ledgers/<int:pk>/delete/', ledger_delete, name='ledger_delete'),
    path('suppliers/', supplier_list, name='supplier_list'),
    path('suppliers/create/', supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/update/', supplier_update, name='supplier_update'),
    path('customers/create/', customer_create, name='customer_create'),
    path('customers/<int:pk>/update/', customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', customer_update, name='customer_delete'),
    path('customers/', customer_list, name='customer_list'),
    path('ledgers/supplier/<int:pk>', supplier_ledger, name='supplier_ledger'),
    
    path('tickets/upload/', upload_csv, name='upload_file'),
    path("__debug__/", include("debug_toolbar.urls")),
]
