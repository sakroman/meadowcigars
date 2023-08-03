from decimal import Decimal

from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return f"Image for {self.product.name}"


class Field(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    product = models.ManyToManyField(Product)
    value = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return f"{self.name} {self.value}"


class Order(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id}"

    def update_total_price(self):
        order_items = self.orderitem_set.all()
        total_price = sum(item.get_total_price() for item in order_items)
        self.total_price = Decimal(total_price)
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"OrderItem {self.id}"

    def get_total_price(self):
        return self.unit_price * self.quantity
