from django.contrib import admin
from . import models 

admin.site.register(models.MpesaPayment)
admin.site.register(models.Payment)