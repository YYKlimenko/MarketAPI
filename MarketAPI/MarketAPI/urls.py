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
from django.urls import path, include
from market.views import ProductCategoryListView, ProductCategoryDetailView, ProductListView, ProductView
from rest_framework import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/v1/categories/', ProductCategoryListView.as_view()),
    path('api/v1/categories/<int:category_pk>/', ProductCategoryDetailView.as_view()),
    path('api/v1/categories/<int:category_pk>/products/', ProductListView.as_view()),
    path('api/v1/categories/<int:category_pk>/products/<int:product_pk>/', ProductView.as_view()),
    path('api/v1/auth/', include(urls))
]
