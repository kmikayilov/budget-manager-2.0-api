from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, models

# Create your views here.

class createTransactionView(generics.CreateAPIView):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.MakeTransactionSerializer
    
    def post(self, request, format=None):
        categoryQuerySet = models.Category.objects.filter(id = request.data['transaction']['categoryId'])
        if categoryQuerySet.exists():
            category = categoryQuerySet[0]
        else:
            Response({"Category not found": "Invalid category id"}, status=status.HTTP_404_NOT_FOUND)

        paymentQuerySet = models.PaymentMethod.objects.filter(id = request.data['transaction']['paymentId'])
        if paymentQuerySet.exists():
            payment = paymentQuerySet[0]
        else:
            Response({"Payment method not found": "Invalid payment method id"}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            "amount": request.data['transaction']['transactionAmount'],
            "date": request.data['transaction']['transactionDate'],
            "category": category,
            "payment": payment
        }

        transaction = models.Transaction(transactionAmount=data["amount"], transactionDate=data["date"], category=data["category"], payment=data["payment"])
        transaction.save()

        return Response(serializers.TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

class TransactionView(APIView):

    def get_transaction(self, transaction_id):
        try: 
            transaction = models.Transaction.objects.filter(id=transaction_id)[0]
            return transaction
        except models.Transaction.DoesNotExist:
            return Response({"Transaction not found": "Invalid transaction id"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, transaction_id):
        if transaction_id == None:
            return Response({"Bad request": "Id param not found in request"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.TransactionSerializer(self.get_transaction(transaction_id))
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, transaction_id):
        if transaction_id == None:
            return Response({"Bad request": "Id param not found in request"}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction = self.get_transaction(transaction_id)

        if transaction.category.id != request.data['transaction']['categoryId']:
            categoryQuerySet = models.Category.objects.filter(id = request.data['transaction']['categoryId'])
            if categoryQuerySet.exists():
                category = categoryQuerySet[0]
            else:
                Response({"Category not found": "Invalid category id"}, status=status.HTTP_404_NOT_FOUND)
            
            transaction.category = category

        if transaction.payment.id != request.data['transaction']['paymentId']:
            paymentQuerySet = models.PaymentMethod.objects.filter(id = request.data['transaction']['paymentId'])
            if paymentQuerySet.exists():
                payment = paymentQuerySet[0]
            else:
                Response({"Payment method not found": "Invalid payment method id"}, status=status.HTTP_404_NOT_FOUND)
            
            transaction.payment = payment
        
        if transaction.transactionAmount != request.data['transaction']['transactionAmount']:
            transaction.transactionAmount = request.data['transaction']['transactionAmount']
         
        if transaction.transactionDate != request.data['transaction']['transactionDate']:
            transaction.transactionDate = request.data['transaction']['transactionDate']

        transaction.save()
       
        return Response(serializers.TransactionSerializer(transaction).data, status=status.HTTP_200_OK)

    def delete(self, request, transaction_id):
        print(transaction_id)
        print(request.data['transaction'])
        
        if transaction_id == None:
            return Response({"Bad request": "Id param not found in request"}, status=status.HTTP_400_BAD_REQUEST)

        transaction = self.get_transaction(transaction_id)
        transaction.delete()
        return Response({"Success": "Transaction successfully deleted!"}, status=status.HTTP_200_OK)