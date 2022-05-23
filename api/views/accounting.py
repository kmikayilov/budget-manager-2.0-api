from rest_framework import viewsets, permissions, response, status
from .. import serializers, models
from ..serializers import UserSerializer
from django.contrib.auth.models import User

# Accounting VIEWSET

class accountingsView(viewsets.ModelViewSet):
    queryset = models.Accounting.objects.all()
    serializer_class = serializers.AccountingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
accounting_list = accountingsView.as_view({ 'get': 'list' })
accounting_post = accountingsView.as_view({ 'post': 'create' })
accounting = accountingsView.as_view({ 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' })
