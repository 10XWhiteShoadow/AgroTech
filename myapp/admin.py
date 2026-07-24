from django.contrib import admin
from .models import Polygon, Details, tools, Crop, HistoricalPrice, ResourceItem
# Register your models here.
admin.site.register(Polygon)
admin.site.register(Details)
admin.site.register(tools)
class HistoricalPriceInline(admin.TabularInline):
    model = HistoricalPrice
    extra = 1

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    inlines = [HistoricalPriceInline]
    list_display = ('name', 'current_price', 'trend', 'updated_at')
    search_fields = ('name',)
    list_filter = ('trend',)
    
@admin.register(ResourceItem)
class ResourceItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price_range', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'price_range')
    fieldsets = (
        (None, {
            'fields': ('category', 'title')
        }),
        ('Product Details', {
            'fields': ('link', 'img_url', 'price_range')
        }),
    )