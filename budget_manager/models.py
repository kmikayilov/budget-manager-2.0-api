from django.db import models

# Create your models here.

class Accounting(models.Model):
    accounting_type = models.CharField(max_length=50, null=True)
    coefficient = models.IntegerField(null=True)

    def __str__(self):
        return self.accounting_type

class Category(models.Model):
    category = models.CharField(max_length=50, null=True)
    accounting = models.ForeignKey(Accounting, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.id} {self.category} ({self.accounting.id})"

class PaymentMethod(models.Model):
    method = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.method
   
class Transaction(models.Model):
    transactionAmount = models.CharField(max_length=50, null=True)
    transactionDate = models.DateField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    payment = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.transactionAmount} ({self.transactionDate}, {self.category.category}, {self.payment.method})"