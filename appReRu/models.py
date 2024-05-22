from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from decimal import Decimal


class Advertisement(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="banners/", blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Advertisement1(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="banners/", blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Advertisement2(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="banners/", blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Advertisement3(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="banners/", blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review for {self.product.name} by {self.name}"


class Category(models.Model):
    JACKETS = "Jackets"
    SWEATPANTS = "SweatPants"
    CAPS = "Caps"

    CATEGORY_CHOICES = [
        (JACKETS, "JACKETS"),
        (SWEATPANTS, "SWEATPANTS"),
        (CAPS, "CAPS"),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"This is {self.name} Category"


class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ("available", "Available"),
        ("sold_out", "Sold Out"),
    ]

    availability_status = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default="available"
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    categories = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.FloatField(null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    details_1 = models.TextField(null=True, blank=True)
    details_2 = models.TextField(null=True, blank=True)
    details_3 = models.TextField(null=True, blank=True)
    seller_name = models.CharField(max_length=100, null=True, blank=True)
    seller_id = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    unique_id = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)  # New field for quantity
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.unique_id}"

    def save(self, *args, **kwargs):
        if not self.unique_id:  # Generate unique_id only if it's not already set
            if self.seller_name:  # Check if seller_name is not None
                self.unique_id = f"{self.seller_name}.{self.created}.{self.name}"
            else:
                # If seller_name is None, generate unique_id without including seller_name
                self.unique_id = f"{self.created}.{self.name}"
        super().save(*args, **kwargs)


class Order(models.Model):
    STATUS_CHOICES = (
        ("fulfilled", "Fulfilled"),
        ("unfulfilled", "Unfulfilled"),
    )

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="unfulfilled"
    )

    def __str__(self):
        return f"Order by {self.customer.username} and Order Num = {str(self.id)}"

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if not i.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = Decimal("0.0")  # Initialize total as Decimal

        # Sum each item's total price as Decimal
        total += sum([Decimal(item.get_total) for item in orderitems])

        # Retrieve the delivery fee
        delivery_fee = DeliveryFee.objects.first()
        if delivery_fee:
            total += Decimal(delivery_fee.amount)

        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class CompletedOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField()
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)


@receiver(post_save, sender=Order)
def create_or_update_completed_order(sender, instance, created, **kwargs):
    if instance.complete:
        if created:  # If the Order instance was just created
            CompletedOrder.objects.create(
                customer=instance.customer,
                date_ordered=instance.date_ordered,
                transaction_id=instance.transaction_id,
                status=instance.status,
            )
        else:  # If the Order instance was updated
            completed_order = CompletedOrder.objects.filter(
                customer=instance.customer, transaction_id=instance.transaction_id
            ).first()
            if completed_order:
                completed_order.date_ordered = instance.date_ordered
                completed_order.status = instance.status
                completed_order.save()
            else:
                CompletedOrder.objects.create(
                    customer=instance.customer,
                    date_ordered=instance.date_ordered,
                    transaction_id=instance.transaction_id,
                    status=instance.status,
                )


class FulfilledOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField()
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)

    def __str__(self):
        return self.transaction_id


@receiver(post_save, sender=Order)
def create_or_delete_fulfilled_order(sender, instance, created, **kwargs):
    if instance.status == "fulfilled":
        if created:  # If the Order instance was just created
            FulfilledOrder.objects.create(
                customer=instance.customer,
                date_ordered=instance.date_ordered,
                transaction_id=instance.transaction_id,
                status=instance.status,
            )
        else:  # If the Order instance was updated
            fulfilled_order = FulfilledOrder.objects.filter(
                customer=instance.customer, transaction_id=instance.transaction_id
            ).first()
            if fulfilled_order:
                fulfilled_order.date_ordered = instance.date_ordered
                fulfilled_order.status = instance.status
                fulfilled_order.save()
            else:
                FulfilledOrder.objects.create(
                    customer=instance.customer,
                    date_ordered=instance.date_ordered,
                    transaction_id=instance.transaction_id,
                    status=instance.status,
                )
    elif instance.status != "fulfilled":
        fulfilled_order = FulfilledOrder.objects.filter(
            customer=instance.customer, transaction_id=instance.transaction_id
        ).first()
        if fulfilled_order:
            fulfilled_order.delete()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    original_quantity = models.IntegerField(
        default=0
    )  # New field to store the original quantity
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    order_notes = models.TextField(null=True)

    def __str__(self):
        return self.address


# footer


class OurSocials(models.Model):
    facebook = models.URLField(max_length=150, null=True, blank=True)
    twitter = models.URLField(max_length=150, null=True, blank=True)
    linkedin = models.URLField(max_length=150, null=True, blank=True)
    youtube = models.URLField(max_length=150, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_created}"


class ContactUs(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date_created}"


class PrivacyPolicy(models.Model):
    policy = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_created}"


class TermsAndConditions(models.Model):
    terms = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_created}"


class ReturnPolicy(models.Model):
    policy = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_created}"


class FaqsHelp(models.Model):
    help_payment_made = models.TextField(null=True, blank=True)
    help_how_paypal = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_created}"


class Contact(models.Model):
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_created}"


class RefundRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fulfilled_order = models.OneToOneField("FulfilledOrder", on_delete=models.CASCADE)
    reason = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund Request from {self.user.username} for Order ID {self.fulfilled_order.transaction_id}"


class UserInbox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # New field to track read status

    def __str__(self):
        return f"Inbox for {self.user.username} sent at {self.sent_at}"


# METADATA FOR OUR WEBSITE


class Visitor(models.Model):
    ip_address = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Visitor at {self.timestamp} with IP {self.ip_address}"


class VisitorMetadata(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    user_agent = models.CharField(max_length=200)
    referer = models.URLField(
        max_length=200, blank=True, null=True
    )  # URL from which the visitor arrived
    language = models.CharField(
        max_length=100, blank=True, null=True
    )  # Language preference of the visitor
    screen_resolution = models.CharField(
        max_length=20, blank=True, null=True
    )  # Screen resolution of the visitor's device
    browser = models.CharField(
        max_length=50, blank=True, null=True
    )  # Name of the visitor's browser
    operating_system = models.CharField(
        max_length=50, blank=True, null=True
    )  # Operating system of the visitor's device
    device_type = models.CharField(
        max_length=50, blank=True, null=True
    )  # Type of device used by the visitor (desktop, mobile, tablet)
    timezone = models.CharField(
        max_length=50, blank=True, null=True
    )  # Timezone of the visitor
    country = models.CharField(
        max_length=100, blank=True, null=True
    )  # Country of the visitor
    city = models.CharField(
        max_length=100, blank=True, null=True
    )  # City of the visitor
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )  # Latitude of the visitor's location
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )  # Longitude of the visitor's location
    # Add more metadata fields as needed

    def __str__(self):
        return f"Visitor at {self.visitor.timestamp} with IP {self.visitor.ip_address}"


# Discount and Delivery Fee


class Discount(models.Model):
    amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Enter the discount amount in percentage",
    )

    def __str__(self):
        return f"{self.amount}%"


class DeliveryFee(models.Model):
    amount = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Enter the delivery fee amount in USD"
    )

    def __str__(self):
        return f"${self.amount}"
