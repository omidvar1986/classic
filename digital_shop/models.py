from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class Category(models.Model):
    """Product categories for the digital shop"""
    name = models.CharField(_('Category Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(_('Category Image'), upload_to='categories/', blank=True, null=True)
    icon = models.CharField(_('Icon Class'), max_length=50, default='fas fa-box')
    color = models.CharField(_('Color Class'), max_length=20, default='primary')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    is_active = models.BooleanField(_('Active'), default=True)
    is_featured = models.BooleanField(_('Featured Category'), default=False)
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()

class Brand(models.Model):
    """Product brands"""
    name = models.CharField(_('Brand Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    logo = models.ImageField(_('Brand Logo'), upload_to='brands/', blank=True, null=True)
    website = models.URLField(_('Website'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_featured = models.BooleanField(_('Featured Brand'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Products for sale in the digital shop"""
    CONDITION_CHOICES = [
        ('new', _('New')),
        ('used', _('Used')),
        ('refurbished', _('Refurbished')),
    ]
    
    # Basic information
    name = models.CharField(_('Product Name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = models.TextField(_('Description'))
    short_description = models.CharField(_('Short Description'), max_length=300, blank=True)
    sku = models.CharField(_('SKU'), max_length=50, unique=True)
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    
    # Pricing
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(_('Compare Price'), max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(_('Cost Price'), max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(_('Stock Quantity'), default=0)
    low_stock_threshold = models.PositiveIntegerField(_('Low Stock Threshold'), default=5)
    
    # Product details
    condition = models.CharField(_('Condition'), max_length=15, choices=CONDITION_CHOICES, default='new')
    weight = models.DecimalField(_('Weight (kg)'), max_digits=6, decimal_places=2, blank=True, null=True)
    dimensions = models.CharField(_('Dimensions'), max_length=100, blank=True)
    
    # Status and visibility
    is_active = models.BooleanField(_('Active'), default=True)
    is_featured = models.BooleanField(_('Featured Product'), default=False)
    is_bestseller = models.BooleanField(_('Best Seller'), default=False)
    is_new = models.BooleanField(_('New Product'), default=False)
    is_on_sale = models.BooleanField(_('On Sale'), default=False)
    
    # SEO and marketing
    meta_title = models.CharField(_('Meta Title'), max_length=60, blank=True)
    meta_description = models.CharField(_('Meta Description'), max_length=160, blank=True)
    keywords = models.CharField(_('Keywords'), max_length=500, blank=True)
    
    # Statistics
    view_count = models.PositiveIntegerField(_('View Count'), default=0)
    sold_count = models.PositiveIntegerField(_('Sold Count'), default=0)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return int(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    @property
    def is_low_stock(self):
        return 0 < self.stock_quantity <= self.low_stock_threshold
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

class ProductImage(models.Model):
    """Product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('Image'), upload_to='products/')
    alt_text = models.CharField(_('Alt Text'), max_length=200, blank=True)
    is_primary = models.BooleanField(_('Primary Image'), default=False)
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
        ordering = ['product', 'sort_order']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.sort_order}"

class ProductAttribute(models.Model):
    """Product attributes (specifications)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(_('Attribute Name'), max_length=100)
    value = models.CharField(_('Attribute Value'), max_length=500)
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=0)
    
    class Meta:
        verbose_name = _('Product Attribute')
        verbose_name_plural = _('Product Attributes')
        ordering = ['product', 'sort_order']
        unique_together = ['product', 'name']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"

class ProductReview(models.Model):
    """Customer reviews for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.PositiveIntegerField(_('Rating'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(_('Review Title'), max_length=200, blank=True)
    comment = models.TextField(_('Review Comment'), blank=True)
    is_verified = models.BooleanField(_('Verified Purchase'), default=False)
    is_approved = models.BooleanField(_('Approved'), default=True)
    helpful_votes = models.PositiveIntegerField(_('Helpful Votes'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')
        ordering = ['-created_at']
        unique_together = ['product', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} stars)"

class Cart(models.Model):
    """Shopping cart"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    added_at = models.DateTimeField(_('Added At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    """Customer orders"""
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('pending_payment', _('Pending Payment')),
        ('confirmed', _('Confirmed')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
        ('refunded', _('Refunded')),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('paid', _('Paid')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
    ]
    
    # Order identification
    order_number = models.CharField(_('Order Number'), max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Order status
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(_('Payment Status'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Customer information
    customer_name = models.CharField(_('Customer Name'), max_length=100)
    customer_email = models.EmailField(_('Customer Email'))
    customer_phone = models.CharField(_('Customer Phone'), max_length=20)
    
    # Shipping information
    shipping_address = models.TextField(_('Shipping Address'))
    shipping_city = models.CharField(_('Shipping City'), max_length=100)
    shipping_postal_code = models.CharField(_('Shipping Postal Code'), max_length=10)
    
    # Pricing
    subtotal = models.DecimalField(_('Subtotal'), max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(_('Shipping Cost'), max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(_('Tax Amount'), max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('Discount Amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('Total Amount'), max_digits=10, decimal_places=2)
    
    # Notes
    customer_notes = models.TextField(_('Customer Notes'), blank=True)
    admin_notes = models.TextField(_('Admin Notes'), blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    paid_at = models.DateTimeField(_('Paid At'), blank=True, null=True)
    shipped_at = models.DateTimeField(_('Shipped At'), blank=True, null=True)
    delivered_at = models.DateTimeField(_('Delivered At'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(_('Product Name'), max_length=200)  # Snapshot of product name
    product_sku = models.CharField(_('Product SKU'), max_length=50)  # Snapshot of product SKU
    quantity = models.PositiveIntegerField(_('Quantity'))
    unit_price = models.DecimalField(_('Unit Price'), max_digits=10, decimal_places=2)
    total_price = models.DecimalField(_('Total Price'), max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
    
    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

class Wishlist(models.Model):
    """Customer wishlist"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(_('Added At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Wishlist Item')
        verbose_name_plural = _('Wishlist Items')
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Coupon(models.Model):
    """Discount coupons"""
    TYPE_CHOICES = [
        ('percentage', _('Percentage')),
        ('fixed', _('Fixed Amount')),
    ]
    
    code = models.CharField(_('Coupon Code'), max_length=20, unique=True)
    description = models.CharField(_('Description'), max_length=200)
    discount_type = models.CharField(_('Discount Type'), max_length=15, choices=TYPE_CHOICES)
    discount_value = models.DecimalField(_('Discount Value'), max_digits=10, decimal_places=2)
    minimum_order_amount = models.DecimalField(_('Minimum Order Amount'), max_digits=10, decimal_places=2, default=0)
    maximum_discount = models.DecimalField(_('Maximum Discount'), max_digits=10, decimal_places=2, blank=True, null=True)
    usage_limit = models.PositiveIntegerField(_('Usage Limit'), blank=True, null=True)
    used_count = models.PositiveIntegerField(_('Used Count'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)
    valid_from = models.DateTimeField(_('Valid From'))
    valid_until = models.DateTimeField(_('Valid Until'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.code
    
    @property
    def is_valid(self):
        now = timezone.now()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_until and
                (self.usage_limit is None or self.used_count < self.usage_limit))
    
    def can_be_used_by(self, user):
        """Check if user can use this coupon"""
        if not self.is_valid:
            return False
        # Check if user has already used this coupon
        return not Order.objects.filter(user=user, coupon=self).exists()

class Banner(models.Model):
    """Promotional banners"""
    POSITION_CHOICES = [
        ('homepage', _('Homepage')),
        ('category', _('Category Page')),
        ('product', _('Product Page')),
    ]
    
    title = models.CharField(_('Title'), max_length=200)
    subtitle = models.CharField(_('Subtitle'), max_length=200, blank=True)
    image = models.ImageField(_('Banner Image'), upload_to='banners/')
    link_url = models.URLField(_('Link URL'), blank=True)
    position = models.CharField(_('Position'), max_length=20, choices=POSITION_CHOICES, default='homepage')
    is_active = models.BooleanField(_('Active'), default=True)
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=0)
    start_date = models.DateTimeField(_('Start Date'), default=timezone.now)
    end_date = models.DateTimeField(_('End Date'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        ordering = ['position', 'sort_order']
    
    def __str__(self):
        return self.title
    
    @property
    def is_current(self):
        now = timezone.now()
        return (self.is_active and 
                self.start_date <= now and 
                (self.end_date is None or self.end_date >= now))

class PaymentReceipt(models.Model):
    """Payment receipt for manual payments (Nobitex-style)"""
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payment_receipts')
    receipt_image = models.ImageField(upload_to='payment_receipts/', verbose_name="تصویر رسید")
    transaction_id = models.CharField(max_length=100, verbose_name="شماره تراکنش", blank=True, null=True)
    depositor_name = models.CharField(max_length=100, verbose_name="نام واریزکننده", blank=True, null=True)
    deposit_date = models.DateTimeField(verbose_name="تاریخ واریز", blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ واریز شده")
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار بررسی'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    
    admin_note = models.TextField(verbose_name="یادداشت ادمین", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "رسید پرداخت"
        verbose_name_plural = "رسیدهای پرداخت"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"رسید سفارش {self.order.id} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        # Auto-approve payment if receipt is approved
        if self.status == 'approved' and self.order.status == 'pending_payment':
            self.order.status = 'paid'
            self.order.save()
        super().save(*args, **kwargs)
