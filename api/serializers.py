from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class AccountingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Accounting
        fields = ('id', 'accounting_type', 'coefficient')

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('id', 'category', 'accounting')

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentMethod
        fields = ('id', 'method')

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Transaction
        fields = ('id', 'transactionAmount', 'transactionDate', 'category', 'payment', 'user')

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
