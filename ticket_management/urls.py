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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from ticket.views import  *
from ticket.csv_manipulation import upload_csv
from ticket.pdf_generation import *
urlpatterns = [
    path('admin/', admin.site.urls),
    # path("__reload__/", include("django_browser_reload.urls")),
    # path("__debug__/", include("debug_toolbar.urls")),
    path('tickets/', index, name='index'),
    path('get_ticket/', get_ticket, name='get_ticket'),
    path('ticket/login/', login_user, name='login'),    
    path('', login_user, name='login'),
    path('logout_user', logout_user, name='logout_user'),
    path('ticket/', include('django.contrib.auth.urls')),
    path('tickets/csv', generateCSV, name='get_csv'),
    path('tickets/create/', ticket_create, name='ticket_create'),
    path('tickets/urgent/', urgent_tickets, name='urgent_tickets'),
    path('tickets/<int:pk>/update/', ticket_update, name='ticket_update'),
    path('delete/<str:model_name>/<int:pk>/delete/', delete_record, name='delete_record'),
    path('tickets/search/', search, name='search'),
    path('ledgers/', ledger_list, name='ledger_list'),
    path('ledgers/create/', ledger_create, name='ledger_create'),
    path('ledgers/<int:pk>/update/', ledger_update, name='ledger_update'),
    path('suppliers/', supplier_list, name='supplier_list'),
    path('suppliers/create/', supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/update/', supplier_update, name='supplier_update'),
    path('customers/create/', customer_create, name='customer_create'),
    path('customers/<int:pk>/update/', customer_update, name='customer_update'),
    path('customers/', customer_list, name='customer_list'),
    path('ledgers/<str:pk>/<str:model_name>', supplier_ledger, name='supplier_ledger'),
    path('generate_pdf', generatePDF, name='generate_pdf'),
    path('tickets/upload/', upload_csv, name='upload_file'),
    path('visas', visa_list, name='visa_list'),
    path('visa/create', visa_create, name='visa_create'),
    path('visa/update/<int:pk>', visa_update, name='visa_update'),
    path('rialprice/create', rialprice_create, name='rialprice_create'),
    
    
]
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)