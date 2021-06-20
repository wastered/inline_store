from django.contrib import admin

from .models import User, Shop, Referral, Purchase, Code


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'name', 'username', "point", "created_at")


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "quantity", "price")


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("id", "referrer_name", "referrer_id")


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ["invitation_code"]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "item_id", "quantity", "amount", "shipping_address", "phone_number",
                    "created_at", "successful")
