from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class DigitalServiceCategory(models.Model):
    """Enhanced categories for digital services with visual appeal"""
    name = models.CharField(_('Category Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    icon = models.CharField(_('Icon Class'), max_length=50, default='fas fa-cog')
    color = models.CharField(_('Color Class'), max_length=20, default='primary')
    gradient_start = models.CharField(_('Gradient Start Color'), max_length=7, default='#007bff')
    gradient_end = models.CharField(_('Gradient End Color'), max_length=7, default='#0056b3')
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)
    is_featured = models.BooleanField(_('Featured Category'), default=False)
    
    class Meta:
        verbose_name = _('Digital Service Category')
        verbose_name_plural = _('Digital Service Categories')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name

class DigitalService(models.Model):
    """Enhanced digital services with smart features"""
    SERVICE_STATUS_CHOICES = [
        ('active', _('Active')),
        ('maintenance', _('Under Maintenance')),
        ('inactive', _('Inactive')),
        ('beta', _('Beta Testing')),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', _('Easy - 5 min')),
        ('medium', _('Medium - 15 min')),
        ('hard', _('Hard - 30+ min')),
    ]
    
    URGENCY_CHOICES = [
        ('low', _('Low Priority')),
        ('medium', _('Medium Priority')),
        ('high', _('High Priority')),
        ('urgent', _('Urgent')),
    ]
    
    # Basic information
    name = models.CharField(_('Service Name'), max_length=200)
    description = models.TextField(_('Description'))
    short_description = models.CharField(_('Short Description'), max_length=150, blank=True)
    category = models.ForeignKey(DigitalServiceCategory, on_delete=models.CASCADE, related_name='services')
    
    # Visual elements
    icon = models.CharField(_('Icon Class'), max_length=50, default='fas fa-cog')
    color = models.CharField(_('Color Class'), max_length=20, default='primary')
    image = models.ImageField(_('Service Image'), upload_to='services/', blank=True, null=True)
    
    # Service details
    official_website = models.URLField(_('Official Website'), blank=True)
    service_url = models.URLField(_('Service URL'), blank=True)
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    
    # Service characteristics
    difficulty = models.CharField(_('Difficulty Level'), max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    urgency = models.CharField(_('Urgency Level'), max_length=10, choices=URGENCY_CHOICES, default='medium')
    estimated_time = models.CharField(_('Estimated Time'), max_length=50, blank=True)
    required_documents = models.TextField(_('Required Documents'), blank=True)
    fees = models.TextField(_('Fees'), blank=True)
    
    # Smart features
    is_automated = models.BooleanField(_('Fully Automated'), default=False)
    supports_bulk = models.BooleanField(_('Supports Bulk Operations'), default=False)
    has_express_lane = models.BooleanField(_('Express Lane Available'), default=False)
    requires_verification = models.BooleanField(_('Requires Verification'), default=True)
    
    # Status and visibility
    status = models.CharField(_('Status'), max_length=15, choices=SERVICE_STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(_('Featured Service'), default=False)
    is_popular = models.BooleanField(_('Popular Service'), default=False)
    is_new = models.BooleanField(_('New Service'), default=False)
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=0)
    
    # Statistics
    view_count = models.PositiveIntegerField(_('View Count'), default=0)
    success_rate = models.DecimalField(_('Success Rate (%)'), max_digits=5, decimal_places=2, default=0.00)
    completion_time_avg = models.PositiveIntegerField(_('Average Completion Time (minutes)'), default=0)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Digital Service')
        verbose_name_plural = _('Digital Services')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

class LifeEvent(models.Model):
    """Life events that trigger service recommendations"""
    name = models.CharField(_('Event Name'), max_length=100)
    description = models.TextField(_('Description'))
    icon = models.CharField(_('Icon Class'), max_length=50, default='fas fa-heart')
    color = models.CharField(_('Color Class'), max_length=20, default='primary')
    services = models.ManyToManyField(DigitalService, related_name='life_events')
    is_active = models.BooleanField(_('Active'), default=True)
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=0)
    
    class Meta:
        verbose_name = _('Life Event')
        verbose_name_plural = _('Life Events')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name

class UserServiceRequest(models.Model):
    """Enhanced user service requests with smart tracking"""
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('submitted', _('Submitted')),
        ('in_progress', _('In Progress')),
        ('pending_documents', _('Pending Documents')),
        ('pending_payment', _('Pending Payment')),
        ('under_review', _('Under Review')),
        ('approved', _('Approved')),
        ('completed', _('Completed')),
        ('rejected', _('Rejected')),
        ('cancelled', _('Cancelled')),
    ]
    
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('normal', _('Normal')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]
    
    # Request identification
    request_id = models.UUIDField(_('Request ID'), default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    service = models.ForeignKey(DigitalService, on_delete=models.CASCADE, related_name='requests')
    
    # Request details
    title = models.CharField(_('Request Title'), max_length=200)
    description = models.TextField(_('Description'))
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(_('Priority'), max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    # Contact information
    contact_phone = models.CharField(_('Contact Phone'), max_length=20, blank=True)
    contact_email = models.EmailField(_('Contact Email'), blank=True)
    
    # Documents and files
    documents = models.FileField(_('Documents'), upload_to='service_requests/', blank=True, null=True)
    additional_files = models.FileField(_('Additional Files'), upload_to='service_requests/', blank=True, null=True)
    
    # Progress tracking
    progress_percentage = models.PositiveIntegerField(_('Progress Percentage'), default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    current_step = models.CharField(_('Current Step'), max_length=100, blank=True)
    estimated_completion = models.DateTimeField(_('Estimated Completion'), blank=True, null=True)
    
    # Admin notes
    admin_notes = models.TextField(_('Admin Notes'), blank=True)
    admin_response = models.TextField(_('Admin Response'), blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    submitted_at = models.DateTimeField(_('Submitted At'), blank=True, null=True)
    completed_at = models.DateTimeField(_('Completed At'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('User Service Request')
        verbose_name_plural = _('User Service Requests')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.request_id} - {self.user.username} - {self.service.name}"
    
    def mark_submitted(self):
        self.status = 'submitted'
        self.submitted_at = timezone.now()
        self.save()
    
    def mark_completed(self):
        self.status = 'completed'
        self.progress_percentage = 100
        self.completed_at = timezone.now()
        self.save()

class ServiceStep(models.Model):
    """Step-by-step process for services"""
    service = models.ForeignKey(DigitalService, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(_('Step Title'), max_length=200)
    description = models.TextField(_('Step Description'))
    step_number = models.PositiveIntegerField(_('Step Number'))
    is_required = models.BooleanField(_('Required'), default=True)
    estimated_time = models.PositiveIntegerField(_('Estimated Time (minutes)'), default=5)
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Service Step')
        verbose_name_plural = _('Service Steps')
        ordering = ['service', 'step_number']
        unique_together = ['service', 'step_number']
    
    def __str__(self):
        return f"{self.service.name} - Step {self.step_number}: {self.title}"

class UserProfile(models.Model):
    """Enhanced user profile for personalized experience"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='digital_profile')
    
    # Personal information
    national_id = models.CharField(_('National ID'), max_length=20, blank=True)
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True)
    address = models.TextField(_('Address'), blank=True)
    city = models.CharField(_('City'), max_length=100, blank=True)
    postal_code = models.CharField(_('Postal Code'), max_length=10, blank=True)
    
    # Preferences
    preferred_language = models.CharField(_('Preferred Language'), max_length=10, default='fa')
    notification_preferences = models.JSONField(_('Notification Preferences'), default=dict)
    
    # Digital citizen stats
    points = models.PositiveIntegerField(_('Digital Citizen Points'), default=0)
    level = models.PositiveIntegerField(_('Digital Citizen Level'), default=1)
    services_completed = models.PositiveIntegerField(_('Services Completed'), default=0)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return f"{self.user.username} - Level {self.level}"

class ServiceReview(models.Model):
    """Enhanced service reviews with more details"""
    RATING_CHOICES = [
        (1, _('1 Star - Poor')),
        (2, _('2 Stars - Fair')),
        (3, _('3 Stars - Good')),
        (4, _('4 Stars - Very Good')),
        (5, _('5 Stars - Excellent')),
    ]
    
    service = models.ForeignKey(DigitalService, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_reviews')
    rating = models.PositiveIntegerField(_('Rating'), choices=RATING_CHOICES)
    comment = models.TextField(_('Comment'), blank=True)
    
    # Additional review aspects
    ease_of_use = models.PositiveIntegerField(_('Ease of Use'), choices=RATING_CHOICES, null=True, blank=True)
    speed = models.PositiveIntegerField(_('Speed'), choices=RATING_CHOICES, null=True, blank=True)
    helpfulness = models.PositiveIntegerField(_('Helpfulness'), choices=RATING_CHOICES, null=True, blank=True)
    
    is_verified = models.BooleanField(_('Verified'), default=False)
    is_helpful = models.PositiveIntegerField(_('Helpful Votes'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Service Review')
        verbose_name_plural = _('Service Reviews')
        ordering = ['-created_at']
        unique_together = ['service', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.rating} stars)"

class ServiceNotification(models.Model):
    """Enhanced notifications for services"""
    NOTIFICATION_TYPES = [
        ('maintenance', _('Maintenance')),
        ('update', _('Update')),
        ('announcement', _('Announcement')),
        ('reminder', _('Reminder')),
        ('promotion', _('Promotion')),
        ('deadline', _('Deadline')),
    ]
    
    service = models.ForeignKey(DigitalService, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(_('Title'), max_length=200)
    message = models.TextField(_('Message'))
    notification_type = models.CharField(_('Type'), max_length=15, choices=NOTIFICATION_TYPES)
    icon = models.CharField(_('Icon Class'), max_length=50, default='fas fa-bell')
    color = models.CharField(_('Color Class'), max_length=20, default='info')
    
    is_active = models.BooleanField(_('Active'), default=True)
    is_urgent = models.BooleanField(_('Urgent'), default=False)
    start_date = models.DateTimeField(_('Start Date'))
    end_date = models.DateTimeField(_('End Date'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Service Notification')
        verbose_name_plural = _('Service Notifications')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.service.name} - {self.title}"
    
    @property
    def is_current(self):
        now = timezone.now()
        return (self.is_active and 
                self.start_date <= now and 
                (self.end_date is None or self.end_date >= now))

class QuickAction(models.Model):
    """Quick action buttons for common services"""
    name = models.CharField(_('Action Name'), max_length=100)
    description = models.CharField(_('Description'), max_length=200)
    icon = models.CharField(_('Icon Class'), max_length=50, default='fas fa-bolt')
    color = models.CharField(_('Color Class'), max_length=20, default='primary')
    service = models.ForeignKey(DigitalService, on_delete=models.CASCADE, related_name='quick_actions')
    is_active = models.BooleanField(_('Active'), default=True)
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=0)
    
    class Meta:
        verbose_name = _('Quick Action')
        verbose_name_plural = _('Quick Actions')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
