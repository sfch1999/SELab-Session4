from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=128)
    authors = models.CharField(max_length=128)
    category=models.CharField(max_length=128)
