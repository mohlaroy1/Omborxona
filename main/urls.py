from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sections/', SectionsView.as_view(), name='sections'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/confirm/', ProductDeleteConfirmView.as_view(), name='product-delete-confirm'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('clients/', ClientsView.as_view(), name='clients'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),

]