from rest_framework import viewsets, permissions, response, status, generics
from ..serializers import UserSerializer, AccountingSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from ..models import Accounting

@api_view(['GET', 'POST'])
def accounting_list(request):
    """
    List all accounting, or create a new accounting.
    """
    if request.method == 'GET':
        accounting = Accounting.objects.all()
        serializer = AccountingSerializer(accounting, many=True)
        return response.Response(serializer.data)

    elif request.method == 'POST':
        serializer = AccountingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def accounting_detail(request, pk):
    """
    Retrieve, update or delete an accounting.
    """
    try:
        accounting = Accounting.objects.get(pk=pk)
    except Accounting.DoesNotExist:
        return response.Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountingSerializer(accounting)
        return response.Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AccountingSerializer(accounting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        accounting.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)