from rest_framework import generics, status
from django.contrib.auth.models import User
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from knox.models import AuthToken
from django.contrib.auth import (
    authenticate, get_user_model, login as auth_login, logout as auth_logout
)
from django.db.models import Q, Sum
import datetime

from . import models, serializers

# monthly analysis of expense and income (Victory chart)


class IncomeExpenseBarChart(APIView):
    def get(self, request):
        data = [
            {
                "name": 'Income',
                "data": [],
            },
            {
                "name": "Expense",
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
            data[1]['data'].append(sumExpense)

        return Response(data, status=status.HTTP_200_OK)


# all categories share in custom tooltip labels (pie chart, better animated)
# { labels: [], series: [] }

class CategoriesDonutChart(APIView):
    def get(self, request):
        queryset = models.Category.objects.all()
        data = {
            "labels": [],
            "series": []
        }

        for category in queryset:
            sumAmount = models.Transaction.objects.filter(category=category.id).aggregate(
                Sum("transactionAmount")).get("transactionAmount__sum") or 0

            data['series'].append(sumAmount)
            data['labels'].append(category.category)
        return Response(data, status=status.HTTP_200_OK)

# voronoi tooltip competing income and expense through time ( x = time, y = cost)

#
