from django.urls import path
from django.contrib import admin

from .views import *

urlpatterns = [
    path('sales/', SalesView.as_view(), name='sales'),
    path('import-products/', ImportProductsView.as_view(), name='import-products'),
    path('debts/', DebtsView.as_view(), name='debts'),
]