from django.contrib import admin
from .models import SubscriptionPlan

# Register your models here.

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'level',
        'price',
        'duration_months',
        'rating',

    )

    ordering = ('level',)
    search_fields = ['name', 'description',]
    list_filter = ('category', 'level', 'price')

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)


