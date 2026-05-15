from django.core.validators import MinValueValidator
from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address=models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50,blank=True, null=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    amount = models.FloatField(validators=[MinValueValidator(0)],default=0)
    unit = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=100)
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    debt = models.FloatField(validators=[MinValueValidator(0)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name









