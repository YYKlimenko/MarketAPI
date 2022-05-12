from django.contrib.auth.models import User
from django.db import models


class ProductCategory(models.Model):
    name = models.CharField('Наименование', max_length=64)
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               verbose_name='Родительская категория',
                               related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'


class Product(models.Model):
    name = models.CharField('Наименование', max_length=64)
    category = models.ForeignKey(ProductCategory,
                                 default=1,
                                 on_delete=models.SET_DEFAULT,
                                 verbose_name='Категория',
                                 related_name='products',
                                 )
    description = models.TextField('Описание', max_length=1028)
    price = models.DecimalField('Стоимость', max_digits=9, decimal_places=3)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='Заказы')
    product = models.ManyToManyField(Product,
                                     verbose_name='Товар',
                                     related_name='products')
    date_create = models.DateTimeField('Время оформления', auto_created=True)
    date_delivery = models.DateField('Дата доставки')
    data_received = models.DateTimeField('Время получения')

    def __str__(self):
        return f'{self.user}: {[self.product]}: {self.date_create}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
