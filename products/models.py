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
        return self.name


class Order(models.Model):
    ...


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # quantity = models.
