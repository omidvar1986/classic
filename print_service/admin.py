from django.contrib import admin
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
    list_display = ('bank_name', 'account_number', 'card_number', 'shaba_number', 'updated_at')