from django.db.models import ExpressionWrapper, F, FloatField
from django.shortcuts import render
from django.views import View
from django.views.generic import RedirectView

from .models import *


class IndexView(RedirectView):
    url = 'sections'


class SectionsView(View):
    def get(self, request):
        return render(request, 'sections.html')


class ProductsView(View):
    def get(self, request):
        products = Product.objects.annotate(
            total_price=ExpressionWrapper(
                F('price') * F('amount'),
                output_field=FloatField()
            )
        ).order_by('-total_price')

        context = {
            'products': products,
        }
        return render(request, 'products.html', context)


    def post(self, request):
        Product.objects.create(
            name = request.POST.get('name'),
            brand = request.POST.get('brand'),
            price = request.POST.get('price'),
            amount = request.POST.get('amount'),
            unit = request.POST.get('unit'),
        )
        return self.get(request)