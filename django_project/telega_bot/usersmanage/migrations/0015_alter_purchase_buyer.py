# Generated by Django 3.2.3 on 2021-06-19 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0014_auto_20210619_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='buyer',
            field=models.ForeignKey(on_delete=models.SET(1), to='usersmanage.user', verbose_name='Покупатель'),
        ),
    ]
