import uuid

from django.conf import settings
from django.db import models
from apps.products.models import Product, Category

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cart_items', on_delete=models.CASCADE, limit_choices_to={'role': 'buyer'})
    product = models. ForeignKey(Product, related_name='cart_items', on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)