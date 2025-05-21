from django.contrib import admin
from .models import CommunityPost

# Register your models here.

class CommunityPostAdmin(admin.ModelAdmin):
    model = CommunityPost

    list_display = ('author', 'created_on', 'approved',)
    search_fields = ['author', 'body', ]
    list_filter = ('approved',)

admin.site.register(CommunityPost, CommunityPostAdmin)