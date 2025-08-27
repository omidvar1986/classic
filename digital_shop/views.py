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

# API Endpoints for React Frontend
@csrf_exempt
def api_products(request):
    """API endpoint to get products list"""
    if request.method == 'GET':
        try:
            # Get all active products
            products = Product.objects.filter(is_active=True).order_by('-created_at')
            
            products_data = []
            for product in products:
                # Get first image
                first_image = product.images.first()
                
                product_data = {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description or product.short_description or '',
                    'price': float(product.price),
                    'compare_price': float(product.compare_price) if product.compare_price else None,
                    'category': {
                        'id': product.category.id,
                        'name': product.category.name,
                    } if product.category else None,
                    'brand': {
                        'id': product.brand.id,
                        'name': product.brand.name,
                    } if product.brand else None,
                    'images': [{
                        'id': img.id,
                        'image': img.image.url if img.image else '',
                    } for img in product.images.all()],
                    'in_stock': product.stock_quantity > 0,
                    'stock_quantity': product.stock_quantity,
                    'sku': product.sku,
                    'is_featured': product.is_featured,
                    'is_new': product.is_new,
                    'is_on_sale': product.is_on_sale,
                    'is_active': product.is_active,  # Add this missing field
                }
                products_data.append(product_data)
            
            return JsonResponse({
                'success': True,
                'products': products_data,
                'count': len(products_data)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در دریافت محصولات: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def api_product_detail(request, product_id):
    """API endpoint to get product details"""
    if request.method == 'GET':
        try:
            product = get_object_or_404(Product, id=product_id, is_active=True)
            
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description or '',
                'short_description': product.short_description or '',
                'price': float(product.price),
                'compare_price': float(product.compare_price) if product.compare_price else None,
                'category': {
                    'id': product.category.id,
                    'name': product.category.name,
                } if product.category else None,
                'brand': {
                    'id': product.brand.id,
                    'name': product.brand.name,
                } if product.brand else None,
                'images': [{
                    'id': img.id,
                    'image': img.image.url if img.image else '',
                } for img in product.images.all()],
                'attributes': [{
                    'name': attr.name,
                    'value': attr.value,
                } for attr in product.attributes.all()],
                'in_stock': product.stock_quantity > 0,
                'stock_quantity': product.stock_quantity,
                'sku': product.sku,
                'view_count': product.view_count,
                'sold_count': product.sold_count,
            }
            
            return JsonResponse({
                'success': True,
                'product': product_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در دریافت جزئیات محصول: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def api_cart(request):
    """API endpoint to get user's cart"""
    if request.method == 'GET':
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            cart_items = []
            for item in cart.items.all():
                first_image = item.product.images.first()
                
                item_data = {
                    'id': item.id,
                    'product': {
                        'id': item.product.id,
                        'name': item.product.name,
                        'price': float(item.product.price),
                        'image': first_image.image.url if first_image and first_image.image else '',
                    },
                    'quantity': item.quantity,
                    'total_price': float(item.total_price),
                }
                cart_items.append(item_data)
            
            return JsonResponse({
                'success': True,
                'cart': {
                    'items': cart_items,
                    'total_items': cart.total_items,
                    'total_price': float(cart.total_price),
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در دریافت سبد خرید: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def api_add_to_cart(request):
    """API endpoint to add product to cart"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            if not product_id:
                return JsonResponse({
                    'success': False,
                    'message': 'شناسه محصول الزامی است'
                }, status=400)
            
            product = get_object_or_404(Product, id=product_id, is_active=True)
            
            if quantity <= 0:
                return JsonResponse({
                    'success': False,
                    'message': 'تعداد باید بیشتر از صفر باشد'
                }, status=400)
            
            if product.stock_quantity < quantity:
                return JsonResponse({
                    'success': False,
                    'message': 'موجودی کافی نیست'
                }, status=400)
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock_quantity:
                    return JsonResponse({
                        'success': False,
                        'message': 'موجودی کافی نیست'
                    }, status=400)
                cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'محصول به سبد خرید اضافه شد',
                'cart_total_items': cart.total_items
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'داده‌های ارسالی نامعتبر است'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در افزودن به سبد خرید: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def api_update_cart_item(request, item_id):
    """API endpoint to update cart item quantity"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            
            if quantity <= 0:
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'message': 'محصول از سبد خرید حذف شد'
                })
            
            if quantity > cart_item.product.stock_quantity:
                return JsonResponse({
                    'success': False,
                    'message': 'موجودی کافی نیست'
                }, status=400)
            
            cart_item.quantity = quantity
            cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'سبد خرید به‌روزرسانی شد'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'داده‌های ارسالی نامعتبر است'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در به‌روزرسانی سبد خرید: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def api_remove_cart_item(request, item_id):
    """API endpoint to remove item from cart"""
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'محصول از سبد خرید حذف شد'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در حذف از سبد خرید: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def api_checkout(request):
    """API endpoint for checkout process"""
    if request.method == 'POST':
        try:
            cart = get_object_or_404(Cart, user=request.user)
            
            if not cart.items.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'سبد خرید خالی است'
                }, status=400)
            
            data = json.loads(request.body)
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                email=request.user.email,
                phone=data.get('phone', ''),
                address=data.get('address', ''),
                notes=data.get('notes', ''),
                total_amount=cart.total_price,
                status='pending_payment'
            )
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    total_price=cart_item.total_price
                )
            
            # Clear cart
            cart.items.all().delete()
            
            return JsonResponse({
                'success': True,
                'message': 'سفارش با موفقیت ثبت شد',
                'order_id': order.id,
                'order_number': order.order_number
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'داده‌های ارسالی نامعتبر است'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در ثبت سفارش: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@login_required
def api_my_orders(request):
    """API endpoint to get user's orders"""
    if request.method == 'GET':
        try:
            # Get user's orders
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
            
            orders_data = []
            for order in orders:
                order_data = {
                    'id': order.id,
                    'order_number': order.order_number,
                    'status': order.status,
                    'payment_status': order.payment_status,
                    'total_amount': float(order.total_amount),
                    'created_at': order.created_at.isoformat(),
                    'customer_name': order.customer_name,
                    'customer_phone': order.customer_phone,
                    'customer_address': order.customer_address,
                    'customer_notes': order.customer_notes or '',
                    'items': []
                }
                
                # Get order items
                for item in order.items.all():
                    item_data = {
                        'id': item.id,
                        'product': {
                            'id': item.product.id,
                            'name': item.product.name,
                            'price': float(item.product.price),
                            'image': item.product.images.first().image.url if item.product.images.first() else None,
                        },
                        'quantity': item.quantity,
                        'total_price': float(item.total_price),
                    }
                    order_data['items'].append(item_data)
                
                orders_data.append(order_data)
            
            return JsonResponse({
                'success': True,
                'orders': orders_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در دریافت سفارشات: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

# New APIs to integrate Next.js checkout and payment upload directly with Django
@login_required
@csrf_exempt
def api_create_order(request):
    """Create an order directly from JSON payload (frontend cart), bypassing server Cart.
    Expected JSON:
    {
      "items": [{"product_id": 1, "quantity": 2}, ...],
      "customer_name": "...",
      "customer_phone": "...",
      "customer_address": "...",
      "customer_notes": "..."
    }
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        if not isinstance(items, list) or len(items) == 0:
            return JsonResponse({'success': False, 'message': 'هیچ آیتمی ارسال نشده است'}, status=400)

        # Calculate totals and validate items
        subtotal = Decimal('0.00')
        order_items_payload = []
        for row in items:
            product_id = int(row.get('product_id'))
            quantity = int(row.get('quantity', 1))
            if quantity <= 0:
                return JsonResponse({'success': False, 'message': 'تعداد نامعتبر است'}, status=400)
            product = get_object_or_404(Product, id=product_id, is_active=True)
            if product.stock_quantity < quantity:
                return JsonResponse({'success': False, 'message': f'موجودی کافی برای {product.name} نیست'}, status=400)
            line_total = Decimal(str(product.price)) * quantity
            subtotal += line_total
            order_items_payload.append((product, quantity, Decimal(str(product.price)), line_total))

        shipping_cost = Decimal('0.00')
        tax_amount = Decimal('0.00')
        discount_amount = Decimal('0.00')
        total_amount = subtotal + shipping_cost + tax_amount - discount_amount

        order = Order.objects.create(
            user=request.user,
            customer_name=data.get('customer_name', ''),
            customer_email=request.user.email,
            customer_phone=data.get('customer_phone', ''),
            shipping_address=data.get('customer_address', ''),
            shipping_city='',
            shipping_postal_code='',
            customer_notes=data.get('customer_notes', ''),
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            total_amount=total_amount,
            status='pending_payment',
            payment_status='pending',
        )

        for product, quantity, unit_price, line_total in order_items_payload:
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_sku=product.sku,
                quantity=quantity,
                unit_price=unit_price,
                total_price=line_total,
            )

        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'order_number': order.order_number,
            'total_amount': float(order.total_amount),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'خطا در ایجاد سفارش: {str(e)}'}, status=500)


@login_required
@csrf_exempt
def api_upload_payment_receipt(request, order_id: int):
    """Upload a payment receipt file for an order. Multipart form expected with:
    - receipt_image (file, required)
    - amount_paid (number, optional)
    - transaction_id, depositor_name, payment_notes (optional)
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if 'receipt_image' not in request.FILES:
            return JsonResponse({'success': False, 'message': 'فایل رسید الزامی است'}, status=400)

        amount_paid_val = request.POST.get('amount_paid')
        try:
            amount_paid = Decimal(str(amount_paid_val)) if amount_paid_val else order.total_amount
        except Exception:
            amount_paid = order.total_amount

        receipt = PaymentReceipt.objects.create(
            order=order,
            receipt_image=request.FILES['receipt_image'],
            transaction_id=request.POST.get('transaction_id', ''),
            depositor_name=request.POST.get('depositor_name', ''),
            amount_paid=amount_paid,
            status='pending'
        )

        # Keep order in pending state for admin approval
        order.status = 'pending_payment'
        order.payment_status = 'pending'
        order.save(update_fields=['status', 'payment_status'])

        return JsonResponse({'success': True, 'message': 'رسید با موفقیت ارسال شد', 'receipt_id': receipt.id})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'خطا در ارسال رسید: {str(e)}'}, status=500)

# Admin API endpoints for React admin panel
@csrf_exempt
def api_admin_products(request):
    """Admin API endpoint to get all products for admin panel"""
    if request.method == 'GET':
        try:
            products = Product.objects.all().order_by('-created_at')
            
            products_data = []
            for product in products:
                product_data = {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description or '',
                    'short_description': product.short_description or '',
                    'price': float(product.price),
                    'compare_price': float(product.compare_price) if product.compare_price else None,
                    'stock_quantity': product.stock_quantity,
                    'sku': product.sku,
                    'category': {
                        'id': product.category.id,
                        'name': product.category.name,
                    } if product.category else None,
                    'brand': {
                        'id': product.brand.id,
                        'name': product.brand.name,
                    } if product.brand else None,
                    'images': [{
                        'id': img.id,
                        'image': img.image.url if img.image else '',
                    } for img in product.images.all()],
                    'is_active': product.is_active,
                    'is_featured': product.is_featured,
                    'is_new': product.is_new,
                    'is_on_sale': product.is_on_sale,
                    'condition': product.condition,
                    'created_at': product.created_at.isoformat(),
                }
                products_data.append(product_data)
            
            return JsonResponse({
                'success': True,
                'products': products_data,
                'count': len(products_data)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در دریافت محصولات: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def api_admin_create_product(request):
    """Admin API endpoint to create a new product"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Generate slug from name
            from django.utils.text import slugify
            slug = slugify(data.get('name', ''))
            
            # Ensure slug is unique
            counter = 1
            original_slug = slug
            while Product.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            # Validate category and brand
            category_id = data.get('category_id')
            brand_id = data.get('brand_id')

            if not category_id or not Category.objects.filter(id=category_id).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'دسته بندی نامعتبر است'
                }, status=400)

            if brand_id and not Brand.objects.filter(id=brand_id).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'برند نامعتبر است'
                }, status=400)

            # Create product
            product = Product.objects.create(
                name=data.get('name'),
                slug=slug,
                description=data.get('description', ''),
                short_description=data.get('short_description', ''),
                sku=data.get('sku', ''),
                price=data.get('price', 0),
                compare_price=data.get('compare_price'),
                stock_quantity=data.get('stock_quantity', 0),
                condition=data.get('condition', 'new'),
                category_id=category_id,
                brand_id=brand_id if brand_id else None,
                is_active=data.get('is_active', True),
                is_featured=data.get('is_featured', False),
                is_new=data.get('is_new', True),
                is_on_sale=data.get('is_on_sale', False),
            )
            
            # Handle images (if provided as base64 or URLs)
            if data.get('images'):
                for i, image_data in enumerate(data['images']):
                    # For now, we'll skip image handling as it requires file upload
                    # In a real implementation, you'd handle file uploads here
                    pass
            
            return JsonResponse({
                'success': True,
                'message': 'محصول با موفقیت ایجاد شد',
                'product_id': product.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در ایجاد محصول: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def api_admin_update_product(request, product_id):
    """Admin API endpoint to update a product"""
    if request.method == 'PUT':
        try:
            product = get_object_or_404(Product, id=product_id)
            data = json.loads(request.body)
            
            # Update product fields
            if 'name' in data:
                product.name = data['name']
                # Regenerate slug if name changed
                from django.utils.text import slugify
                slug = slugify(data['name'])
                counter = 1
                original_slug = slug
                while Product.objects.filter(slug=slug).exclude(id=product_id).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                product.slug = slug
            
            if 'description' in data:
                product.description = data['description']
            if 'short_description' in data:
                product.short_description = data['short_description']
            if 'price' in data:
                product.price = data['price']
            if 'compare_price' in data:
                product.compare_price = data['compare_price']
            if 'stock_quantity' in data:
                product.stock_quantity = data['stock_quantity']
            if 'category_id' in data:
                product.category_id = data['category_id']
            if 'brand_id' in data:
                product.brand_id = data['brand_id'] if data['brand_id'] else None
            if 'is_active' in data:
                product.is_active = data['is_active']
            if 'is_featured' in data:
                product.is_featured = data['is_featured']
            if 'is_new' in data:
                product.is_new = data['is_new']
            if 'is_on_sale' in data:
                product.is_on_sale = data['is_on_sale']
            if 'condition' in data:
                product.condition = data['condition']
            
            product.save()
            
            return JsonResponse({
                'success': True,
                'message': 'محصول با موفقیت به‌روزرسانی شد'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در به‌روزرسانی محصول: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def api_admin_delete_product(request, product_id):
    """Admin API endpoint to delete a product"""
    if request.method == 'DELETE':
        try:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'محصول با موفقیت حذف شد'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در حذف محصول: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
