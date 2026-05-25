from django.urls import path
from django.contrib import admin

from .views import *

urlpatterns = [
    path('sales/', SalesView.as_view(), name='sales'),
]