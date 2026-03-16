from django.contrib import admin
from apps.orders.models import Order, CartItem, OrderItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'quantity', 'created_at')
    search_fields = ('buyer__username',)
    list_filter = ('created_at',)

