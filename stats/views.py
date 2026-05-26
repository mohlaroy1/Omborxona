from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .models import *


class SalesView(View):
    def get(self, request):
        sales = Sale.objects.all()
        products = Product.objects.all()
        clients = Client.objects.all()
        context={
            'sales':sales,
            'products':products,
            'clients':clients
        }
        return render(request, 'sales.html', context)


    def post(self, request):
        product = get_object_or_404(Product, id=request.POST['product_id'])
        client = get_object_or_404(Client, id=request.POST['client_id'])


        Sale.objects.create(
            product=product,
            client=client,
            amount=request.POST['amount'],
            total_price=request.POST['total_price'],
            paid_price=request.POST['paid_price'],
            debt_price=request.POST['debt_price'],
            created_at=request.POST['created_at'],
        )

        return self.get(request)




