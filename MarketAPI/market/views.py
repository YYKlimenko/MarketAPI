from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import ProductCategory, Product
from .serializers import ProductCategorySerializer, ProductSerializer


class CommonDataSet:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductCategoryListView(CommonDataSet, ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    filter_fields = ['parent']
    search_fields = ['name', 'parent']
    ordering_fields = ['name', 'parent']

    def get_queryset(self):
        if self.kwargs.get('category_pk'):
            return ProductCategory.objects.filter(parent=self.kwargs['category_pk'])
        else:
            return ProductCategory.objects.all()


class ProductCategoryView(CommonDataSet, RetrieveUpdateDestroyAPIView):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    lookup_url_kwarg = 'category_pk'


class ProductListView(CommonDataSet, ListCreateAPIView):
    serializer_class = ProductSerializer
    filter_fields = ['category']
    search_fields = ['name', 'category__name', 'description']
    ordering_fields = ['name', 'category', 'price', 'description']

    def get_queryset(self):
        if self.kwargs.get('category_pk'):
            return Product.objects.filter(category=self.kwargs['category_pk'])
        else:
            return Product.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs.get('category_pk'):
            context['category'] = self.kwargs['category_pk']
        return context


class ProductView(CommonDataSet, RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_url_kwarg = 'product_pk'
