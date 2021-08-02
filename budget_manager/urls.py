from django.urls import path

from . import transactionViews, listsViews

urlpatterns = [
   
    #listsAPI
    path('transactions', listsViews.transactionsView.as_view(), name="transactions-list"),
    path('accountings', listsViews.accountingsView.as_view(), name="accoutings-list"),
    path('categories', listsViews.categoriesView.as_view(), name="categories-list"),
    path('payments', listsViews.paymentsView.as_view(), name="payments-list"),

    # transactionAPI
    
    # transaction/post
    path('transaction/create', transactionViews.createTransactionView.as_view(), name="transaction-create" ), 
    # transaction/fetch
    # transaction/put
    # transaction/delete
    path('transaction/<transaction_id>', transactionViews.TransactionView.as_view(), name="transaction_detail"),

    # transaction/filter


    # authAPI

    # auth/register
    
    # auth/login
    
    # auth/auth
]
