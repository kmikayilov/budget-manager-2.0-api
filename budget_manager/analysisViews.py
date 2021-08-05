from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Sum
import datetime

from . import models, serializers

# monthly analysis of expense and income (Victory chart)


class IncomeExpenseBarChart(APIView):
    def get(self, request):
        data = [
            {
                "seriesname": 'Income',
                "data": [],
            },
            {
                "seriesname": "Expense",
                "data": [],
            }
        ]

        year = datetime.datetime.today().year

        for i in range(1, 13):
            date = "{}-{}-".format(year,
                                   i) if i > 9 else "{}-0{}-".format(year, i)
            sumIncome = models.Transaction.objects.filter(Q(transactionDate__icontains=date) & Q(
                category__accounting=1)).aggregate(Sum('transactionAmount')).get('transactionAmount__sum') or 0
            sumExpense = models.Transaction.objects.filter(Q(transactionDate__icontains=date) & Q(
                category__accounting=2)).aggregate(Sum('transactionAmount')).get('transactionAmount__sum') or 0

            data[0]['data'].append(sumIncome)
            data[1]['data'].append({
                    "value":sumExpense
                }
            )


        return Response(data, status=status.HTTP_200_OK)


# all categories share in custom tooltip labels (pie chart, better animated)
# { labels: [], series: [] }

class CategoriesDonutChart(APIView):
    def get(self, request):
        queryset = models.Category.objects.all()
        data = []

        for category in queryset:
            sumAmount = models.Transaction.objects.filter(category=category.id).aggregate(
                Sum("transactionAmount")).get("transactionAmount__sum") or 0


            data.append({
                "id": category.category,
                "label": category.category,
                "value": sumAmount,
                # "valuePosition": "inside"
            })
        return Response(data, status=status.HTTP_200_OK)

# voronoi tooltip competing income and expense through time ( x = time, y = cost)

#
