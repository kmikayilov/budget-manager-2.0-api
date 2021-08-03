from rest_framework import generics, status
from django.contrib.auth.models import User
from . import serializers
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from knox.models import AuthToken
from django.contrib.auth import (
	authenticate, get_user_model, login as auth_login, logout as auth_logout
)


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = serializers.RegistationSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data['user'])
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "User created successfully",
                "user": serializer.data,

            }, status=status.HTTP_201_CREATED)
    
        return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        username=request.data['user']['username']
        password=request.data['user']['password']
        
        serializer = self.get_serializer(data = request.data['user'])
        if serializer.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                return Response({
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    },
                    "token": AuthToken.objects.create(user)[1],
                }, status=status.HTTP_200_OK)

            return Response({"Error": "There is no such user with this username and password"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        
       