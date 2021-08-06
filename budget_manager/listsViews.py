from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers, models

# Create your Lists views here.


class categoriesView(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get(self, request, format=None):
        print(request.headers)
        objects = self.get_queryset()
        objectsList = serializers.CategorySerializer(objects, many=True).data
        data = {
            "categories": objectsList or [],
            "categoriesCount": len(objects)
        }
        return Response(data, status=status.HTTP_200_OK)


class accountingsView(generics.ListCreateAPIView):
    queryset = models.Accounting.objects.all()
    serializer_class = serializers.AccountingSerializer

    def get(self, request, format=None):
        objects = self.get_queryset()
        objectsList = serializers.AccountingSerializer(objects, many=True).data
        data = {
            "accountings": objectsList or [],
            "accountingsCount": len(objects)
        }
        return Response(data, status=status.HTTP_200_OK)


class paymentsView(generics.ListCreateAPIView):
    queryset = models.PaymentMethod.objects.all()
    serializer_class = serializers.PaymentMethodSerializer

    def get(self, request, format=None):
        objects = self.get_queryset()
        objectsList = serializers.PaymentMethodSerializer(
            objects, many=True).data
        data = {
            "payments": objectsList or [],
            "paymentsCount": len(objects)
        }
        return Response(data, status=status.HTTP_200_OK)


class transactionsView(generics.ListCreateAPIView):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer

    def get(self, request, format=None):
        objects = self.get_queryset()
        objectsList = serializers.TransactionSerializer(
            objects, many=True).data
        data = {
            "transactions": objectsList or [],
            "transactionsCount": len(objects)
        }
        return Response(data, status=status.HTTP_200_OK)
