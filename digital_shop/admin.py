from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Count, Avg
from django.utils.safestring import mark_safe

from .models import (
    Category, Brand, Product, ProductImage, ProductAttribute, ProductReview,
    Cart, CartItem, Order, OrderItem, Wishlist, Coupon, Banner
)

class ProductImageInline(admin.TabularInline):
    """Inline admin for product images"""
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'sort_order']
    readonly_fields = ['created_at']

class ProductAttributeInline(admin.TabularInline):
    """Inline admin for product attributes"""
    model = ProductAttribute
    extra = 1
    fields = ['name', 'value', 'sort_order']

class ProductReviewInline(admin.TabularInline):
    """Inline admin for product reviews"""
    model = ProductReview
    extra = 0
    readonly_fields = ['user', 'rating', 'title', 'comment', 'created_at']
    fields = ['user', 'rating', 'title', 'comment', 'is_verified', 'is_approved', 'helpful_votes']
    can_delete = False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'product_count', 'is_active', 'is_featured', 'sort_order']
    list_filter = ['is_active', 'is_featured', 'parent']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_featured', 'sort_order']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        (_('Visual Elements'), {
            'fields': ('image', 'icon', 'color')
        }),
        (_('Status and Visibility'), {
            'fields': ('is_active', 'is_featured', 'sort_order')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'is_active', 'is_featured', 'product_count']
    list_filter = ['is_active', 'is_featured']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = _('Products')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'brand', 'price', 'stock_quantity', 
        'is_active', 'is_featured', 'view_count', 'sold_count'
    ]
    list_filter = [
        'category', 'brand', 'condition', 'is_active', 'is_featured', 
        'is_bestseller', 'is_new', 'is_on_sale', 'created_at'
    ]
    search_fields = ['name', 'sku', 'description', 'category__name', 'brand__name']
    list_editable = ['price', 'stock_quantity', 'is_active', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['view_count', 'sold_count', 'created_at', 'updated_at']
    
    inlines = [ProductImageInline, ProductAttributeInline, ProductReviewInline]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'sku', 'description', 'short_description')
        }),
        (_('Categorization'), {
            'fields': ('category', 'brand')
        }),
        (_('Pricing'), {
            'fields': ('price', 'compare_price', 'cost_price')
        }),
        (_('Inventory'), {
            'fields': ('stock_quantity', 'low_stock_threshold')
        }),
        (_('Product Details'), {
            'fields': ('condition', 'weight', 'dimensions')
        }),
        (_('Status and Visibility'), {
            'fields': ('is_active', 'is_featured', 'is_bestseller', 'is_new', 'is_on_sale')
        }),
        (_('SEO and Marketing'), {
            'fields': ('meta_title', 'meta_description', 'keywords'),
            'classes': ('collapse',)
        }),
        (_('Statistics'), {
            'fields': ('view_count', 'sold_count'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_featured', 'mark_bestseller', 'mark_new', 'mark_on_sale', 'activate_products', 'deactivate_products']
    
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, _('Selected products marked as featured.'))
    mark_featured.short_description = _('Mark as featured')
    
    def mark_bestseller(self, request, queryset):
        queryset.update(is_bestseller=True)
        self.message_user(request, _('Selected products marked as best sellers.'))
    mark_bestseller.short_description = _('Mark as best seller')
    
    def mark_new(self, request, queryset):
        queryset.update(is_new=True)
        self.message_user(request, _('Selected products marked as new.'))
    mark_new.short_description = _('Mark as new')
    
    def mark_on_sale(self, request, queryset):
        queryset.update(is_on_sale=True)
        self.message_user(request, _('Selected products marked as on sale.'))
    mark_on_sale.short_description = _('Mark as on sale')
    
    def activate_products(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _('Selected products activated.'))
    activate_products.short_description = _('Activate products')
    
    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _('Selected products deactivated.'))
    deactivate_products.short_description = _('Deactivate products')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'is_primary', 'sort_order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
    list_editable = ['is_primary', 'sort_order']
    readonly_fields = ['created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return _('No image')
    image_preview.short_description = _('Preview')

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value', 'sort_order']
    list_filter = ['product__category']
    search_fields = ['product__name', 'name', 'value']
    list_editable = ['sort_order']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_verified', 'is_approved', 'helpful_votes', 'created_at']
    list_filter = ['rating', 'is_verified', 'is_approved', 'created_at', 'product__category']
    search_fields = ['product__name', 'user__username', 'title', 'comment']
    list_editable = ['is_verified', 'is_approved']
    readonly_fields = ['created_at']
    
    actions = ['approve_reviews', 'unapprove_reviews', 'verify_reviews', 'unverify_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, _('Selected reviews approved.'))
    approve_reviews.short_description = _('Approve reviews')
    
    def unapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, _('Selected reviews unapproved.'))
    unapprove_reviews.short_description = _('Unapprove reviews')
    
    def verify_reviews(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, _('Selected reviews marked as verified.'))
    verify_reviews.short_description = _('Verify reviews')
    
    def unverify_reviews(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, _('Selected reviews marked as unverified.'))
    unverify_reviews.short_description = _('Unverify reviews')

class CartItemInline(admin.TabularInline):
    """Inline admin for cart items"""
    model = CartItem
    extra = 0
    readonly_fields = ['added_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    """Inline admin for order items"""
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'unit_price', 'total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'customer_name', 'status', 'payment_status', 
        'total_amount', 'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_email', 'user__username']
    readonly_fields = [
        'order_number', 'created_at', 'updated_at', 'paid_at', 'shipped_at', 'delivered_at'
    ]
    inlines = [OrderItemInline]
    
    fieldsets = (
        (_('Order Information'), {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        (_('Customer Information'), {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        (_('Shipping Information'), {
            'fields': ('shipping_address', 'shipping_city', 'shipping_postal_code')
        }),
        (_('Pricing'), {
            'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'discount_amount', 'total_amount')
        }),
        (_('Notes'), {
            'fields': ('customer_notes', 'admin_notes')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at', 'paid_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_confirmed', 'mark_processing', 'mark_shipped', 'mark_delivered', 'mark_cancelled']
    
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, _('Selected orders marked as confirmed.'))
    mark_confirmed.short_description = _('Mark as confirmed')
    
    def mark_processing(self, request, queryset):
        queryset.update(status='processing')
        self.message_user(request, _('Selected orders marked as processing.'))
    mark_processing.short_description = _('Mark as processing')
    
    def mark_shipped(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='shipped', shipped_at=timezone.now())
        self.message_user(request, _('Selected orders marked as shipped.'))
    mark_shipped.short_description = _('Mark as shipped')
    
    def mark_delivered(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='delivered', delivered_at=timezone.now())
        self.message_user(request, _('Selected orders marked as delivered.'))
    mark_delivered.short_description = _('Mark as delivered')
    
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, _('Selected orders marked as cancelled.'))
    mark_cancelled.short_description = _('Mark as cancelled')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'product_name', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['order__order_number', 'product__name', 'product_name']
    readonly_fields = ['order', 'product', 'product_name', 'product_sku', 'quantity', 'unit_price', 'total_price']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at', 'product__category']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['added_at']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'description', 'discount_type', 'discount_value', 
        'is_active', 'is_valid', 'used_count', 'valid_until'
    ]
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'description']
    list_editable = ['is_active']
    readonly_fields = ['used_count', 'created_at']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('code', 'description', 'discount_type', 'discount_value')
        }),
        (_('Usage Limits'), {
            'fields': ('minimum_order_amount', 'maximum_discount', 'usage_limit', 'used_count')
        }),
        (_('Validity'), {
            'fields': ('is_active', 'valid_from', 'valid_until')
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['activate_coupons', 'deactivate_coupons']
    
    def activate_coupons(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _('Selected coupons activated.'))
    activate_coupons.short_description = _('Activate coupons')
    
    def deactivate_coupons(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _('Selected coupons deactivated.'))
    deactivate_coupons.short_description = _('Deactivate coupons')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'is_active', 'is_current', 'sort_order', 'start_date']
    list_filter = ['position', 'is_active', 'start_date', 'end_date']
    search_fields = ['title', 'subtitle']
    list_editable = ['is_active', 'sort_order']
    readonly_fields = ['created_at']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'subtitle', 'image', 'link_url')
        }),
        (_('Display Settings'), {
            'fields': ('position', 'is_active', 'sort_order')
        }),
        (_('Schedule'), {
            'fields': ('start_date', 'end_date')
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

# Custom admin site configuration
admin.site.site_header = _('Digital File Shop Administration')
admin.site.site_title = _('Digital File Shop Admin')
admin.site.index_title = _('Welcome to Digital File Shop Administration')
