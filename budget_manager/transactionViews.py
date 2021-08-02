from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

# from django.models.db import Q

from . import serializers, models

# Create your views here.


class createTransactionView(generics.CreateAPIView):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.MakeTransactionSerializer

    def post(self, request, format=None):
        categoryQuerySet = models.Category.objects.filter(
            id=request.data['transaction']['categoryId'])
        if categoryQuerySet.exists():
            category = categoryQuerySet[0]
        else:
            Response({"Category not found": "Invalid category id"},
                     status=status.HTTP_404_NOT_FOUND)

        paymentQuerySet = models.PaymentMethod.objects.filter(
            id=request.data['transaction']['paymentId'])
        if paymentQuerySet.exists():
            payment = paymentQuerySet[0]
        else:
            Response({"Payment method not found": "Invalid payment method id"},
                     status=status.HTTP_404_NOT_FOUND)

        data = {
            "amount": request.data['transaction']['transactionAmount'],
            "date": request.data['transaction']['transactionDate'],
            "category": category,
            "payment": payment
        }

        transaction = models.Transaction(
            transactionAmount=data["amount"], transactionDate=data["date"], category=data["category"], payment=data["payment"])
        transaction.save()

        return Response(serializers.TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


class TransactionView(APIView):
    def get_transaction(self, transaction_id):
        try:
            transaction = models.Transaction.objects.filter(id=transaction_id)[
                0]
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

        if transaction.category.id != request.data['transaction']['categoryId']:
            categoryQuerySet = models.Category.objects.filter(
                id=request.data['transaction']['categoryId'])
            if categoryQuerySet.exists():
                category = categoryQuerySet[0]
            else:
                Response({"Category not found": "Invalid category id"},
                         status=status.HTTP_404_NOT_FOUND)

            transaction.category = category

        if transaction.payment.id != request.data['transaction']['paymentId']:
            paymentQuerySet = models.PaymentMethod.objects.filter(
                id=request.data['transaction']['paymentId'])
            if paymentQuerySet.exists():
                payment = paymentQuerySet[0]
            else:
                Response({"Payment method not found": "Invalid payment method id"},
                         status=status.HTTP_404_NOT_FOUND)

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


class FilterTransactions(generics.CreateAPIView):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer

    def post(self, request, format=None):
        data = {}
        print(request.data)
        query = self.get_queryset()
        data['transactionsCount'] = self.get_queryset().count()

        for filter in request.data['filters']:
            lookup = "%s__contains" % filter
            value = request.data['filters'][filter]
            print(lookup, value)

        filters = {
            "%s__contains": value
            for key, value in request.data['filters']
        }

        print(filters)

        query = query.filter(**filters)
        # query = query.filter(lookup=value)
        #     if filter == 'id':
        #         query = query.filter(
        #             id__contains=request.data['filters']['id'])
        #         continue
        #     if filter == 'transactionDate':
        #         query = query.filter(
        #             transactionDate__contains=request.data['filters']['transactionDate'])
        #         continue
        #     if filter == 'transactionAmount':
        #         query = query.filter(
        #             transactionAmount__contains=request.data['filters']['transactionAmount'])
        #         continue
        #     if filter == 'category_name':
        #         query = query.filter(
        #             category_id=request.data['filters']['category_name'])
        #         continue
        #     if filter == 'payment_method':
        #         query = query.filter(
        #             payment_id=request.data['filters']['payment_method'])
        #         continue
        #     if filter == 'accounting_type':
        #         query = query.filter(
        #             accounting_id=request.data['filters']['accounting_type'])
        #         continue

        # if filter == 'id':
        #     query = query.order_by(
        #         id__contains=request.data['filters']['id'])
        # elif filter == 'transactionDate':
        #     query = query.filter(
        #         transactionDate__contains=request.data['filters']['transactionDate'])
        # elif filter == 'transactionAmount':
        #     query = query.filter(
        #         transactionAmount__contains=request.data['filters']['transactionAmount'])
        # elif filter == 'category_name':
        #     query = query.filter(
        #         category_id=request.data['filters']['category_name'])
        # elif filter == 'payment_method':
        #     query = query.filter(
        #         payment_id=request.data['filters']['payment_method'])
        # else:
        #     query = query.filter(
        #         accounting_id=request.data['filters']['accounting_type'])

        # if request.data['sortOrder'] == 'desc':
        #     order = '-' + self.normalize(request.data['sortField'])
        # else:
        #     order = self.normalize(request.data['sortField'])

        # query = query.order_by(order)

        objectsList = serializers.TransactionSerializer(query, many=True).data
        data["transactions"] = objectsList or []

        return Response(data, status=status.HTTP_200_OK)
        return Response()
        # return Response(f"Fuck off!")
