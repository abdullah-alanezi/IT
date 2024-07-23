from django.contrib import admin
from .models import MaintenanceRequest,PrinterRequest
# Register your models here.


admin.site.register(MaintenanceRequest)
admin.site.register(PrinterRequest)