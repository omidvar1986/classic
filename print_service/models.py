from django.db import models

# Create your models here.

class PrintOrder(models.Model):
    # Customer information (can be linked to User model later)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Print options
    COLOR_CHOICES = [
        ('color', 'Color'),
        ('bw', 'Black & White'),
    ]
    color_mode = models.CharField(max_length=10, choices=COLOR_CHOICES)

    SIDE_CHOICES = [
        ('single', 'Single-sided'),
        ('double', 'Double-sided'),
    ]
    side_type = models.CharField(max_length=10, choices=SIDE_CHOICES)

    PAPER_SIZE_CHOICES = [
        ('A4', 'A4'),
        ('A3', 'A3'),
        ('A5', 'A5'),
        ('Letter', 'Letter'),
    ]
    paper_size = models.CharField(max_length=10, choices=PAPER_SIZE_CHOICES)
    num_copies = models.PositiveIntegerField(default=1)

    # Order status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('ready', 'Ready for Pickup/Delivery'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Delivery method
    DELIVERY_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    ]
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    address = models.TextField(blank=True, null=True)  # Only for delivery

    # Payment
    PAYMENT_CHOICES = [
        ('online', 'Online'),
        ('cod', 'Cash on Delivery'),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    is_paid = models.BooleanField(default=False)

    # Online payment slip upload and approval
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    payment_slip = models.ImageField(upload_to='payment_slips/', blank=True, null=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name} ({self.status})"

class UploadedFile(models.Model):
    order = models.ForeignKey(PrintOrder, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='print_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Order #{self.order.id}: {self.file.name}"



class PaymentSettings(models.Model):
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=30)
    card_number = models.CharField(max_length=30)
    shaba_number = models.CharField(max_length=34)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank_name} - {self.card_number}"