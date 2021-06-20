from django.db import IntegrityError
from django.db.models import F, Q

from django_project.telega_bot.usersmanage.models import User, Shop, Code, Referral, Purchase, StorageItem

from asgiref.sync import sync_to_async


@sync_to_async
def select_points(user_id: int):
    user = User.objects.filter(user_id=user_id).first()
    return user.point


@sync_to_async
def update_point(user_id):
    user = User.objects.filter(user_id=user_id).first()
    return User.objects.filter(id=user.id).update(point=F("point") + 10)


@sync_to_async
def payment_point(user_id, amount):
    user = User.objects.filter(user_id=user_id).first()
    return User.objects.filter(id=user.id).update(point=amount)


@sync_to_async
def update_quantity(item_id: int, quantity):
    item = Shop.objects.filter(id=item_id).first()
    return Shop.objects.filter(id=item.id).update(quantity=F("quantity") - quantity)


@sync_to_async
def select_user(user_id: int):
    return User.objects.filter(user_id=user_id).first()


@sync_to_async
def add_user(user_id, full_name, username):
    try:
        return User(user_id=int(user_id), name=full_name, username=username, point=0).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def add_referrer(referrer_id, user_id):
    user = User.objects.filter(user_id=user_id).first()
    referrer_name = User.objects.filter(user_id=referrer_id).first()
    obj = User.objects.get(id=user.id)

    return Referral(
        id=obj,
        referral_name=user.name,
        referrer_id=int(referrer_id),
        referrer_name=referrer_name.name).save(force_insert=True)


@sync_to_async
def get_all_items():
    return Shop.objects.order_by('name')


@sync_to_async
def get_item(text):
    return Shop.objects.filter(Q(name__icontains=text) | Q(description__icontains=text))


@sync_to_async
def get_item_id(item_id):
    item = Shop.objects.filter(id=item_id).first()
    return item


@sync_to_async
def get_code(text):
    code = Code.objects.filter(invitation_code=text).first()
    return code


@sync_to_async
def update_purchase(buyer, item_id, amount, quantity, shipping_address, phone_number, successful):
    user = User.objects.filter(user_id=buyer).first()
    obj_user = User.objects.get(id=user.id)
    obj_item = Shop.objects.get(id=item_id)

    return Purchase(
        buyer=obj_user,
        item_id=obj_item,
        amount=amount,
        quantity=quantity,
        shipping_address=shipping_address,
        phone_number=phone_number,
        successful=successful).save(force_insert=True)


@sync_to_async
def storage_item(user_id, item):
    try:
        return StorageItem(user_id=user_id, item=item).save()
    except IntegrityError:
        return StorageItem.objects.filter(user_id=user_id).update(item=item)


@sync_to_async
def get_storage_item(user_id):
    obj = StorageItem.objects.filter(user_id=user_id).first()
    return obj.item


@sync_to_async
def delete_storage_item(user_id):
    obj = StorageItem.objects.filter(user_id=user_id).delete()
    return obj
