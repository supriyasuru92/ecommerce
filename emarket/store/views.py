from django.shortcuts import render
from .models import *
from rest_framework import filters, status, viewsets
from .serializers import *
from .filters import OrderFilter

class CustomersViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class OrdersViewSet(viewsets.ModelViewSet):
    serializer_class = OrdersSerializer
    queryset = Order.objects.all()
    filterset_class = OrderFilter
