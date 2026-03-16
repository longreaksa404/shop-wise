from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'created_at')
    list_filter = ('parent_category',)
    search_fields = ('name',)
    ordering = ('name',)