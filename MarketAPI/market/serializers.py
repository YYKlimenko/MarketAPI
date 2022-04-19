from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import ProductCategory, Product, Order


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = SerializerMethodField()

    def get_category(self, obj):
        if self.context.get('category'):
            return self.context['category']
        else:
            return obj.category_id

    class Meta:
        model = Product
        fields = '__all__'
