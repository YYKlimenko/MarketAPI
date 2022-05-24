from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import ProductCategory, Product, Order, OrderStatus, ProductImage


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


class ProductImageListSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        values['product_id'] = self.context.get('product')
        return values

    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductImageDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta(ProductImageListSerializer.Meta):
        pass


class ProductListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        if self.context.get('category'):
            represent['category'] = self.context['category']
        else:
            represent['category'] = instance.category_id
        return represent

    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        values['category_id'] = self.context.get('category')
        return values

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'images')


class ProductDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['category'] = ProductCategoryDetailSerializer(instance.category).data
        represent['images'] = ProductImageListSerializer(instance.images.all(), many=True).data
        return represent

    class Meta(ProductListSerializer.Meta):
        fields = ('id', 'name', 'category', 'description', 'price')


class OrderStatusListSerializer(serializers.ModelSerializer):
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
        represent['status'] = OrderStatusListSerializer(instance.statuses.latest('date')).data
        represent['status'].pop('order')
        return represent

    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['products'] = ProductListSerializer(instance.products, many=True).data
        represent['statuses'] = OrderStatusListSerializer(instance.statuses, many=True).data
        return represent

    class Meta:
        model = Order
        fields = ('id', 'user', 'products', 'statuses')
