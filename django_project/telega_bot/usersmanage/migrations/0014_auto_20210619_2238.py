# Generated by Django 3.2.3 on 2021-06-19 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0013_alter_storageitem_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='buyer',
            field=models.ForeignKey(on_delete=models.SET('deleted'), to='usersmanage.user', verbose_name='Покупатель'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=models.TextField(blank=True, max_length=3000, verbose_name='Описание'),
        ),
    ]
