from django.contrib import admin
from .models import TypingOrder, TypedFile, TypingPriceSettings
from django.utils.translation import gettext_lazy as _

@admin.register(TypingOrder)
class TypingOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'status', 'total_price', 'created_at', 'final_approved')
    list_filter = ('status', 'final_approved', 'created_at')
    search_fields = ('user_name', 'user_email', 'id')
    
    # Allow admin to edit these fields in the change view
    readonly_fields = ('created_at', 'updated_at')
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