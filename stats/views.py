from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Sum
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



class ImportProductsView(LoginRequiredMixin, View):
    def get(self, request):
        import_products = ImportProduct.objects.filter(branch=request.user.branch)
        products = Product.objects.filter(branch=request.user.branch)
        context = {
            'import_products':import_products,
            'products':products,
        }
        return render(request, 'import-products.html', context)

    def post(self, request):
        product = get_object_or_404(Product, id=request.POST['product_id'], branch=request.user.branch)
        i = ImportProduct.objects.create(
            product=product,
            buy_price=float(request.POST.get('buy_price')),
            sell_price=request.POST.get('sell_price') if request.POST.get('sell_price') else None,
            amount=request.POST.get('amount') if request.POST.get('amount') else None,
            total_price=float(request.POST.get('total_price')),
            description=request.POST.get('description'),
            branch=request.user.branch,
            user=request.user,
        )
        product.amount += i.amount
        if i.sell_price:
            product.price = i.sell_price
        product.save()

        if not i.total_price:
            i.total_price = i.buy_price * i.amount
            i.save()

        return redirect('import-products')


class DebtsView(View):
    template_name = 'debts.html'

    def get_queryset(self, request):
        qs = PayDebt.objects.select_related('client', 'user').filter(
            branch=request.user.branch
        )
        q = request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(client__name__icontains=q) |
                Q(description__icontains=q)
            )
        return qs

    def get(self, request):
        qs = self.get_queryset(request)
        context = {
            'debts':         qs,
            'clients':       Client.objects.filter(branch=request.user.branch),
            'total_amount':  qs.aggregate(s=Sum('amount'))['s'] or 0,
            'total_count':   qs.count(),
            'clients_count': qs.values('client').distinct().count(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')

        if action == 'add':
            client = get_object_or_404(Client, id=request.POST.get('client'), branch=request.user.branch)
            amount = float(request.POST.get('amount'))
            client.debt -= amount
            client.save()
            PayDebt.objects.create(
                client=client,
                amount=amount,
                description=request.POST.get('description', ''),
                branch=request.user.branch,
                user=request.user,
            )
            messages.success(request, "To'lov muvaffaqiyatli qo'shildi.")

        elif action == 'edit':
            debt = get_object_or_404(PayDebt, id=request.POST.get('debt_id'), branch=request.user.branch)
            client = debt.client
            new_amount = float(request.POST.get('amount', debt.amount))
            client.debt += debt.amount
            client.debt -= new_amount
            client.save()
            debt.client      = get_object_or_404(Client, id=request.POST.get('client'), branch=request.user.branch)
            debt.amount      = new_amount
            debt.description = request.POST.get('description', debt.description)
            debt.save()
            messages.success(request, "To'lov muvaffaqiyatli yangilandi.")

        elif action == 'delete':
            debt = get_object_or_404(PayDebt, id=request.POST.get('debt_id'), branch=request.user.branch)
            client = debt.client
            client.debt += debt.amount
            client.save()
            debt.delete()
            messages.success(request, "To'lov o'chirildi.")

        return redirect('debts')
