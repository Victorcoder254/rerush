from django.contrib import admin
from .models import *


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "date_created")
    search_fields = ("title",)
    list_filter = ("date_created",)


admin.site.register(Advertisement, AdvertisementAdmin)


class Advertisement1Admin(admin.ModelAdmin):
    list_display = ("title", "date_created")
    search_fields = ("title",)
    list_filter = ("date_created",)


admin.site.register(Advertisement1, Advertisement1Admin)


class Advertisement2Admin(admin.ModelAdmin):
    list_display = ("title", "date_created")
    search_fields = ("title",)
    list_filter = ("date_created",)


admin.site.register(Advertisement2, Advertisement2Admin)


class Advertisement3Admin(admin.ModelAdmin):
    list_display = ("title", "date_created")
    search_fields = ("title",)
    list_filter = ("date_created",)


admin.site.register(Advertisement3, Advertisement3Admin)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "name", "email", "date_created")
    list_filter = ("product", "date_created")
    search_fields = ("product__name", "name", "email", "review")
    readonly_fields = ("date_created",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "seller_name", "created", "unique_id")
    list_filter = ("categories", "created")
    search_fields = ("name", "seller_name")
    readonly_fields = ("created",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "date_ordered", "complete", "status")
    list_filter = ("customer", "date_ordered", "complete")
    search_fields = ("customer__username", "transaction_id")
    readonly_fields = ("date_ordered",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "order", "quantity", "date_added")
    list_filter = ("product", "order", "date_added")
    search_fields = ("product__name",)
    readonly_fields = ("date_added",)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "order", "address", "city", "state", "date_added")
    list_filter = ("customer", "order", "date_added")
    search_fields = ("customer__username", "address", "city", "state")
    readonly_fields = ("date_added",)


@admin.register(OurSocials)
class OurSocialsAdmin(admin.ModelAdmin):
    list_display = ("id", "date_created")


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "date_created")


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "date_created")


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ("id", "date_created")


@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "date_created")


@admin.register(FaqsHelp)
class FaqsHelpAdmin(admin.ModelAdmin):
    list_display = ("id", "date_created")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("address", "email", "phone", "date_created")


class FulfilledOrderAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "date_ordered",
        "transaction_id",
        "status",
    ]  # Adjust the fields as needed


admin.site.register(FulfilledOrder, FulfilledOrderAdmin)


class CompletedOrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "date_ordered", "transaction_id", "status"]
    list_filter = ["status"]
    search_fields = ["customer__username", "transaction_id"]


admin.site.register(CompletedOrder, CompletedOrderAdmin)


class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "fulfilled_order", "date_created")
    list_filter = ("date_created",)
    search_fields = ("user__username", "fulfilled_order__transaction_id")
    readonly_fields = ("date_created",)


admin.site.register(RefundRequest, RefundRequestAdmin)


class UserInboxAdmin(admin.ModelAdmin):
    list_display = ("user", "sent_at", "subject")
    list_filter = ("sent_at", "user")


admin.site.register(UserInbox)


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("id", "ip_address")


@admin.register(VisitorMetadata)
class VisitorMetadataAdmin(admin.ModelAdmin):
    list_display = ("id", "visitor", "user_agent", "referer")


admin.site.register(Discount)

admin.site.register(DeliveryFee)
