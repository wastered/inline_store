# Generated by Django 3.2.3 on 2021-06-19 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0016_alter_purchase_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usersmanage.user', verbose_name='Покупатель'),
        ),
    ]
