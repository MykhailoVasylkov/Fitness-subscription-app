from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'email', 'avatar_path')

    def avatar_path(self, obj):
        return obj.avatar.url if obj.avatar else 'No avatar'
    avatar_path.short_description = 'Avatar URL'
