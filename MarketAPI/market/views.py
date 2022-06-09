from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import ProductCategory, Product, Order, OrderStatus, ProductImage
from .serializers import ProductCategoryListSerializer, ProductCategoryDetailSerializer, ProductListSerializer, \
    ProductDetailSerializer, OrderListSerializer, OrderDetailSerializer, OrderStatusListSerializer, \
    ProductImageListSerializer, ProductImageDetailSerializer


class ProductCategoryListView(ListCreateAPIView):
    queryset = ProductCategory.objects.all().select_related('parent')
    serializer_class = ProductCategoryListSerializer
    filter_fields = ['parent']
    search_fields = ['name']
    ordering_fields = ['name', 'parent']


class ProductCategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all().select_related('parent')
    serializer_class = ProductCategoryDetailSerializer
    lookup_url_kwarg = 'category_pk'


class ProductListView(ListCreateAPIView):
    serializer_class = ProductListSerializer
    filter_fields = ['category']
    search_fields = ['name', 'category__name', 'description']
    ordering_fields = ['name', 'category', 'price', 'description']

    def get_queryset(self):
        return Product.objects.filter(
            category=self.kwargs['category_pk']).select_related('category').prefetch_related('images')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['category'] = self.kwargs['category_pk']
        return context


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    lookup_url_kwarg = 'product_pk'

    def get_queryset(self):
        if self.kwargs.get('category_pk'):
            return Product.objects.filter(
                category=self.kwargs['category_pk']).select_related('category').prefetch_related('images')
        else:
            return Product.objects.all()


class OrderListView(ListCreateAPIView):
    queryset = Order.objects.all().select_related('user').prefetch_related('products', 'statuses')
    serializer_class = OrderListSerializer


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().select_related('user').prefetch_related('products', 'statuses')
    serializer_class = OrderDetailSerializer
    lookup_url_kwarg = 'order_pk'


class OrderStatusListView(ListCreateAPIView):
    serializer_class = OrderStatusListSerializer

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


class ProductImageListView(ListCreateAPIView):
    serializer_class = ProductImageListSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product'] = self.kwargs.get('product_pk')
        return context


class ProductImageDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductImageDetailSerializer
    lookup_url_kwarg = 'image_pk'

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
