from django.contrib import admin
from django.utils.html import format_html
from .models import PrintOrder, UploadedFile, PaymentSettings

@admin.register(PrintOrder)
class PrintOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('name', 'email', 'phone')

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'file', 'uploaded_at')
    search_fields = ('order__id', 'file')

@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'formatted_account_number', 'formatted_card_number', 'formatted_shaba_number', 'updated_at')
    list_display_links = ('bank_name',)
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Bank Information', {
            'fields': ('bank_name',)
        }),
        ('Account Details', {
            'fields': ('account_number', 'card_number', 'shaba_number'),
            'description': 'Enter the bank account details that customers will use for payments.'
        }),
        ('System Information', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_account_number(self, obj):
        if obj.account_number:
            # Show only last 4 digits for security
            return f"****{obj.account_number[-4:]}" if len(obj.account_number) >= 4 else "****"
        return "Not set"
    formatted_account_number.short_description = "Account Number"
    
    def formatted_card_number(self, obj):
        if obj.card_number:
            # Show only last 4 digits for security
            return f"****{obj.card_number[-4:]}" if len(obj.card_number) >= 4 else "****"
        return "Not set"
    formatted_card_number.short_description = "Card Number"
    
    def formatted_shaba_number(self, obj):
        if obj.shaba_number:
            # Show only last 4 digits for security
            return f"****{obj.shaba_number[-4:]}" if len(obj.shaba_number) >= 4 else "****"
        return "Not set"
    formatted_shaba_number.short_description = "Shaba Number"
    
    def has_add_permission(self, request):
        # Only allow one PaymentSettings instance
        return not PaymentSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of PaymentSettings
        return False
    
    def message_user(self, request, message, level=None, extra_tags='', fail_silently=False):
        # Custom success message
        if "was added successfully" in message:
            message = "Bank account details have been configured successfully!"
        elif "was changed successfully" in message:
            message = "Bank account details have been updated successfully!"
        super().message_user(request, message, level, extra_tags, fail_silently)