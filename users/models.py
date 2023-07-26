from django.db import models
from django.contrib.auth.models import AbstractUser

from products.models import Product


class User(AbstractUser):
    pass


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist for {self.user.username}"
