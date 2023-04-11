from django.db import models
from django.contrib.auth.models import AbstractUser


class UserCustom(AbstractUser):
    username = models.CharField(max_length=50)
    fio = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fio']


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()


class Cart(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)


class Order(models.Model):
    products = models.ManyToManyField(Product)
    order_price = models.IntegerField()
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
