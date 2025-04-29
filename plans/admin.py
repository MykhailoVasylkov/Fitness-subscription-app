from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from .models import SubscriptionPlan
from django.db import models


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

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)


