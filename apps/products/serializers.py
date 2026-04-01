from rest_framework import serializers
from apps.products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.serializerMethodField(Category)
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent_category', 'subcategories', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_subcategories(self, obj):
        # return list of subcategory names
        return [sub.name for sub in obj.subcategories.all()]
    
    def __str__(self):
        return self.category_name