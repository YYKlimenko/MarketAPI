from django.contrib import admin
from .models import Product, ProductCategory, Order, OrderStatus, ProductImage

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(OrderStatus)
admin.site.register(ProductImage)
