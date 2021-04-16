import datetime

import django
from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    isAdmin = models.BooleanField(default=False)
    token=models.CharField(max_length=256, default="")
    token_exp_time = models.DateTimeField(default= django.utils.timezone.now)
