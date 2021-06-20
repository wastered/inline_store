from django.contrib.auth import get_user_model
from django.db import models


class TimedBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimedBaseModel):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name='ID пользователя Телеграм')
    name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    username = models.CharField(max_length=100, verbose_name='Username Телеграм', null=True)
    point = models.DecimalField(verbose_name='Баллы', decimal_places=2, max_digits=8)

    def __str__(self):
        return f"№{self.id} {self.name}"


class Shop(TimedBaseModel):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = 'Товары'

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название Товара', max_length=50)
    photo = models.CharField(verbose_name='Фото file_id', max_length=200)
    price = models.DecimalField(verbose_name='Цена ₽', decimal_places=2, max_digits=8)
    quantity = models.IntegerField(verbose_name='Количество')
    description = models.TextField(verbose_name='Описание', max_length=3000, blank=True)

    def __str__(self):
        return f"{self.id} - {self.name} {self.quantity}"


class Referral(TimedBaseModel):
    class Meta:
        verbose_name = "Реферал"
        verbose_name_plural = 'Рефералы'

    id = models.ForeignKey(User, unique=True, primary_key=True, on_delete=models.CASCADE)
    referral_name = models.CharField(max_length=100, verbose_name='Пользователь')
    referrer_name = models.CharField(max_length=100, verbose_name='Привел пользователь', null=True)
    referrer_id = models.BigIntegerField()

    def __str__(self):
        return f"№{self.id} - от {self.referrer_name}"


class Code(TimedBaseModel):
    class Meta:
        verbose_name = "Код приглашения"
        verbose_name_plural = 'Приглашения'

    invitation_code = models.CharField(unique=True, verbose_name='Код приглашения', max_length=200, null=True)


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Purchase(TimedBaseModel):
    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.SET_NULL, null=True)
    item_id = models.ForeignKey(Shop, verbose_name='Идентификатор товара', on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name='Стоимость ₽', decimal_places=2, max_digits=8)
    quantity = models.IntegerField(verbose_name='Количество')
    purchase_time = models.DateTimeField(verbose_name='Время покупки', auto_now_add=True)
    shipping_address = models.CharField(verbose_name='Адрес доставки', max_length=200, null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=50, null=True)
    successful = models.BooleanField(verbose_name='Оплачено', default=False)

    def __str__(self):
        return f"{self.id} - {self.item_id} ({self.quantity} кол-во)"


class StorageItem(TimedBaseModel):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True)
    item = models.CharField(max_length=250)
