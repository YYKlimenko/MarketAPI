# Generated by Django 4.0.3 on 2022-05-14 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='products',
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_created=True, verbose_name='Время назначения статуса')),
                ('title', models.CharField(choices=[('crt', 'Создано'), ('snt', 'Отправлено'), ('dlv', 'Доставлено'), ('rcv', 'Получено'), ('cnl', 'Отменено')], max_length=3, verbose_name='Наименование статуса')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='market.order', verbose_name='Статус заказа')),
            ],
        ),
    ]
