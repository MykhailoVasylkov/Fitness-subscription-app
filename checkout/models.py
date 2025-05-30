# Code snippet form Boutique Ado
import uuid

from django.db import models
from django.db.models import Sum

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile
from settings.models import DeliverySettings
from plans.models import SubscriptionPlanSnapshot


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
    ]
    order_number = models.CharField(max_length=32, null=False, editable=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        default=0
    )
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default=''
    )

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = (
            self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum']
            or 0
        )
        settings = DeliverySettings.get_solo()
        if self.order_total < settings.free_delivery_threshold:
            self.delivery_cost = (
                self.order_total * settings.standard_delivery_percentage / 100
            )
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    product_size = models.CharField(max_length=3, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'


class Subscription(models.Model):
    subscription_number = models.CharField(
        max_length=32,
        null=False,
        editable=False
    )
    date = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscriptions'
    )
    subscription_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=255, null=True, blank=True)

    def _generate_subscription_number(self):
        """
        Generate a random, unique subscription number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        # Generate subscription number if it is not set
        if not self.subscription_number:
            self.subscription_number = self._generate_subscription_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Subscription {self.subscription_number} "
            f"({self.user_profile.user.username})"
        )


class SubscriptionLineItem(models.Model):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    plan = models.ForeignKey(
        SubscriptionPlanSnapshot,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        default=1
    )
    quantity = models.PositiveIntegerField(default=1)
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.plan.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plan.name} (x{self.quantity})"
