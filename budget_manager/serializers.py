from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import models


class RegistationSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(max_length=50, min_length=6)
    username = serializers.CharField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    
    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ("email already exists")})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": ("username already exists")})
        
        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)
    class Meta:
        model = User
        fields = ('username', 'password')

#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         return data


from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid=decoded_payload['user_id']
        # add filter query
        # data.update({'custom_field': 'custom_data')})
        return data

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
