# I used code snippet form Boutique Ado
from django.contrib import admin
from .models import Order, OrderLineItem, Subscription, SubscriptionLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid',)

    fields = ('order_number', 'status', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag',
              'stripe_pid',)

    list_display = ('order_number', 'status', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)


class SubscriptionLineItemInline(admin.TabularInline):
    model = SubscriptionLineItem
    readonly_fields = ('plan', 'quantity')
    extra = 0


class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriptionLineItemInline]

    readonly_fields = (
        'subscription_number',
        'original_bag',
        'stripe_pid',
        'subscription_total',
        'date',
    )

    fields = ('subscription_number', 'date', 'user_profile', 'full_name',
              'email', 'original_bag', 'stripe_pid', 'subscription_total')

    list_display = (
        'subscription_number',
        'subscription_total',
        'full_name',
        'email',
        'date',
    )

    ordering = ('-date',)


admin.site.register(Subscription, SubscriptionAdmin)
