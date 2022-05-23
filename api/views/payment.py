from rest_framework import viewsets, permissions
from .. import serializers, models
from ..serializers import UserSerializer
from django.contrib.auth.models import User

# Payment VIEWSET

class paymentsView(viewsets.ModelViewSet):
    queryset = models.PaymentMethod.objects.all()
    serializer_class = serializers.PaymentMethodSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
payment_list = paymentsView.as_view({ 'get': 'list' })
payment_post = paymentsView.as_view({ 'post': 'create' })
payment = paymentsView.as_view({ 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' })
