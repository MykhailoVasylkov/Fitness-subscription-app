from django.contrib import admin
from .models import Product, Category, ProductSize, Brand

# Register your models here.
"""
Register ProductSize model in admin panel.
"""

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


"""
Register Product model in admin panel.
Add how product items is displaying.
Add search functionality.
Add filter functionality.
"""

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)
    search_fields = ['name', 'description', 'sku']
    list_filter = ('category', 'status', 'price')
    inlines = [ProductSizeInline]

"""
Register Category model in admin panel.
Add how category items is displaying.
"""

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

"""
Register Brand model in admin panel.
"""

class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)