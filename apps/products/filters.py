import django_filters
from apps.products.models import Product


class ProductFilter(django_filters.FilterSet):

    # category: filter by exact category ID
    # search: handled separately by DRF SearchFilter in the view

    # filter max and min by customer buget range
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # hide sold out products
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    # filter my name with iexact search
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    
    class Meta:
        model = Product
        fields = ('price_min', 'price_max', 'in_stock', 'category')

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_quantity__gt=0)
        return queryset.filter(stock_quantity=0)