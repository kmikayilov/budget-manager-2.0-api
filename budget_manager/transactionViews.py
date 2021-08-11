from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

# from django.models.db import Q
from django.db.models import Q
from . import serializers, models

# Create your views here.


class createTransactionView(generics.CreateAPIView):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.MakeTransactionSerializer

    def post(self, request, format=None):
        data = {}
        new_transaction = request.data.get('transaction', {})

        categoryQuerySet = models.Category.objects.filter(
            id=new_transaction.get('categoryId', 0))
        if categoryQuerySet.exists():
            data['category'] = categoryQuerySet.first()
        else:
            Response({"Category not found": "Invalid category id"},
                     status=status.HTTP_404_NOT_FOUND)
        

        paymentQuerySet = models.PaymentMethod.objects.filter(
            id=new_transaction.get('paymentId', 0))
        if paymentQuerySet.exists():
            data['payment'] = paymentQuerySet.first()
        else:
            Response({"Payment method not found": "Invalid payment method id"},
                    status=status.HTTP_404_NOT_FOUND)
        

        data["transactionAmount"] = new_transaction.get('transactionAmount', 0)
        data["transactionDate"] =  new_transaction.get('transactionDate', datetime.today())
    
        transaction = models.Transaction(**data)
        transaction.save()

        return Response(serializers.TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


class TransactionView(APIView):
    def get_transaction(self, transaction_id):
        try:
            transaction = models.Transaction.objects.filter(id=transaction_id).first()
            return transaction
        except models.Transaction.DoesNotExist:
            return Response({"Transaction not found": "Invalid transaction id"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, transaction_id):
        if transaction_id == None:
            return Response({"Bad request": "Id param not found in request"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.TransactionSerializer(
            self.get_transaction(transaction_id))
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, transaction_id):
        if transaction_id == None:
            return Response({"Bad request": "Id param not found in request"}, status=status.HTTP_400_BAD_REQUEST)

        transaction = self.get_transaction(transaction_id)
        
        new_transaction = request.data.get('transaction', {})

        if transaction.category.id != new_transaction.get('categoryId', 0):
            categoryQuerySet = models.Category.objects.filter(
                id=new_transaction.get('categoryId', 0))
            if categoryQuerySet.exists():
                category = categoryQuerySet.first()
            else:
                Response({"Category not found": "Invalid category id"},
                         status=status.HTTP_404_NOT_FOUND)

            transaction.category = category
    

        if transaction.payment.id != new_transaction.get('paymentId', 0):
            paymentQuerySet = models.PaymentMethod.objects.filter(
                id=new_transaction.get('paymentId', 0))
            if paymentQuerySet.exists():
                payment = paymentQuerySet.first()
            else:
                Response({"Payment method not found": "Invalid payment method id"},
                        status=status.HTTP_404_NOT_FOUND)

            transaction.payment = payment

        if transaction.transactionAmount != new_transaction.get('transactionAmount', 0):
            transaction.transactionAmount = new_transaction.get('transactionAmount', 0)

        if transaction.transactionDate != new_transaction.get('transactionDate', 0):
            transaction.transactionDate = new_transaction.get('transactionDate', 0)

        transaction.save()

        return Response(serializers.TransactionSerializer(transaction).data, status=status.HTTP_200_OK)

    def delete(self, request, transaction_id):
        if transaction_id == None:
            return Response({"Bad request": "Id param not found in request"}, status=status.HTTP_400_BAD_REQUEST)

        transaction = self.get_transaction(transaction_id)
        transaction.delete()
        return Response({"Success": "Transaction successfully deleted!"}, status=status.HTTP_200_OK)


class FilterTransactions(generics.CreateAPIView):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer

    def order_by(self, order, field):
        sign = '-' if order == 'desc' else '' 
        if field == 'id' or field == 'transactionAmount' or field == 'transactionDate' or field == 'payment_id' or field == 'category_id':
            val = sign + field
        else:
            val = sign + 'category__accounting'
        
        return val

    def post(self, request, format=None):
        data = {}

        query = self.get_queryset()
        data['transactionCount'] = self.get_queryset().count()
        
        req = request.data
        filterObject = req['filters']
      
        and_condition = Q()
        for filter in filterObject:
            if filter == 'id' or filter == 'transactionAmount' or filter == 'transactionDate':
                and_condition.add(Q(**{"{}__icontains".format(filter):filterObject[filter]}), Q.AND)

            if filter == 'category_id' or filter == 'payment_id':
                and_condition.add(Q(**{filter: filterObject[filter]}), Q.AND)
            
            if filter == "accounting_id":
                and_condition.add(Q(**{"category__accounting": filterObject[filter]}), Q.AND)

        query = self.get_queryset().filter(and_condition)
        
        if 'sortField' in req:
            order = self.order_by(req['sortOrder'], req['sortField'])
            query = query.order_by(order)
        
        
        objectsList = serializers.TransactionSerializer(query, many=True).data
        data["transactions"] = objectsList[req['offset']:req['offset']+req['limit']]

        return Response(data, status=status.HTTP_200_OK)