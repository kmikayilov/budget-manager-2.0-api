from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import jwt
import datetime

from . import serializers, models

# Register API


class RegisterView(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(
            data=request.data.get('user', {}))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#  {
#  "user": {
#      "email": "",
#      "username": '',
#      "password": ""
#  }
# }


class LoginView(APIView):
    def post(self, request):
        data = request.data.get('user', {})
        email = data.get('email', '')
        password = data.get('password', '')

        user = models.User.objects.filter(email=email).first()

        if user is None:
            return Response({"message": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"message": "Password is incorrect!"}, status=status.HTTP_404_NOT_FOUND)

        payload = {
            "token_type": "access",
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, "secret",
                           algorithm='HS256')

        return Response({
            'user': serializers.UserSerializer(user).data,
            'token': token
        }, status=status.HTTP_200_OK)


#  {
#  "user": {
#      "email": "kenan.mikayilov.00@gmail.com",
#      "password": "KM_jr2000"
#  }
# }

class UserView(APIView):
    
    def get(self, request):
        token = request.headers.get('Authorization', None)[7:]
      
        if not token:
            return Response({"message": "Unauthorized!"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, "secret", algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"message": "Unauthorized!"}, status=status.HTTP_401_UNAUTHORIZED)

        user = models.User.objects.filter(id=payload.get('id', 0)).first()

        return Response({
            "user": serializers.UserSerializer(user).data,
            "token": token
        }, status=status.HTTP_200_OK)
