from rest_framework import serializers
from .models import *
from django.utils import timezone



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "contact_number",
            "email",
        ]
        read_only_fields = ['id']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically remove 'email' from fields for PUT requests
        if self.context and self.context['request'].method == 'PUT':
            self.fields.pop('email', None)
    # email = serializers.EmailField(required=False)
    def validate_name(self, name):
        if Customer.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError("Customer name must be unique.")
        return name
    
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "weight",
        ]
        read_only_fields = ['id']

    def validate_name(self, name):
        if Product.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError("Product name must be unique.")
        return name
    
    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be a positive decimal.")
        if value > 25:
            raise serializers.ValidationError("Weight cannot be more than 25 kg.")
        return value
    
class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


        
class OrdersSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer', 'order_date', 'address', 'order_item']
        read_only_fields = ['id', 'order_number']

    def validate_order_item(self, order_items_data):
        cumulative_weight = 0
        for order_item_data in order_items_data:
            product = order_item_data['product']
            quantity = order_item_data['quantity']
            cumulative_weight += product.weight * quantity
        if cumulative_weight > 150:
            raise serializers.ValidationError("Order cumulative weight must be under 150kg.")

        return order_items_data
    
    def validate_order_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_item')

        order = Order.objects.create(**validated_data)

        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order,**order_item_data)

        return order