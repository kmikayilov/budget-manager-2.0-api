from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            "password": { "write_only": True}
        }

    def create(self, validated_data):
        password  = validated_data.pop('password', None)
        instance =  self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance

class AccountingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Accounting
        fields = ('id', 'accounting_type', 'coefficient')

class CategorySerializer(serializers.ModelSerializer):
    accounting = AccountingSerializer()
    class Meta:
        model = models.Category
        fields = ('id', 'category', 'accounting')

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentMethod
        fields = ('id', 'method')

class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    payment = PaymentMethodSerializer()

    class Meta:
        model = models.Transaction
        fields = ('id', 'transactionAmount', 'transactionDate', 'category', 'payment')

class MakeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ('transactionAmount', 'transactionDate', 'category', 'payment')
