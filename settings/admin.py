from django.contrib import admin
from .models import DeliverySettings
from solo.admin import SingletonModelAdmin

"""
Register DeliverySettings model in admin panel.
"""

@admin.register(DeliverySettings)
class DeliverySettingsAdmin(SingletonModelAdmin):
    list_display = ('free_delivery_threshold', 'standard_delivery_percentage')
    fieldsets = (
        (None, {
            'fields': ('free_delivery_threshold', 'standard_delivery_percentage'),
            'description': 'Delivery settings displayed when placing an order.',
        }),
    )