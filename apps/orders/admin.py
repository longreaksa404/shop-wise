from django.contrib import admin
from apps.orders.models import Order, CartItem, OrderItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'quantity', 'created_at')
    search_fields = ('buyer__username',)
    list_filter = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'status', 'total_amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('buyer__username',)
    readonly_fields = ('created_at', 'updated_at', 'status', 'total_amount')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal')
    search_fields = ('order__buyer__username',)
    readonly_fields = ('created_at', 'price')