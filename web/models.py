from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class PurchaseCategory(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class IncomeCategory(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Purchase(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    value = models.FloatField(verbose_name="Значение")
    date = models.DateTimeField(verbose_name="Дата")
    is_planed = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(PurchaseCategory)


class Income(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    value = models.FloatField(verbose_name="Значение")
    date = models.DateTimeField(verbose_name="Дата")
    is_planed = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(IncomeCategory)
