from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from market.models import ProductCategory, Product, Order, OrderStatus
from market.serializers import (
    ProductCategoryListSerializer,
    ProductCategoryDetailSerializer, ProductListSerializer,
    ProductDetailSerializer, OrderListSerializer,
    OrderDetailSerializer, OrderStatusListSerializer
)


class ProductAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='admin',
                                                 email='admin@admin.ru',
                                                 password='admin')
        cls.category_1 = ProductCategory.objects.create(name='Техника')
        cls.category_2 = ProductCategory.objects.create(name='Телевизоры',
                                                        parent_id=1)
        cls.product_1 = Product.objects.create(
            name='Xiaomi P1',
            category_id=2,
            description='Топ за свои деньги',
            price='22200.22'
        )
        cls.order_1 = Order.objects.create(user=cls.user)
        cls.order_1.products.set((cls.product_1,))

    """Блок тестирования Категорий продуктов"""

    def test_category_get_list(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(
            ProductCategoryListSerializer([self.category_1, self.category_2],
                                          many=True).data,
            response.data
        )
        self.assertEqual(response.status_code, 200)

    def test_category_post(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(reverse('categories'), data={'name': 'смартфоны',
                                                      'parent': 2})
        category_3 = ProductCategory.objects.get(pk=3)
        self.assertEqual(
            (category_3.name, category_3.parent_id),
            ('смартфоны', 2)
        )

    def test_category_get_detail(self):
        response = self.client.get(reverse('category',
                                           kwargs={'category_pk': 2}))
        self.assertEqual(
            ProductCategoryDetailSerializer(self.category_2).data,
            response.data
        )
        self.assertEqual(response.status_code, 200)

    """Блок тестирования Продуктов"""

    def test_product_get_list(self):
        response = self.client.get(reverse('products',
                                           kwargs={'category_pk': 2}))
        queryset = Product.objects.filter(category=2)
        self.assertEqual(
            ProductListSerializer(queryset, many=True).data,
            response.data
        )
        self.assertEqual(response.status_code, 200)

    def test_product_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('products', kwargs={'category_pk': 2}),
            data={'name': 'Samsung TV',
                  'category': 2,
                  'description': 'Норм',
                  'price': 12000.12}
        )
        product_2 = Product.objects.get(pk=2)
        self.assertEqual(
            (product_2.name, product_2.category_id, product_2.description),
            ('Samsung TV', 2, 'Норм')
        )
        self.assertEqual(response.status_code, 201)

    def test_product_get_detail(self):
        response = self.client.get(reverse('product',
                                           kwargs={'category_pk': 2,
                                                   'product_pk': 1}))
        instance = Product.objects.get(pk=1)
        self.assertEqual(
            ProductDetailSerializer(instance).data,
            response.data
        )
        self.assertEqual(response.status_code, 200)

    """Блок тестирования Заказов"""

    def test_order_get_list(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(
            OrderListSerializer([self.order_1], many=True).data,
            response.data
        )
        self.assertEqual(response.status_code, 200)

    def test_order_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('orders'),
            data={'user': 1,
                  'products': [1]}
        )
        instance = Order.objects.get(pk=2)
        self.assertEqual(
            instance.user_id,
            1
        )
        self.assertEqual(
            instance.products.all().first(),
            self.product_1
        )
        self.assertEqual(response.status_code, 201)
        self.assertQuerysetEqual(
            self.product_1.orders.all(),
            Order.objects.filter(products=1),
            ordered=False
        )

    def test_order_get_detail(self):
        response = self.client.get(reverse('order', kwargs={'order_pk': 1}))
        instance = Order.objects.get(pk=1)
        self.assertEqual(
            OrderDetailSerializer(instance).data,
            response.data
        )
        self.assertEqual(response.status_code, 200)

    def test_order_status_get_list(self):
        response = self.client.get(reverse('statuses', kwargs={'order_pk': 1}))
        self.assertEqual(
            OrderStatusListSerializer(OrderStatus.objects.filter(order_id=1),
                                      many=True).data,
            response.data
        )
        self.assertEqual(response.status_code, 200)

    def test_order_status_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('statuses', kwargs={'order_pk': 1}),
            data={'title': 'snt'}
        )
        self.assertEqual(
            OrderStatus.objects.get(pk=3).title,
            'snt'
        )
        self.assertEqual(
            OrderStatus.objects.get(pk=3).order,
            self.order_1
        )
        self.assertEqual(response.status_code, 201)
