from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count, Min, Max
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from .models import (
    Category, Brand, Product, ProductImage, ProductAttribute, ProductReview,
    Cart, CartItem, Order, OrderItem, Wishlist, Coupon, Banner, PaymentReceipt
)
from print_service.models import PaymentSettings
import json

def shop_home(request):
    """Main shop homepage with featured products and categories"""
    # Get featured categories
    featured_categories = Category.objects.filter(
        is_active=True, is_featured=True
    ).order_by('sort_order')[:6]
    
    # Get featured products
    featured_products = Product.objects.filter(
        is_active=True, is_featured=True
    ).order_by('-created_at')[:8]
    
    # Get new products
    new_products = Product.objects.filter(
        is_active=True, is_new=True
    ).order_by('-created_at')[:8]
    
    # Get best sellers
    best_sellers = Product.objects.filter(
        is_active=True, is_bestseller=True
    ).order_by('-sold_count')[:8]
    
    # Get on-sale products
    on_sale_products = Product.objects.filter(
        is_active=True, is_on_sale=True
    ).order_by('-created_at')[:8]
    
    # Get active banners
    banners = [b for b in Banner.objects.filter(is_active=True) if b.is_current]
    
    # Get brands
    brands = Brand.objects.filter(is_active=True, is_featured=True)[:8]
    
    context = {
        'featured_categories': featured_categories,
        'featured_products': featured_products,
        'new_products': new_products,
        'best_sellers': best_sellers,
        'on_sale_products': on_sale_products,
        'banners': banners,
        'brands': brands,
    }
    
    return render(request, 'digital_shop/home.html', context)

def product_list(request):
    """Product listing page with search and filters"""
    # Get search and filter parameters
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    condition = request.GET.get('condition')
    sort_by = request.GET.get('sort', '-created_at')
    
    # Start with all active products
    products = Product.objects.filter(is_active=True)
    
    # Apply search filter
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(sku__icontains=query)
        )
    
    # Apply category filter
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Apply brand filter
    if brand_id:
        products = products.filter(brand_id=brand_id)
    
    # Apply price filters
    if min_price:
        products = products.filter(price__gte=Decimal(min_price))
    if max_price:
        products = products.filter(price__lte=Decimal(max_price))
    
    # Apply condition filter
    if condition:
        products = products.filter(condition=condition)
    
    # Apply sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'popular':
        products = products.order_by('-view_count')
    elif sort_by == 'bestseller':
        products = products.order_by('-sold_count')
    else:
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    # Get price range
    price_range = products.aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'price_range': price_range,
        'filters': {
            'query': query,
            'category_id': category_id,
            'brand_id': brand_id,
            'min_price': min_price,
            'max_price': max_price,
            'condition': condition,
            'sort_by': sort_by,
        }
    }
    
    return render(request, 'digital_shop/product_list.html', context)

def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Increment view count
    product.increment_view_count()
    
    # Get product images
    images = product.images.order_by('sort_order')
    
    # Get product attributes
    attributes = product.attributes.order_by('sort_order')
    
    # Get reviews
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Check if user has this in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    # Get user's cart
    cart = None
    cart_item = None
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = cart.items.filter(product=product).first()
    
    context = {
        'product': product,
        'images': images,
        'attributes': attributes,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
        'cart': cart,
        'cart_item': cart_item,
    }
    
    return render(request, 'digital_shop/product_detail.html', context)

def category_detail(request, slug):
    """Category detail page"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Get products in this category
    products = Product.objects.filter(
        category=category,
        is_active=True
    ).order_by('-created_at')
    
    # Get subcategories
    subcategories = category.children.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'subcategories': subcategories,
    }
    
    return render(request, 'digital_shop/category_detail.html', context)

def brand_detail(request, slug):
    """Brand detail page"""
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    
    # Get products from this brand
    products = Product.objects.filter(
        brand=brand,
        is_active=True
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'brand': brand,
        'page_obj': page_obj,
    }
    
    return render(request, 'digital_shop/brand_detail.html', context)

@login_required
def cart_view(request):
    """Shopping cart view"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle quantity updates
        for item in cart.items.all():
            quantity_key = f'quantity_{item.id}'
            if quantity_key in request.POST:
                try:
                    quantity = int(request.POST[quantity_key])
                    if quantity > 0:
                        item.quantity = quantity
                        item.save()
                    else:
                        item.delete()
                except ValueError:
                    pass
        
        # Handle remove items
        remove_item = request.POST.get('remove_item')
        if remove_item:
            try:
                item = cart.items.get(id=remove_item)
                item.delete()
                messages.success(request, _('Item removed from cart.'))
            except CartItem.DoesNotExist:
                pass
        
        return redirect('digital_shop:cart')
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
    }
    
    return render(request, 'digital_shop/cart.html', context)

@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        messages.error(request, _('Quantity must be greater than 0.'))
        return redirect('digital_shop:product_detail', slug=product.slug)
    
    if quantity > product.stock_quantity:
        messages.error(request, _('Not enough stock available.'))
        return redirect('digital_shop:product_detail', slug=product.slug)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, _('Product added to cart successfully!'))
    return redirect('digital_shop:cart')

@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, _('Item removed from cart.'))
    except CartItem.DoesNotExist:
        messages.error(request, _('Item not found.'))
    
    return redirect('digital_shop:cart')

@login_required
def checkout(request):
    """Checkout process"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if not cart.items.exists():
        messages.error(request, _('Your cart is empty.'))
        return redirect('digital_shop:cart')
    
    if request.method == 'POST':
        # Process checkout
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_postal_code = request.POST.get('shipping_postal_code')
        customer_notes = request.POST.get('customer_notes', '')
        
        # Calculate totals
        subtotal = cart.total_price
        shipping_cost = Decimal('0.00')  # You can implement shipping calculation
        tax_amount = Decimal('0.00')  # You can implement tax calculation
        discount_amount = Decimal('0.00')  # You can implement coupon system
        total_amount = subtotal + shipping_cost + tax_amount - discount_amount
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_postal_code=shipping_postal_code,
            customer_notes=customer_notes,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            total_amount=total_amount,
            status='pending_payment',
            payment_status='pending',
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
                total_price=cart_item.total_price,
            )
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, _('Order placed successfully! Please complete your payment.'))
        return redirect('digital_shop:payment_page', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
    }
    
    return render(request, 'digital_shop/checkout.html', context)

@login_required
def order_detail(request, order_number):
    """Order detail page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'digital_shop/order_detail.html', context)

@login_required
def my_orders(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'digital_shop/my_orders.html', context)

@login_required
@require_POST
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, _('Product added to wishlist!'))
    else:
        messages.info(request, _('Product is already in your wishlist.'))
    
    return redirect('digital_shop:product_detail', slug=product.slug)

@login_required
@require_POST
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    try:
        wishlist_item = Wishlist.objects.get(
            user=request.user,
            product_id=product_id
        )
        wishlist_item.delete()
        messages.success(request, _('Product removed from wishlist.'))
    except Wishlist.DoesNotExist:
        messages.error(request, _('Product not found in wishlist.'))
    
    return redirect('digital_shop:wishlist')

@login_required
def wishlist(request):
    """User's wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-added_at')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    
    return render(request, 'digital_shop/wishlist.html', context)

@login_required
@require_POST
def submit_review(request, product_id):
    """Submit product review"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    rating = int(request.POST.get('rating', 5))
    title = request.POST.get('title', '')
    comment = request.POST.get('comment', '')
    
    # Check if user already reviewed this product
    existing_review = ProductReview.objects.filter(
        user=request.user,
        product=product
    ).first()
    
    if existing_review:
        existing_review.rating = rating
        existing_review.title = title
        existing_review.comment = comment
        existing_review.save()
        messages.success(request, _('Your review has been updated!'))
    else:
        ProductReview.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            title=title,
            comment=comment,
        )
        messages.success(request, _('Thank you for your review!'))
    
    return redirect('digital_shop:product_detail', slug=product.slug)

@csrf_exempt
def search_products(request):
    """AJAX product search"""
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        )[:10]
        
        results = []
        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'image': product.images.filter(is_primary=True).first().image.url if product.images.filter(is_primary=True).exists() else '',
                'url': reverse('digital_shop:product_detail', args=[product.slug])
            })
        
        return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})

@login_required
@csrf_exempt
def update_cart_item(request, item_id):
    """Update cart item quantity via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            
            if quantity <= 0:
                return JsonResponse({'success': False, 'error': 'تعداد باید بیشتر از 0 باشد'})
            
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
            
            return JsonResponse({'success': True})
            
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'آیتم یافت نشد'})
        except (ValueError, KeyError):
            return JsonResponse({'success': False, 'error': 'داده‌های نامعتبر'})
    
    return JsonResponse({'success': False, 'error': 'متد نامعتبر'})

@login_required
@csrf_exempt
def remove_cart_item(request, item_id):
    """Remove cart item via AJAX"""
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return JsonResponse({'success': True})
            
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'آیتم یافت نشد'})
    
    return JsonResponse({'success': False, 'error': 'متد نامعتبر'})

@login_required
@csrf_exempt
def apply_coupon(request):
    """Apply coupon code via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            coupon_code = data.get('coupon_code', '').strip()
            
            if not coupon_code:
                return JsonResponse({'success': False, 'error': 'کد تخفیف را وارد کنید'})
            
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                
                if not coupon.is_valid:
                    return JsonResponse({'success': False, 'error': 'کد تخفیف منقضی شده است'})
                
                cart, created = Cart.objects.get_or_create(user=request.user)
                
                if cart.total_price < coupon.minimum_order_amount:
                    return JsonResponse({
                        'success': False, 
                        'error': f'حداقل مبلغ سفارش برای این کد تخفیف {coupon.minimum_order_amount} تومان است'
                    })
                
                # Apply coupon logic here
                # For now, just return success
                return JsonResponse({
                    'success': True, 
                    'message': f'کد تخفیف {coupon.description} اعمال شد'
                })
                
            except Coupon.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'کد تخفیف نامعتبر است'})
                
        except (ValueError, KeyError):
            return JsonResponse({'success': False, 'error': 'داده‌های نامعتبر'})
    
    return JsonResponse({'success': False, 'error': 'متد نامعتبر'})

def about_us(request):
    """About us page"""
    return render(request, 'digital_shop/about.html')

def contact_us(request):
    """Contact us page"""
    return render(request, 'digital_shop/contact.html')

def terms_conditions(request):
    """Terms and conditions page"""
    return render(request, 'digital_shop/terms.html')

def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'digital_shop/privacy.html')

@login_required
def payment_page(request, order_id):
    """Payment page for manual payment (Nobitex-style)"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order is in pending payment status
    if order.status != 'pending_payment':
        messages.error(request, 'این سفارش در وضعیت پرداخت نیست.')
        return redirect('digital_shop:order_detail', order_id=order.id)
    
    # Get payment settings
    payment_settings = PaymentSettings.objects.filter(is_active=True).first()
    if not payment_settings:
        messages.error(request, 'تنظیمات پرداخت در دسترس نیست.')
        return redirect('digital_shop:order_detail', order_id=order.id)
    
    # Calculate order expiry date
    from datetime import timedelta
    order_expiry = order.created_at + timedelta(hours=payment_settings.order_validity_hours)
    
    if request.method == 'POST':
        # Handle receipt upload
        try:
            receipt = PaymentReceipt.objects.create(
                order=order,
                receipt_image=request.FILES['receipt_image'],
                transaction_id=request.POST.get('transaction_id', ''),
                depositor_name=request.POST.get('depositor_name', ''),
                amount_paid=request.POST.get('amount_paid'),
                status='pending'
            )
            
            # Set deposit date if provided
            if request.POST.get('deposit_date'):
                receipt.deposit_date = request.POST.get('deposit_date')
                receipt.save()
            
            # Update order status
            order.status = 'pending_payment'
            order.payment_status = 'pending'
            order.save()
            
            messages.success(request, 'رسید پرداخت با موفقیت ارسال شد. تیم پشتیبانی در کمتر از 24 ساعت آن را بررسی خواهد کرد.')
            return redirect('digital_shop:order_detail', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f'خطا در ارسال رسید: {str(e)}')
    
    context = {
        'order': order,
        'payment_settings': payment_settings,
        'order_expiry': order_expiry,
    }
    
    return render(request, 'digital_shop/payment_page.html', context)

@login_required
def order_detail(request, order_id):
    """Order detail page with payment status"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Get payment receipt if exists
    payment_receipt = order.payment_receipts.first()
    
    context = {
        'order': order,
        'payment_receipt': payment_receipt,
    }
    
    return render(request, 'digital_shop/order_detail.html', context)
