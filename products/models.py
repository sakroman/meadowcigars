from decimal import Decimal

from django.db import models
from django.db.models import Sum, F
from django.utils.text import slugify

from django.contrib.auth import get_user_model

# Ако наследиш този абстрактен модел вместо models.Model
# моделът, който дефинираш, ще има created_at, updated_at, etc...
#
# class MetadataBaseModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True, db_index=True)
#     created_by = models.ForeignKey(
#         User, editable=False, null=True, on_delete=models.SET_NULL,
#         related_name='created_%(class)s',
#     )
#     updated_by = models.ForeignKey(
#         User, editable=False, null=True, on_delete=models.SET_NULL,
#         related_name='updated_%(class)s'
#     )
#
#     class Meta:
#         abstract = True
#


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
    ORDER_STATUSES = (
        ('cart', 'Cart'),
        ('confirmed', 'Confirmed'),
    )

    user = models.ForeignKey('users.User',null=True, blank=True ,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUSES,
                              default='cart')

    def __str__(self):
        return f"Order {self.id}"

    def get_info(self):
        ...

    def get_total_price(self):
        return self.items.aggregate(
            total_value=Sum(F('product__price') * F('quantity'))
        )['total_value'] or 0

    def update_total_price(self):
        order_items = self.orderitem_set.all()
        total_price = sum(item.get_total_price() for item in order_items)
        self.total_price = Decimal(total_price)
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"OrderItem {self.id}"

    def get_total_price(self):
        return self.product.price * self.quantity


class ShippingInfo(models.Model):
    order = models.OneToOneField(Order, related_name='info', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255)
    suite_apartment = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=12)
    phone_number = models.CharField(max_length=30)

    def __str__(self):
        return f"ShippingInfo for Order {self.order.id}"
