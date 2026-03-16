from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'created_at')
    list_filter = ('parent_category',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'category', 'seller', 'is_in_stock', 'created_at')
    list_filter = ('category', 'seller')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('name', 'description', 'image')}),
        ('Pricing & Stock', {'fields': ('price', 'stock_quantity')}),
        ('Relations', {'fields': ('category', 'seller')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )