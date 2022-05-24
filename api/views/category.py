from rest_framework import viewsets, permissions
from ..models import Category
from ..serializers import UserSerializer, CategorySerializer
from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, response, status, generics
from ..serializers import UserSerializer, AccountingSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from ..models import Accounting

# Category VIEWSET

@api_view(['GET', 'POST'])
def category_list(request):
    """
    List all category, or create a new category.
    """
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return response.Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    """
    Retrieve, update or delete an category.
    """
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return response.Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return response.Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def category_filter(request, accounting_id):
    """
    Retrieve categories by accounting id.
    """
    try:
        category = Category.objects.get(accounting__id=accounting_id)
    except Category.DoesNotExist:
        return response.Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return response.Response(serializer.data)