from django.contrib import admin
from django.utils.html import format_html
from .models import PrintOrder, UploadedFile, PaymentSettings, Accessory, PackageDeal, PrintOrderAccessory, PrintPriceSettings

class PrintOrderAccessoryInline(admin.TabularInline):
    model = PrintOrderAccessory
    extra = 0
    readonly_fields = ['price']
    fields = ['accessory', 'quantity', 'price']

@admin.register(PrintOrder)
class PrintOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'status', 'created_at', 'get_total_price']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email']
    inlines = [PrintOrderAccessoryInline]
    readonly_fields = ['get_total_price', 'get_accessories_total']
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price()} تومان"
    get_total_price.short_description = 'Total Price'
    
    def get_accessories_total(self, obj):
        return f"{obj.get_accessories_total()} تومان"
    get_accessories_total.short_description = 'Accessories Total'

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['order', 'file', 'uploaded_at']

@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'card_number', 'updated_at']

@admin.register(PrintPriceSettings)
class PrintPriceSettingsAdmin(admin.ModelAdmin):
    list_display = ['base_price_per_page', 'color_price_multiplier', 'double_sided_discount', 'updated_at']
    fieldsets = (
        ('Base Pricing', {
            'fields': ('base_price_per_page',)
        }),
        ('Price Modifiers', {
            'fields': ('color_price_multiplier', 'double_sided_discount'),
            'description': 'Configure how different print options affect the final price'
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent creating more than one settings object
        return not PrintPriceSettings.objects.exists()

@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'service_type', 'base_price', 'is_active']
    list_filter = ['category', 'service_type', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['category', 'sort_order', 'name']

@admin.register(PackageDeal)
class PackageDealAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'discount_price', 'original_price', 'savings', 'is_active']
    list_filter = ['service_type', 'is_active']
    search_fields = ['name', 'description']
    filter_horizontal = ['accessories']

@admin.register(PrintOrderAccessory)
class PrintOrderAccessoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'accessory', 'quantity', 'price']
    list_filter = ['accessory__category']
    search_fields = ['order__name', 'accessory__name']