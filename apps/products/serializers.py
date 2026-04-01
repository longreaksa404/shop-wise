from rest_framework import serializers
from apps.products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    parent_category_name = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent_category', 'parent_category_name', 'subcategories', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_parent_category_name(self, obj):
        if obj.parent_category:
            return obj.parent_category.name
        return None

    def get_subcategories(self, obj):
        # return list of subcategory names
        return [sub.name for sub in obj.subcategories.all()]