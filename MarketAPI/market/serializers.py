from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import ProductCategory, Product


class ProductCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'parent']


class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    # cash = {}
    # parents = SerializerMethodField()
    #
    # def get_parents(self, instance):
    #     parents = []
    #     while instance.parent_id:
    #         if instance.parent_id in self.cash:
    #             parents.append((self.cash[instance.parent_id].id, self.cash[instance.parent_id].name))
    #             instance = self.cash[instance.parent_id]
    #         else:
    #             instance = instance.parent
    #             self.cash[instance.id] = instance
    #             parents.append((self.cash[instance.id].id, self.cash[instance.id].name))
    #     return parents

    # def to_representation(self, instance):
    #     represent = super().to_representation(instance)
    #     represent.pop('parent')
    #     return represent

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'parent']
        depth = 5


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
