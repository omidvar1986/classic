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
        ('pending', 'Pending Review'),
        ('awaiting_payment', 'Awaiting Payment'),
        ('awaiting_approval', 'Awaiting Approval'),
        ('processing', 'In Progress'),
        ('ready', 'Ready for Pickup/Delivery'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
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
    
    def get_total_price(self):
        """Get total price including accessories"""
        base_price = self.calculate_base_price()
        accessories_price = sum(acc.price for acc in self.accessories.all())
        return base_price + accessories_price
    
    def calculate_base_price(self):
        """Calculate base price based on print settings"""
        try:
            settings = PrintPriceSettings.objects.first()
            if not settings:
                return 50000  # Default price
            
            base_price = settings.base_price_per_page
            
            # Apply color multiplier
            if self.color_mode == 'color':
                base_price = int(base_price * settings.color_price_multiplier)
            
            # Apply double-sided discount
            if self.side_type == 'double':
                base_price = int(base_price * settings.double_sided_discount)
            
            # Multiply by number of copies
            return base_price * self.num_copies
            
        except Exception:
            return 50000  # Fallback price
    
    def get_accessories_total(self):
        """Get total price of accessories only"""
        return sum(acc.price for acc in self.accessories.all())
    
    def get_accessories_list(self):
        """Get list of accessories with details"""
        return [
            {
                'name': acc.accessory.name,
                'quantity': acc.quantity,
                'price': acc.price,
                'category': acc.accessory.get_category_display()
            }
            for acc in self.accessories.all()
        ]

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


class PrintPriceSettings(models.Model):
    """Pricing settings for print services"""
    base_price_per_page = models.PositiveIntegerField(
        default=50000,
        help_text="قیمت پایه هر صفحه (تومان)"
    )
    color_price_multiplier = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.5,
        help_text="ضریب قیمت برای پرینت رنگی (1.5 = 50% گران‌تر)"
    )
    double_sided_discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.8,
        help_text="تخفیف برای پرینت دو رو (0.8 = 20% تخفیف)"
    )
    # Additional pricing options
    a4_price = models.PositiveIntegerField(default=50000, help_text="قیمت صفحه A4")
    a3_price = models.PositiveIntegerField(default=100000, help_text="قیمت صفحه A3")
    a5_price = models.PositiveIntegerField(default=30000, help_text="قیمت صفحه A5")
    letter_price = models.PositiveIntegerField(default=45000, help_text="قیمت صفحه Letter")
    
    # Bulk discounts
    bulk_discount_10 = models.DecimalField(max_digits=3, decimal_places=2, default=0.95, help_text="تخفیف برای 10+ صفحه")
    bulk_discount_50 = models.DecimalField(max_digits=3, decimal_places=2, default=0.90, help_text="تخفیف برای 50+ صفحه")
    bulk_discount_100 = models.DecimalField(max_digits=3, decimal_places=2, default=0.85, help_text="تخفیف برای 100+ صفحه")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Print Pricing Settings - Base: {self.base_price_per_page} تومان"

    class Meta:
        verbose_name = "Print Pricing Settings"
        verbose_name_plural = "Print Pricing Settings"

    def has_add_permission(self, request):
        # Prevent creating more than one settings object
        return not PrintPriceSettings.objects.exists()

class Accessory(models.Model):
    """Accessories for print and typing orders with Digikala-style pricing"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='accessories/', blank=True, null=True, help_text="تصویر لوازم جانبی")
    category = models.CharField(max_length=50, choices=[
        ('binding', 'گزینه‌های صحافی'),
        ('finishing', 'گزینه‌های تکمیل'),
        ('packaging', 'بسته‌بندی'),
        ('paper', 'گزینه‌های کاغذ'),
        ('delivery', 'تحویل'),
        ('priority', 'اولویت')
    ])
    service_type = models.CharField(max_length=20, choices=[
        ('print', 'سرویس پرینت'),
        ('typing', 'سرویس تایپ'),
        ('both', 'هر دو سرویس')
    ])
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="نمایش در بخش ویژه")
    icon = models.CharField(max_length=50, default='fas fa-tag')
    sort_order = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=7, default='#007bff', help_text="رنگ نمایش (کد هگز)")
    
    class Meta:
        ordering = ['category', 'sort_order', 'name']
        verbose_name_plural = 'Accessories'
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class PackageDeal(models.Model):
    """Package deals for accessories with discounts"""
    name = models.CharField(max_length=100)
    accessories = models.ManyToManyField(Accessory)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    service_type = models.CharField(max_length=20, choices=[
        ('print', 'Print Service'),
        ('typing', 'Typing Service'),
        ('both', 'Both Services')
    ])
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (Save ${self.original_price - self.discount_price})"
    
    @property
    def savings(self):
        return self.original_price - self.discount_price

class PrintOrderAccessory(models.Model):
    """Accessories selected for a print order"""
    order = models.ForeignKey(PrintOrder, on_delete=models.CASCADE, related_name='accessories')
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['order', 'accessory']
    
    def __str__(self):
        return f"{self.order.id} - {self.accessory.name} (x{self.quantity})"
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.accessory.base_price * self.quantity
        super().save(*args, **kwargs)