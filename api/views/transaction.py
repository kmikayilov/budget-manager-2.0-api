from rest_framework import viewsets, permissions
from .. import serializers, models
from ..serializers import UserSerializer
from django.contrib.auth.models import User

# Transaction VIEWSET

class transactionsView(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

transaction_list = transactionsView.as_view({ 'get': 'list' })
transaction_post = transactionsView.as_view({ 'post': 'create' })
transaction = transactionsView.as_view({ 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' })
