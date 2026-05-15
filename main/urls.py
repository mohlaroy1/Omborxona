from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sections/', SectionsView.as_view(), name='sections'),
    path('products/', ProductsView.as_view(), name='products'),

]