from django.contrib import admin
from .models import Transaction, Category, Accounting, PaymentMethod



# Register your models here.
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Accounting)
admin.site.register(PaymentMethod)
