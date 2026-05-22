from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sections/', SectionsView.as_view(), name='sections'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('clients/', ClientsView.as_view(), name='clients'),

]