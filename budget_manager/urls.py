from django.urls import path

from . import transactionViews, listsViews, authViews, analysisViews

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    # listsAPI
    path('transactions', listsViews.transactionsView.as_view(),
         name="transactions-list"),
    path('accountings', listsViews.accountingsView.as_view(), name="accoutings-list"),
    path('categories', listsViews.categoriesView.as_view(), name="categories-list"),
    path('payments', listsViews.paymentsView.as_view(), name="payments-list"),

    # transactionAPIru

    # transaction/post
    path('transaction/create', transactionViews.createTransactionView.as_view(),
         name="transaction-create"),

    # transaction/filter
    path('transaction/filter', transactionViews.FilterTransactions.as_view(),
         name="transactions_filter"),

    # transaction/fetch
    # transaction/put
    # transaction/delete
    path('transaction/<transaction_id>',
         transactionViews.TransactionView.as_view(), name="transaction_detail"),



     # authAPI

     # auth/register
    path('auth/register', authViews.RegisterView.as_view(), name="register-user"),
     
     # auth/login
    path('auth/login', authViews.LoginView.as_view(), name="login-user"),

     # auth/auth
    path('auth/user', authViews.UserView.as_view(), name="auth-user"),

     # analysis

     # donut chart categories
    path('analysis/categories-donut-chart', analysisViews.CategoriesDonutChart.as_view(), name="categories-donut-chart"),
     
     # income expense bar chart
    path('analysis/income-expense-bar-chart', analysisViews.IncomeExpenseBarChart.as_view(), name="income-expense-bar-chart"),
     
    path('analysis/total-net-bar-chart', analysisViews.TotalNetBarChart.as_view(), name="total-net-bar-chart"),

]
