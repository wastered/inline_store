# Generated by Django 3.2.3 on 2021-06-20 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0019_auto_20210620_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Стоимость ₽'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена ₽'),
        ),
    ]
