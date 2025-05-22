from django.contrib import admin
from .models import NewsletterSubscriber
# Register your models here.

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active', 'unsubscribe_token')
    list_filter = ('is_active',)
    search_fields = ('email',)
    readonly_fields = ('unsubscribe_token',)
