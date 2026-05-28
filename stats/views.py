from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views import View
from django.contrib import messages

from .models import *


class SalesView(View):
    def get(self, request):
        sales = Sale.objects.order_by('-id')

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
        amount = float(request.POST.get('amount'))

        if product.amount < amount:
            messages.error(request, 'Mahsulot yetarli emas!')
            return redirect('sales')

        debt_price = float(request.POST.get('debt_price')) if request.POST.get('debt_price') else None
        total_price = float(request.POST.get('total_price')) if request.POST.get('total_price') else None
        paid_price = float(request.POST.get('paid_price')) if request.POST.get('paid_price') else None

        if total_price is None:
            if paid_price and debt_price:
                total_price = debt_price + paid_price
            else:
                total_price = product.price * amount

        if not paid_price and debt_price:
            paid_price = total_price - debt_price
        elif paid_price and not debt_price:
            debt_price = total_price - paid_price
        else:
            paid_price = total_price
            debt_price = 0

        if total_price != paid_price + debt_price:
            messages.warning(request, "Noto'g'ri hisoblash! Iltimos qayta urining.")

        Sale.objects.create(
            product=product,
            client=client,
            amount=amount,
            debt_price=debt_price,
            total_price=total_price,
            paid_price=paid_price,
            created_at=request.POST.get('created_at'),
        )

        product.amount -= amount
        product.save()

        client.debt += debt_price
        client.save()

        return self.get(request)




