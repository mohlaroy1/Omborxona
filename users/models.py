from django.db import models
from django.contrib.auth.models import AbstractUser

from main.models import Branch

class User(AbstractUser):
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)



