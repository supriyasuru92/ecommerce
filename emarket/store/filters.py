from .models import Order
from django_filters import rest_framework as filters
import django_filters

class OrderFilter(django_filters.FilterSet):
    customer = filters.CharFilter(method="filter_customer")
    products = django_filters.CharFilter(
        field_name='order_item__product__name',
        method='filter_products',
        label='Products',
    )

    class Meta:
        model = Order
        fields = ("customer",)

    def filter_customer(self, queryset, name, value):
        return queryset.filter(customer__name__iexact=value)
    
    def filter_products(self, queryset, name, value):
        # Split the product names from the provided value
        product_names = [product.strip() for product in value.split(',') if product.strip()]

        # Filter orders based on the products
        queryset = queryset.filter(order_item__product__name__in=product_names).distinct()

        return queryset