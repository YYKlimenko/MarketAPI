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
        ordering = ('id',)


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
        ordering = ('id',)


class ProductImage(models.Model):
    name = models.CharField('Название', max_length=20)
    image = models.ImageField('Изображение товара', upload_to='images/%Y/%m/%d/')
    product = models.ForeignKey(Product,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE,
                                verbose_name='Товар',
                                related_name='images')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображение товара'


class OrderStatus(models.Model):
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              verbose_name='Заказ',
                              related_name='statuses')
    title = models.CharField('Наименование статуса',
                             max_length=3,
                             choices=[
                                 ('crt', 'Создано'),
                                 ('snt', 'Отправлено'),
                                 ('dlv', 'Доставлено'),
                                 ('rcv', 'Получено'),
                                 ('cnl', 'Отменено')
                             ])
    date = models.DateTimeField('Время назначения статуса', auto_now_add=True)

    def __str__(self):
        return f'{self.title}: {self.date}'

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        unique_together = ('order', 'title')


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='orders')
    products = models.ManyToManyField(Product,
                                      verbose_name='Товар',
                                      related_name='orders')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Order, self).save()
        OrderStatus.objects.create(order_id=self.id, title='crt')

    def __str__(self):
        return f'{self.id} - {self.user}: {[self.products]}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



