from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ProductCategory, Product, Order, OrderStatus, ProductImage
from .serializers import ProductCategoryListSerializer, ProductCategoryDetailSerializer, ProductListSerializer, \
    ProductDetailSerializer, OrderListSerializer, OrderDetailSerializer, OrderStatusSerializer, \
    ProductImageListSerializer, ProductImageDetailSerializer
from .permissions import IsAdminOrReadOnly


class CommonDataSet:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAdminOrReadOnly]


class ProductCategoryListView(CommonDataSet, ListCreateAPIView):
    queryset = ProductCategory.objects.all().select_related('parent')
    serializer_class = ProductCategoryListSerializer
    filter_fields = ['parent']
    search_fields = ['name', 'parent']
    ordering_fields = ['name', 'parent']


class ProductCategoryDetailView(CommonDataSet, RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all().select_related('parent')
    serializer_class = ProductCategoryDetailSerializer
    lookup_url_kwarg = 'category_pk'


class ProductListView(CommonDataSet, ListCreateAPIView):
    serializer_class = ProductListSerializer
    filter_fields = ['category']
    search_fields = ['name', 'category__name', 'description']
    ordering_fields = ['name', 'category', 'price', 'description']

    def get_queryset(self):
        if self.kwargs.get('category_pk'):
            return Product.objects.filter(
                category=self.kwargs['category_pk']).select_related('category').prefetch_related('images')
        else:
            return Product.objects.all().select_related('category').prefetch_related('images')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs.get('category_pk'):
            context['category'] = self.kwargs['category_pk']
        return context


class ProductDetailView(CommonDataSet, RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    lookup_url_kwarg = 'product_pk'

    def get_queryset(self):
        if self.kwargs.get('category_pk'):
            return Product.objects.filter(
                category=self.kwargs['category_pk']).select_related('category').prefetch_related('images')
        else:
            return Product.objects.all()


class OrderListView(CommonDataSet, ListCreateAPIView):
    queryset = Order.objects.all().select_related('user').prefetch_related('products', 'statuses')
    serializer_class = OrderListSerializer


class OrderDetailView(CommonDataSet, RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().select_related('user').prefetch_related('products', 'statuses')
    serializer_class = OrderDetailSerializer
    lookup_url_kwarg = 'order_pk'


class OrderStatusListView(CommonDataSet, ListCreateAPIView):
    serializer_class = OrderStatusSerializer

    def get_queryset(self):
        if self.kwargs.get('order_pk'):
            return OrderStatus.objects.filter(order=self.kwargs['order_pk'])
        else:
            return OrderStatus.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs.get('order_pk'):
            context['order'] = self.kwargs['order_pk']
        return context


class ProductImageListView(CommonDataSet, ListCreateAPIView):
    serializer_class = ProductImageListSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product'] = self.kwargs.get('product_pk')
        return context


class ProductImageDetailView(CommonDataSet, RetrieveUpdateDestroyAPIView):
    serializer_class = ProductImageDetailSerializer
    lookup_url_kwarg = 'image_pk'

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
