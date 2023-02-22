from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug', 'title')

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ('id', 'title', 'price', 'featured', 'category', 'category_id')

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Cart
        fields = ('id', 'user', 'menuitem', 'menuitem_id','quantity', 'unit_price', 'price')

class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField(read_only=True)
    order_items_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items', 'order_items_id')
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        return OrderItemSerializer(order_items, many=True).data

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'menuitem', 'quantity', 'unit_price', 'price', 'menuitem_id')


class ManagerListSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id','username','email']