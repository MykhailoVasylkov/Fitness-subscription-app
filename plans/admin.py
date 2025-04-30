from django.contrib import admin
import nested_admin
from .models import SubscriptionPlan, Week, Day, DayContentItem


# Register your models here.

class DayContentInline(nested_admin.NestedTabularInline):
    model = DayContentItem
    extra = 1


class DayInline(nested_admin.NestedStackedInline):
    model = Day
    inlines = [DayContentInline]
    extra = 1


class WeekInline(nested_admin.NestedStackedInline):
    model = Week
    inlines = [DayInline]
    extra = 1


class SubscriptionPlanAdmin(nested_admin.NestedModelAdmin):
    inlines = [WeekInline]

    list_display = (
        'name',
        'category',
        'level',
        'price',
        'duration_weeks',
        'rating',
    )
    ordering = ('level',)
    search_fields = ['name', 'description']
    list_filter = ('category', 'level', 'price')


admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)