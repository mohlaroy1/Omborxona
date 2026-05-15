from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

from main.models import Branch,Product,Client

User=get_user_model()

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    total_price = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    paid_price = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    debt_price = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product} -- {self.client}"


class ImportProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    buy_price = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    sell_price = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    total_price = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product.name} -- {self.amount} {self.product.unit}"

    def save(self, *args, **kwargs):
        if self.sell_price is not None:
            self.product.price = self.sell_price
            self.product.save()
        super().save(*args, **kwargs)


class PayDebt(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)


    def __str__(self):
        return f"{self.client.name} -- {self.amount}"