"""MarketAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from market.views import ProductCategoryListView, ProductCategoryDetailView, ProductListView, ProductDetailView, \
    OrderListView, OrderDetailView, OrderStatusListView, ProductImageListView, ProductImageDetailView
from MarketAPI.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from rest_framework import urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from market.yasg import urlpatterns as doc_urls


urlpatterns = [
    # Маршруты администрирования
    path('admin/', admin.site.urls),

    # Маршруты Категорий продуктов
    path('api/v1/categories/',
         ProductCategoryListView.as_view(),
         name='categories'),
    path('api/v1/categories/<int:category_pk>/',
         ProductCategoryDetailView.as_view(),
         name='category'),

    # Маршруты продуктов
    path('api/v1/categories/<int:category_pk>/products/',
         ProductListView.as_view(),
         name='products'),
    path('api/v1/categories/<int:category_pk>/products/<int:product_pk>/',
         ProductDetailView.as_view(),
         name='product'),
    path('api/v1/categories/<int:category_pk>/products/<int:product_pk>/images/',
         ProductImageListView.as_view()),
    path('api/v1/categories/<int:category_pk>/products/<int:product_pk>/images/<int:image_pk>/',
         ProductImageDetailView.as_view()),


    # Маршруты заказов
    path('api/v1/orders/',
         OrderListView.as_view(),
         name='orders'),
    path('api/v1/orders/<int:order_pk>/',
         OrderDetailView.as_view(),
         name='order'),
    path('api/v1/orders/<int:order_pk>/statuses/',
         OrderStatusListView.as_view(),
         name='statuses'),

    # Маршруты авторизации
    path('api/v1/auth/', include(urls)),
    path('api/v1/token/',
         TokenObtainPairView.as_view(),
         name='token'),
    path('api/v1/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/v1/token/verify/',
         TokenVerifyView.as_view(),
         name='token_verify'),
]

urlpatterns += doc_urls

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
