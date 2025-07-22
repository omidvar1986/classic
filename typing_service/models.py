# typing_service/models.py

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class TypingOrder(models.Model):
    STATUS_CHOICES = [
        ('pending_review', _('Pending Review')),
        ('awaiting_payment', _('Awaiting Payment')),
        ('awaiting_approval', _('Awaiting Approval')),
        ('in_progress', _('In Progress')),
        ('awaiting_final_approval', _('Awaiting Final Approval')),
        ('completed', _('Completed')),
        ('rejected', _('Rejected')),
    ]

    DELIVERY_CHOICES = [
        ('print', _('Printed by staff')),
        ('email', _('Sent to email')),
    ]

    # Customer and order details
    user_name = models.CharField(_('User Name'), max_length=100)
    user_email = models.EmailField(_('User Email'), blank=True, null=True)
    user_phone = models.CharField(_('User Phone'), max_length=20, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True)
    document_file = models.FileField(_('Document to Type'), upload_to='typing_documents/', blank=True, null=True)
    
    # Pricing and payment
    page_count = models.PositiveIntegerField(_('Page Count'), default=1)
    total_price = models.PositiveIntegerField(_('Total Price'), default=0, help_text=_("Set by admin after review."))
    payment_slip = models.ImageField(_('Payment Slip'), upload_to='typing_payment_slips/', blank=True, null=True)
    
    # Status and workflow
    status = models.CharField(_('Status'), max_length=30, choices=STATUS_CHOICES, default='pending_review')
    
    # Finalization by admin
    final_approved = models.BooleanField(_('Admin Final Approval'), default=False)
    final_note = models.TextField(_('Admin Final Note'), blank=True, null=True)

    # Finalization by user
    final_approved_by_user = models.BooleanField(_('User Final Approval'), default=False)
    delivery_option = models.CharField(_('Delivery Option'), max_length=10, choices=DELIVERY_CHOICES, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateTimeField(_('Estimated Delivery'), blank=True, null=True)

    def __str__(self):
        return f"Typing Order #{self.id} - {self.user_name}"


class TypedFile(models.Model):
    order = models.ForeignKey(TypingOrder, on_delete=models.CASCADE, related_name='typed_files')
    file = models.FileField(upload_to='typed_files/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Typed File for Order #{self.order.id}"


class TypingPriceSettings(models.Model):
    price_per_page = models.PositiveIntegerField(
        _('Price per Page'),
        default=1000,
        help_text=_("The default price per page for a standard typing order.")
    )

    def __str__(self):
        return _("Typing Pricing Settings")

    class Meta:
        verbose_name = _("Typing Pricing Settings")
        verbose_name_plural = _("Typing Pricing Settings")
