from rest_framework import viewsets, permissions
from .. import serializers, models
from ..serializers import UserSerializer
from django.contrib.auth.models import User

# User VIEWSET

class usersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

user_post = usersView.as_view({ 'post': 'create' })
user = usersView.as_view({ 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' })