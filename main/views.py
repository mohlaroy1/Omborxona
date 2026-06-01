from django.contrib import messages
from django.db.models import ExpressionWrapper, F, FloatField
from django.db.models import Q
from django.views import View
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from .models import *


class IndexView(RedirectView):
    url = 'sections'


class SectionsView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'sections.html')


class ProductsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            products = Product.objects.filter(
                branch=request.user.branch,
            ).annotate(
                total_price=ExpressionWrapper(
                    F('price') * F('amount'),
                    output_field=FloatField()
                )
            ).order_by('-total_price')

            query_search = request.GET.get('q')
            if query_search:
                products = products.filter(
                    Q(name__icontains=query_search) | Q(brand__icontains=query_search)
                )

            context = {
                'products': products,
                'query_search': query_search,
            }
            return render(request, 'products.html', context)
        return redirect('login')


    def post(self, request):
        if request.user.is_authenticated:
            Product.objects.create(
                name=request.POST.get('name'),
                brand=request.POST.get('brand'),
                price=request.POST.get('price'),
                amount=request.POST.get('amount'),
                unit=request.POST.get('unit'),
                branch = request.user.branch,
            )
            return self.get(request)
        return redirect('login')


class ProductUpdateView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk, branch=request.user.branch)

        context = {
            'product': product,
        }
        return render(request, 'product-update.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk, branch=request.user.branch)
        try:
            product.name = request.POST.get('name')
            product.brand = request.POST.get('brand')
            product.price = request.POST.get('price')
            product.amount = request.POST.get('amount')
            product.unit = request.POST.get('unit')
            product.branch = request.user.branch
            product.save()
            messages.success(request, 'Ma\'lumotlar muvaffaqiyatli saqlandi!')
        except Exception as e:
            messages.warning(request, f"Ma\'lumotlari yangilanmadi. Qayta urining! Error: {e}")
        return redirect('products')


class ProductDeleteConfirmView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk, branch=request.user.branch)
        context = {
            'product': product,
        }
        return render(request, 'product-delete.html', context)


class ProductDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk, branch=request.user.branch)
        product.delete()
        return redirect('products')


from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Client

class ClientsView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        clients = Client.objects.filter(branch=request.user.branch)
        return render(request, 'clients.html', {'clients': clients})

    def post(self, request):
        Client.objects.create(
            name=request.POST.get('client_name'),
            shop_name=request.POST.get('client_shop'),
            phone=request.POST.get('client_phone'),
            address=request.POST.get('client_address'),
            debt=request.POST.get('client_debt') or 0,
            branch=request.user.branch,

        )
        return redirect('clients')


class ClientUpdateView(LoginRequiredMixin, View):
    login_url = 'login'
    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk, branch=request.user.branch)
        client.name = request.POST.get('client_name')
        client.name = request.POST.get('client_name')
        client.shop_name = request.POST.get('client_shop')
        client.phone = request.POST.get('client_phone')
        client.address = request.POST.get('client_address')
        client.debt = request.POST.get('client_debt')

        client.save()
        return redirect('clients')


class ClientDeleteView(LoginRequiredMixin, View):
    login_url = 'login'
    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk, branch=request.user.branch)
        client.delete()
        return redirect('clients')

















