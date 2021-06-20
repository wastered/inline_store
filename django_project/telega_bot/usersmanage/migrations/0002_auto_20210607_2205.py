# Generated by Django 3.2.3 on 2021-06-07 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('channel_id', models.BigIntegerField(null=True, unique=True, verbose_name='Канал')),
            ],
            options={
                'verbose_name': 'Канал',
                'verbose_name_plural': 'Каналы',
            },
        ),
        migrations.RenameField(
            model_name='user',
            old_name='scores',
            new_name='point',
        ),
        migrations.RemoveField(
            model_name='referral',
            name='channel',
        ),
    ]