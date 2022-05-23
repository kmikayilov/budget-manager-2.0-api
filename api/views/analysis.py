from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Sum
import datetime
from .. import models, serializers

# monthly analysis of total net / income / expense (Victory chart)
class TotalNetBarChart(APIView):
    def get(self, request):
        data = []

        year = datetime.datetime.today().year

        for i in range(1, 13):
            date = "{}-{}-".format(year, i) if i > 9 else "{}-0{}-".format(year, i)
            sumIncome = models.Transaction.objects.filter(Q(transactionDate__icontains=date) & Q(category__accounting=1)).aggregate(Sum('transactionAmount')).get('transactionAmount__sum') or 0
            sumExpense = models.Transaction.objects.filter(Q(transactionDate__icontains=date) & Q(category__accounting=2)).aggregate(Sum('transactionAmount')).get('transactionAmount__sum') or 0

            data.append({
                    "name": datetime.datetime.strptime(str(i), "%m").strftime("%b"),
                    "Net income": sumIncome,
                    "Net expense": sumExpense, 
                    "Net cash flow": sumIncome - sumExpense,
                }
            )

        return Response(data, status=status.HTTP_200_OK)

# the amount of money spend or acquired for each category
class CategoriesDonutChart(APIView):
    def get(self, request):
        queryset = models.Category.objects.all()
        data = []

        for category in queryset:
            sumAmount = models.Transaction.objects.filter(category=category.id).aggregate(Sum("transactionAmount")).get("transactionAmount__sum") or 0

            if sumAmount  != 0:
                data.append({
                    "name": category.category,
                    "value": sumAmount,
                })
        return Response(data, status=status.HTTP_200_OK)

