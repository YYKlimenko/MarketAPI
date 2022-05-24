from collections import OrderedDict

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from market.models import ProductCategory, Product, Order
from market.serializers import ProductCategoryListSerializer, ProductCategoryDetailSerializer, ProductListSerializer, \
    ProductDetailSerializer, OrderListSerializer, OrderDetailSerializer


class ProductAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='admin', email='admin@admin.ru', password='admin')
        cls.category_1 = ProductCategory.objects.create(name='Техника')
        cls.category_2 = ProductCategory.objects.create(name='Телевизоры', parent_id=1)
        cls.product_1 = Product.objects.create(
            name='Xiaomi P1',
            category_id=2,
            description='Топ за свои деньги',
            price='22200.22'
        )
        cls.product_2 = Product.objects.create(
            name='Xiaomi P2',
            category_id=1,
            description='Топ за свои деньги',
            price='22200.22'
        )
        cls.order_1 = Order.objects.create(user=cls.user)
        cls.order_1.products.set([cls.product_1])

    def test_category_list_serializer(self):
        self.assertEqual(
            ProductCategoryListSerializer([self.category_1, self.category_2], many=True).data,
            [OrderedDict([('id', 1), ('name', 'Техника'), ('parent', None)]),
             OrderedDict([('id', 2), ('name', 'Телевизоры'), ('parent', 1)])]
        )

    def test_category_detail_serializer(self):
        self.assertEqual(
            ProductCategoryDetailSerializer(self.category_1).data,
            {'id': 1, 'name': 'Техника', 'parent': None}
        )

    def test_product_list_serializer(self):
        self.assertEqual(
            ProductListSerializer([self.product_1, self.product_2], many=True).data,
            [OrderedDict([('id', 1), ('name', 'Xiaomi P1'), ('description', 'Топ за свои деньги'),
                          ('price', '22200.220'), ('images', []), ('category', 2)]),
             OrderedDict([('id', 2), ('name', 'Xiaomi P2'), ('description', 'Топ за свои деньги'),
                          ('price', '22200.220'), ('images', []), ('category', 1)])]
        )

    def test_product_detail_serializer(self):
        self.assertEqual(
            ProductDetailSerializer(self.product_1).data,
            {'id': 1,
             'name': 'Xiaomi P1',
             'category': {'id': 2, 'name': 'Телевизоры', 'parent': {'id': 1, 'name': 'Техника', 'parent': None}},
             'description': 'Топ за свои деньги',
             'price': '22200.220',
             'images': []}
        )

    def test_order_list_serializer(self):
        order = OrderListSerializer([self.order_1], many=True).data
        order[0]['status'].pop('date'),
        self.assertEqual(
            order,
            [OrderedDict([('id', 1), ('user', 1), ('products', [1]),
                          ('status', {'id': 1, 'title': 'crt'})])]
        )

    def test_order_detail_serializer(self):
        order = OrderDetailSerializer(self.order_1).data
        order.pop('statuses')
        self.assertEqual(
            order,
            {'id': 1, 'user': 1, 'products':
                [OrderedDict(
                    [
                        ('id', 1),
                        ('name', 'Xiaomi P1'),
                        ('description', 'Топ за свои деньги'),
                        ('price', '22200.220'),
                        ('images', []),
                        ('category', 2)
                    ]
                )]
             }
        )

