from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import ProductCategory, Product, Order, OrderStatus


class ProductCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'parent']


class ProductCategoryDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        if instance.parent_id:
            represent['parent'] = self.__class__(instance.parent).data
        return represent

    class Meta (ProductCategoryListSerializer.Meta):
        pass


class ProductListSerializer(serializers.ModelSerializer):
    category = SerializerMethodField()

    def get_category(self, obj):
        if self.context.get('category'):
            return self.context['category']
        else:
            return obj.category_id

    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        values['category_id'] = self.context.get('category')
        return values

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['category'] = ProductCategoryDetailSerializer(instance.category).data
        return represent

    class Meta(ProductListSerializer.Meta):
        pass


class OrderStatusSerializer(serializers.ModelSerializer):
    order = SerializerMethodField()

    def get_order(self, obj):
        if self.context.get('order'):
            return self.context['order']
        else:
            return obj.order_id

    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        values['order_id'] = self.context.get('order')
        return values

    class Meta:
        model = OrderStatus
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['status'] = OrderStatusSerializer(instance.statuses.latest('date')).data
        represent['status'].pop('order')
        return represent

    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['products'] = ProductListSerializer(instance.products, many=True).data
        represent['statuses'] = OrderStatusSerializer(instance.statuses, many=True).data
        return represent

    class Meta:
        model = Order
        fields = ('id', 'user', 'products', 'statuses')
