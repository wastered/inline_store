# Generated by Django 3.2.3 on 2021-06-10 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0005_auto_20210609_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='quantity',
            field=models.IntegerField(default=5, verbose_name='Количество'),
            preserve_default=False,
        ),
    ]