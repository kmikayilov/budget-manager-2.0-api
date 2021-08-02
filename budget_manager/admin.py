from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Accounting)
admin.site.register(models.Category)
admin.site.register(models.PaymentMethod)
admin.site.register(models.Transaction)