from django.contrib import admin
from .models import MaintenanceRequest,PrinterRequest,ItHelp,PrinterHelp,Chat
# Register your models here.


admin.site.register(MaintenanceRequest)
admin.site.register(PrinterRequest)
admin.site.register(ItHelp)
admin.site.register(PrinterHelp)
admin.site.register(Chat)