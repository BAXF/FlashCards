from django.contrib import admin
from django.utils.html import format_html
from .models import Card, CardGroup

admin.site.site_header = 'FlashCard Admin'
admin.site.site_title = 'FlashCard Admin Area'
admin.site.index_title = 'Welcome to the FlashCard Admin Area'

@admin.register(CardGroup)
class CardGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'status', 'user', 'image_preview', 'created_at')
    list_filter = ('status', 'group', 'created_at', 'user')
    search_fields = ('name', 'description')
    readonly_fields = ('uuid', 'created_at', 'updated_at', 'image_preview')
    list_editable = ('status',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.user = request.user
        super().save_model(request, obj, form, change)
