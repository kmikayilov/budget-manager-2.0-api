from drf_yasg.views import get_schema_view
from .views import base, analysis, user, transaction, payment, accounting, category
from rest_framework import permissions
from drf_yasg import openapi
from django.urls import path


schema_view = get_schema_view(
   openapi.Info(
      title="Swagger",
      default_version='v1',
   ),
   public=False,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   
   path('', base.index, name="dashboard"),
   path('accounts/login/', base.loginPanel, name="loginPanel"),
   path('accounts/logout/', base.logoutManager, name="logout"),
   path('reset_password/', base.change_password, name="change_password"),
   
   # Transaction APIs
   path('Transaction/list/', transaction.transaction_list, name="transaction-list"),
   path('Transaction/create/', transaction.transaction_post, name="transaction-create"),
   path('Transaction/<pk>/', transaction.transaction, name="transaction"),
   
   # Accounting APIs
   path('Accounting/list/', accounting.accounting_list, name="accounting-list"),
   path('Accounting/create/', accounting.accounting_post, name="accounting-create"),
   path('Accounting/<pk>/', accounting.accounting, name="accounting"),
   
   # Category APIs
   path('Category/list/', category.category_list, name="category-list"),
   path('Category/create/', category.category_post, name="category-create"),
   path('Category/<pk>/', category.category, name="category"),
   
   # Payment APIs
   path('Payment/list/', payment.payment_list, name="payment-list"),
   path('Payment/create/', payment.payment_post, name="payment-create"),
   path('Payment/<pk>/', payment.payment, name="payment"),
   
   # User APIs
   path('User/create/', user.user_post, name="user-create"),
   path('User/<pk>/', user.user, name="user"),

   # Analysis APIs
   path('Analysis/Transaction-Amount-Per-Category/', analysis.CategoriesDonutChart.as_view(), name="categories-donut-chart"),
   path('Analysis/Total-Income-Expense-Net-Cash-Flow/', analysis.TotalNetBarChart.as_view(), name="total-net-bar-chart"),

   # swagger
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
