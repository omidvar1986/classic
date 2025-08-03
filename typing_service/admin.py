from django.contrib import admin
from .models import TypingOrder, TypedFile, TypingPriceSettings, TypingOrderAccessory
from django.utils.translation import gettext_lazy as _

class TypingOrderAccessoryInline(admin.TabularInline):
    model = TypingOrderAccessory
    extra = 0
    readonly_fields = ['price']
    fields = ['accessory', 'quantity', 'price']

@admin.register(TypingOrder)
class TypingOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'status', 'total_price', 'created_at', 'final_approved', 'get_total_price')
    list_filter = ('status', 'final_approved', 'created_at')
    search_fields = ('user_name', 'user_email', 'id')
    inlines = [TypingOrderAccessoryInline]
    
    # Allow admin to edit these fields in the change view
    readonly_fields = ('created_at', 'updated_at', 'get_total_price', 'get_accessories_total')
    fieldsets = (
        (_('Order Information'), {
            'fields': ('user_name', 'user_email', 'user_phone', 'description', 'document_file')
        }),
        (_('Pricing and Status'), {
            'fields': ('status', 'page_count', 'total_price', 'payment_slip')
        }),
        (_('Finalization'), {
            'fields': ('final_approved', 'final_note', 'final_approved_by_user', 'delivery_option')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at', 'estimated_delivery')
        }),
    )
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price()} تومان"
    get_total_price.short_description = 'Total Price (with accessories)'
    
    def get_accessories_total(self, obj):
        return f"{obj.get_accessories_total()} تومان"
    get_accessories_total.short_description = 'Accessories Total'

@admin.register(TypedFile)
class TypedFileAdmin(admin.ModelAdmin):
    list_display = ('order', 'file', 'uploaded_at')
    search_fields = ('order__user_name',)

@admin.register(TypingPriceSettings)
class TypingPriceSettingsAdmin(admin.ModelAdmin):
    list_display = ('price_per_page',)

    def has_add_permission(self, request):
        # Prevent creating more than one settings object
        return not TypingPriceSettings.objects.exists()