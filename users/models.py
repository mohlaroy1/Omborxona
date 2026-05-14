from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    branch = models.ForeignKey('main.Branch', on_delete=models.SET_NULL, null=True,blank=True)

