import uuid

from django.conf import settings
from django.db import models
from django.db.models import DecimalField

from apps.products.models import Product, Category

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cart_items', on_delete=models.CASCADE, limit_choices_to={'role': 'buyer'})
    product = models. ForeignKey(Product, related_name='cart_items', on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending',
        PAID = 'paid', 'Paid',
        SHIPPED = 'shipped', 'Shipped',
        DELIVERED = 'delivered', 'Delivered',
        CANCELED = 'canceled', 'Canceled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE, limit_choices_to={'role': 'buyer'})
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_amount = DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)