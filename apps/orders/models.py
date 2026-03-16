import uuid

from django.conf import settings
from django.db import models

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cart_items', on_delete=models.CASCADE, limit_choices_to={'role': 'buyer'})
    product = models. ForeignKey('products.Product', related_name='cart_items', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'
        ordering = ('-created_at',)
        unique_together = (('buyer', 'product'),) # prevent duplicate cart

    def __str__(self):
        return f"{self.buyer.username} -> {self.product or 'deleted'} x(${self.quantity})"

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
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.buyer.username}  ${self.total_amount} | (${self.status})"

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', related_name='items', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.product or 'deleted'} -> {self.price} x(${self.quantity})"

    @property
    def subtotal(self):
        return self.price * self.quantity