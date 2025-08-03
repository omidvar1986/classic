from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import (
    DigitalServiceCategory, DigitalService, UserServiceRequest, 
    ServiceReview, ServiceStep, UserProfile, ServiceNotification,
    LifeEvent, QuickAction
)

@admin.register(DigitalServiceCategory)
class DigitalServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color', 'is_featured', 'is_active', 'sort_order']
    list_filter = ['is_active', 'is_featured']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_featured', 'sort_order']
    ordering = ['sort_order', 'name']

@admin.register(DigitalService)
class DigitalServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'difficulty', 'urgency', 'status',
        'is_featured', 'is_popular', 'is_new', 'view_count', 'success_rate'
    ]
    list_filter = [
        'status', 'difficulty', 'urgency', 'category', 
        'is_featured', 'is_popular', 'is_new', 'is_automated'
    ]
    search_fields = ['name', 'description', 'short_description']
    list_editable = ['status', 'is_featured', 'is_popular', 'is_new']
    readonly_fields = ['view_count', 'success_rate', 'completion_time_avg']
    filter_horizontal = ['life_events']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'short_description', 'description', 'category')
        }),
        (_('Visual Elements'), {
            'fields': ('icon', 'color', 'image')
        }),
        (_('Service Details'), {
            'fields': ('official_website', 'service_url', 'phone_number', 'email')
        }),
        (_('Service Characteristics'), {
            'fields': ('difficulty', 'urgency', 'estimated_time', 'required_documents', 'fees')
        }),
        (_('Smart Features'), {
            'fields': ('is_automated', 'supports_bulk', 'has_express_lane', 'requires_verification')
        }),
        (_('Status and Visibility'), {
            'fields': ('status', 'is_featured', 'is_popular', 'is_new', 'sort_order')
        }),
        (_('Statistics'), {
            'fields': ('view_count', 'success_rate', 'completion_time_avg'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(UserServiceRequest)
class UserServiceRequestAdmin(admin.ModelAdmin):
    list_display = [
        'request_id', 'user', 'service', 'status', 'priority', 
        'progress_percentage', 'created_at'
    ]
    list_filter = ['status', 'priority', 'service__category', 'created_at']
    search_fields = ['request_id', 'user__username', 'user__email', 'service__name']
    readonly_fields = ['request_id', 'created_at', 'updated_at', 'submitted_at', 'completed_at']
    list_editable = ['status', 'priority', 'progress_percentage']
    
    fieldsets = (
        (_('Request Information'), {
            'fields': ('request_id', 'user', 'service', 'title', 'description')
        }),
        (_('Status and Progress'), {
            'fields': ('status', 'priority', 'progress_percentage', 'current_step', 'estimated_completion')
        }),
        (_('Contact Information'), {
            'fields': ('contact_phone', 'contact_email')
        }),
        (_('Documents'), {
            'fields': ('documents', 'additional_files')
        }),
        (_('Admin Notes'), {
            'fields': ('admin_notes', 'admin_response')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at', 'submitted_at', 'completed_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ServiceStep)
class ServiceStepAdmin(admin.ModelAdmin):
    list_display = ['service', 'step_number', 'title', 'is_required', 'estimated_time', 'is_active']
    list_filter = ['service', 'is_required', 'is_active']
    search_fields = ['service__name', 'title', 'description']
    list_editable = ['step_number', 'is_required', 'is_active', 'estimated_time']
    ordering = ['service', 'step_number']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'level', 'points', 'services_completed', 
        'national_id', 'phone_number', 'city'
    ]
    list_filter = ['level', 'preferred_language']
    search_fields = ['user__username', 'user__email', 'national_id', 'phone_number']
    readonly_fields = ['points', 'level', 'services_completed']
    
    fieldsets = (
        (_('User Information'), {
            'fields': ('user', 'national_id', 'phone_number')
        }),
        (_('Address Information'), {
            'fields': ('address', 'city', 'postal_code')
        }),
        (_('Preferences'), {
            'fields': ('preferred_language', 'notification_preferences')
        }),
        (_('Digital Citizen Stats'), {
            'fields': ('points', 'level', 'services_completed'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'service', 'rating', 'ease_of_use', 'speed', 
        'helpfulness', 'is_verified', 'created_at'
    ]
    list_filter = ['rating', 'is_verified', 'service__category', 'created_at']
    search_fields = ['user__username', 'service__name', 'comment']
    readonly_fields = ['created_at']
    list_editable = ['is_verified']

@admin.register(LifeEvent)
class LifeEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color', 'is_active', 'sort_order', 'services_count']
    list_filter = ['is_active', 'color']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'sort_order']
    filter_horizontal = ['services']
    
    def services_count(self, obj):
        return obj.services.count()
    services_count.short_description = _('Services Count')

@admin.register(QuickAction)
class QuickActionAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'icon', 'color', 'is_active', 'sort_order']
    list_filter = ['is_active', 'color', 'service__category']
    search_fields = ['name', 'description', 'service__name']
    list_editable = ['is_active', 'sort_order']

@admin.register(ServiceNotification)
class ServiceNotificationAdmin(admin.ModelAdmin):
    list_display = [
        'service', 'title', 'notification_type', 'is_active', 
        'is_urgent', 'start_date', 'is_current'
    ]
    list_filter = ['notification_type', 'is_active', 'is_urgent', 'service__category']
    search_fields = ['service__name', 'title', 'message']
    list_editable = ['is_active', 'is_urgent']
    readonly_fields = ['is_current']
    
    fieldsets = (
        (_('Notification Information'), {
            'fields': ('service', 'title', 'message', 'notification_type')
        }),
        (_('Visual Elements'), {
            'fields': ('icon', 'color')
        }),
        (_('Status and Timing'), {
            'fields': ('is_active', 'is_urgent', 'start_date', 'end_date')
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
