from rest_framework import viewsets, permissions
from .. import serializers, models
from ..serializers import UserSerializer
from django.contrib.auth.models import User

# Category VIEWSET

class categoriesView(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    
category_list = categoriesView.as_view({ 'get': 'list' })
category_post = categoriesView.as_view({ 'post': 'create' })
category = categoriesView.as_view({ 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' })
