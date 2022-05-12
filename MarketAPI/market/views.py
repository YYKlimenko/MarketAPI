from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ProductCategory, Product
from .serializers import ProductCategoryListSerializer, ProductCategoryDetailSerializer, ProductSerializer
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


class ProductCategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all().select_related('parent')
    serializer_class = ProductCategoryDetailSerializer
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


class ProductView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_url_kwarg = 'product_pk'
