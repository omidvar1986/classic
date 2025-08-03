# admin_dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from print_service.models import PrintOrder, PaymentSettings, PrintPriceSettings, Accessory, PackageDeal
from typing_service.models import TypingOrder, TypingPriceSettings
from government_services.models import DigitalService, DigitalServiceCategory, UserServiceRequest
from digital_shop.models import Category, Brand, Product, ProductImage, ProductAttribute, Order, OrderItem, Coupon, Banner
from print_service.forms import AdminPaymentReviewForm
from django.db.models import Q, Count, F
from typing_service.forms import FinalApprovalForm
from .forms import (
    TypingPriceSettingsForm, PrintPriceSettingsForm, AccessoryForm, 
    PackageDealForm, PaymentSettingsForm, AccessoryBulkEditForm
)
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.contrib.auth.forms import UserChangeForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# فقط کاربران staff یا superuser دسترسی داشته باشند
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff or u.is_superuser)(view_func)

@staff_required
def dashboard_view(request):
    tab = request.GET.get('tab', '')
    status = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()

    print_orders = PrintOrder.objects.filter(payment_slip__isnull=False)
    typing_orders = TypingOrder.objects.filter(payment_slip__isnull=False)

    if status in ['pending', 'approved', 'rejected']:
        print_orders = print_orders.filter(payment_status=status)
        typing_orders = typing_orders.filter(status=status)

    if query:
        print_orders = print_orders.filter(
            Q(id__icontains=query) | Q(name__icontains=query) | Q(email__icontains=query)
        )
        typing_orders = typing_orders.filter(
            Q(id__icontains=query) | Q(user_name__icontains=query) | Q(user_email__icontains=query)
        )

    if tab == 'print':
        orders = list(print_orders)
    elif tab == 'typing':
        orders = list(typing_orders)
    else:
        orders = list(print_orders) + list(typing_orders)

    orders.sort(key=lambda x: x.created_at, reverse=True)

    context = {
        'orders': orders,
        'active_filter': status if status else 'all',
        'active_tab': tab if tab else 'all',
        'query': query,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)

# User Management Views
@staff_required
def user_management_view(request):
    """Main user management dashboard"""
    query = request.GET.get('q', '').strip()
    filter_type = request.GET.get('filter', 'all')
    
    users = User.objects.all()
    
    # Apply search filter
    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
    
    # Apply type filter
    if filter_type == 'staff':
        users = users.filter(is_staff=True)
    elif filter_type == 'superuser':
        users = users.filter(is_superuser=True)
    elif filter_type == 'active':
        users = users.filter(is_active=True)
    elif filter_type == 'inactive':
        users = users.filter(is_active=False)
    
    # Get user statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    superusers = User.objects.filter(is_superuser=True).count()
    
    # Get users with their order counts
    users_with_stats = []
    for user in users:
        print_orders_count = PrintOrder.objects.filter(email=user.email).count()
        typing_orders_count = TypingOrder.objects.filter(user_email=user.email).count()
        total_orders = print_orders_count + typing_orders_count
        
        users_with_stats.append({
            'user': user,
            'print_orders_count': print_orders_count,
            'typing_orders_count': typing_orders_count,
            'total_orders': total_orders,
        })
    
    # Sort by total orders (most active first)
    users_with_stats.sort(key=lambda x: x['total_orders'], reverse=True)
    
    context = {
        'users_with_stats': users_with_stats,
        'query': query,
        'filter_type': filter_type,
        'stats': {
            'total_users': total_users,
            'active_users': active_users,
            'staff_users': staff_users,
            'superusers': superusers,
        }
    }
    return render(request, 'admin_dashboard/user_management.html', context)

@staff_required
def user_detail_view(request, user_id):
    """View detailed information about a specific user"""
    user = get_object_or_404(User, id=user_id)
    
    # Get user's orders
    print_orders = PrintOrder.objects.filter(email=user.email).order_by('-created_at')
    typing_orders = TypingOrder.objects.filter(user_email=user.email).order_by('-created_at')
    
    # Calculate statistics
    total_print_orders = print_orders.count()
    total_typing_orders = typing_orders.count()
    total_spent = sum(order.total_price for order in print_orders if order.total_price) + \
                  sum(order.total_price for order in typing_orders if order.total_price)
    
    context = {
        'user_detail': user,
        'print_orders': print_orders,
        'typing_orders': typing_orders,
        'total_print_orders': total_print_orders,
        'total_typing_orders': total_typing_orders,
        'total_spent': total_spent,
    }
    return render(request, 'admin_dashboard/user_detail.html', context)

@staff_required
def edit_user_view(request, user_id):
    """Edit user information"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} has been updated successfully.')
            return redirect('admin_dashboard:user_management')
    else:
        form = UserChangeForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'admin_dashboard/edit_user.html', context)

@staff_required
@require_POST
def delete_user_view(request, user_id):
    """Delete a user"""
    user = get_object_or_404(User, id=user_id)
    
    # Prevent deleting yourself
    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('admin_dashboard:user_management')
    
    username = user.username
    user.delete()
    messages.success(request, f'User {username} has been deleted successfully.')
    return redirect('admin_dashboard:user_management')

@staff_required
@require_POST
def toggle_user_status_view(request, user_id):
    """Toggle user active status"""
    user = get_object_or_404(User, id=user_id)
    
    # Prevent deactivating yourself
    if user == request.user:
        messages.error(request, 'You cannot deactivate your own account.')
        return redirect('admin_dashboard:user_management')
    
    user.is_active = not user.is_active
    user.save()
    
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User {user.username} has been {status}.')
    return redirect('admin_dashboard:user_management')

@staff_required
@require_POST
def toggle_staff_status_view(request, user_id):
    """Toggle user staff status"""
    user = get_object_or_404(User, id=user_id)
    
    # Prevent removing staff status from yourself
    if user == request.user:
        messages.error(request, 'You cannot remove staff status from your own account.')
        return redirect('admin_dashboard:user_management')
    
    user.is_staff = not user.is_staff
    user.save()
    
    status = 'granted staff privileges' if user.is_staff else 'removed staff privileges'
    messages.success(request, f'User {user.username} has been {status}.')
    return redirect('admin_dashboard:user_management')

@staff_required
def user_statistics_view(request):
    """Display user statistics and analytics"""
    # Basic statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    superusers = User.objects.filter(is_superuser=True).count()
    
    # Users with orders
    users_with_print_orders = User.objects.filter(
        email__in=PrintOrder.objects.values_list('email', flat=True).distinct()
    ).count()
    
    users_with_typing_orders = User.objects.filter(
        email__in=TypingOrder.objects.values_list('user_email', flat=True).distinct()
    ).count()
    
    # Recent activity
    recent_users = User.objects.filter(
        date_joined__gte=timezone.now() - timezone.timedelta(days=30)
    ).count()
    
    # Top users by order count
    top_users = []
    for user in User.objects.all():
        print_count = PrintOrder.objects.filter(email=user.email).count()
        typing_count = TypingOrder.objects.filter(user_email=user.email).count()
        total_orders = print_count + typing_count
        
        if total_orders > 0:
            top_users.append({
                'user': user,
                'total_orders': total_orders,
                'print_orders': print_count,
                'typing_orders': typing_count,
            })
    
    top_users.sort(key=lambda x: x['total_orders'], reverse=True)
    top_users = top_users[:10]  # Top 10 users
    
    context = {
        'stats': {
            'total_users': total_users,
            'active_users': active_users,
            'staff_users': staff_users,
            'superusers': superusers,
            'users_with_print_orders': users_with_print_orders,
            'users_with_typing_orders': users_with_typing_orders,
            'recent_users': recent_users,
        },
        'top_users': top_users,
    }
    return render(request, 'admin_dashboard/user_statistics.html', context)

@staff_required
def approve_payment_view(request, service_type, order_id):
    if service_type == 'print':
        order = get_object_or_404(PrintOrder, id=order_id)
        order.payment_status = 'approved'
        order.is_paid = True
        order.status = 'processing'
        order.save()
        messages.success(request, f"Print Order #{order.id} approved.")
    else:
        order = get_object_or_404(TypingOrder, id=order_id)
        order.status = 'in_progress'
        order.save()
        messages.success(request, f"Typing Order #{order.id} approved and is now In Progress.")
    return redirect('admin_dashboard:dashboard')

@staff_required
def reject_payment_view(request, service_type, order_id):
    if service_type == 'print':
        order = get_object_or_404(PrintOrder, id=order_id)
        order.payment_status = 'rejected'
        order.is_paid = False
        order.save()
        messages.warning(request, f"Print Order #{order.id} rejected.")
    else:
        order = get_object_or_404(TypingOrder, id=order_id)
        order.status = 'rejected'
        order.save()
        messages.warning(request, f"Typing Order #{order.id} rejected.")
    return redirect('admin_dashboard:dashboard')

@staff_required
def delete_order_view(request, service_type, order_id):
    if service_type == 'print':
        order = get_object_or_404(PrintOrder, id=order_id)
        order.delete()
        messages.success(request, f"Print Order #{order_id} deleted.")
    else:
        order = get_object_or_404(TypingOrder, id=order_id)
        order.delete()
        messages.success(request, f"Typing Order #{order_id} deleted.")
    return redirect('admin_dashboard:dashboard')

@staff_required
def review_payment_view(request, service_type, order_id):
    if service_type == 'print':
        order = get_object_or_404(PrintOrder, id=order_id)
        if request.method == 'POST':
            form = AdminPaymentReviewForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(request, f"Payment status updated for Print Order #{order.id}")
                return redirect('admin_dashboard:dashboard')
        else:
            form = AdminPaymentReviewForm(instance=order)
    else: # This is a typing order
        order = get_object_or_404(TypingOrder, id=order_id)
        pricing_settings = TypingPriceSettings.objects.first()
        
        if request.method == 'POST':
            page_count = request.POST.get('page_count')
            if page_count:
                order.page_count = int(page_count)
                # Auto-calculate price if settings exist
                if pricing_settings:
                    order.total_price = order.page_count * pricing_settings.price_per_page
                order.status = 'awaiting_payment'
                order.save()
                messages.success(request, _('Price has been set and the user has been notified.'))
                return redirect('admin_dashboard:dashboard')
        
        form = None # No form needed for typing review, it's handled via POST

    return render(request, 'admin_dashboard/review_order.html', {
        'order': order,
        'form': form,
        'service_type': service_type,
        'pricing_settings': pricing_settings,
    })
    
    
@staff_required
def approve_final_download(request, order_id):
    order = get_object_or_404(TypingOrder, id=order_id)
    order.final_approved = True
    order.save()
    messages.success(request, f"دانلود برای سفارش {order.id} آزاد شد.")
    return redirect('admin_dashboard:dashboard')

@staff_required
def settings_view(request):
    """Main settings dashboard with links to all management sections"""
    # Get statistics for the dashboard
    total_accessories = Accessory.objects.count()
    active_accessories = Accessory.objects.filter(is_active=True).count()
    total_packages = PackageDeal.objects.count()
    active_packages = PackageDeal.objects.filter(is_active=True).count()
    
    # Get current settings
    print_settings = PrintPriceSettings.objects.first()
    typing_settings = TypingPriceSettings.objects.first()
    payment_settings = PaymentSettings.objects.first()
    
    context = {
        'stats': {
            'accessories': {
                'total': total_accessories,
                'active': active_accessories,
            },
            'packages': {
                'total': total_packages,
                'active': active_packages,
            }
        },
        'settings': {
            'print': print_settings,
            'typing': typing_settings,
            'payment': payment_settings,
        }
    }
    
    return render(request, 'admin_dashboard/settings.html', context)

@staff_required
def finalize_order(request, order_id):
    order = get_object_or_404(TypingOrder, id=order_id)
    if request.method == 'POST':
        form = FinalApprovalForm(request.POST, instance=order)
        if form.is_valid():
            order.final_approved = True
            form.save()
            messages.success(request, "Order finalized and note saved.")
            return redirect('admin_dashboard:dashboard')
    else:
        form = FinalApprovalForm(instance=order)
    return render(request, 'admin_dashboard/finalize_order.html', {'order': order, 'form': form})

def direct_admin_access(request):
    """
    Direct access for superusers without going through custom login
    """
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_dashboard:dashboard')
    else:
        messages.error(request, 'You need to be logged in as a staff member or superuser to access this page.')
        return redirect('accounts:login')

# ============================================================================
# SETTINGS MANAGEMENT VIEWS
# ============================================================================

@staff_required
def print_pricing_view(request):
    """Manage print service pricing settings"""
    settings, created = PrintPriceSettings.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        form = PrintPriceSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, _('Print pricing settings updated successfully!'))
            return redirect('admin_dashboard:print_pricing')
    else:
        form = PrintPriceSettingsForm(instance=settings)

    return render(request, 'admin_dashboard/print_pricing.html', {
        'form': form,
        'settings': settings
    })

@staff_required
def typing_pricing_view(request):
    """Manage typing service pricing settings"""
    settings, created = TypingPriceSettings.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        form = TypingPriceSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, _('Typing pricing settings updated successfully!'))
            return redirect('admin_dashboard:typing_pricing')
    else:
        form = TypingPriceSettingsForm(instance=settings)

    return render(request, 'admin_dashboard/typing_pricing.html', {
        'form': form,
        'settings': settings
    })

@staff_required
def payment_settings_view(request):
    """Manage payment settings"""
    settings, created = PaymentSettings.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        form = PaymentSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, _('Payment settings updated successfully!'))
            return redirect('admin_dashboard:payment_settings')
    else:
        form = PaymentSettingsForm(instance=settings)

    return render(request, 'admin_dashboard/payment_settings.html', {
        'form': form,
        'settings': settings
    })

# ============================================================================
# ACCESSORIES MANAGEMENT VIEWS
# ============================================================================

@staff_required
def accessories_view(request):
    """List all accessories with management options"""
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '')
    service_filter = request.GET.get('service', '')
    status_filter = request.GET.get('status', '')
    
    accessories = Accessory.objects.all()
    
    # Apply filters
    if query:
        accessories = accessories.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    if category_filter:
        accessories = accessories.filter(category=category_filter)
    
    if service_filter:
        accessories = accessories.filter(service_type=service_filter)
    
    if status_filter == 'active':
        accessories = accessories.filter(is_active=True)
    elif status_filter == 'inactive':
        accessories = accessories.filter(is_active=False)
    
    # Get statistics
    total_accessories = Accessory.objects.count()
    active_accessories = Accessory.objects.filter(is_active=True).count()
    print_accessories = Accessory.objects.filter(service_type__in=['print', 'both']).count()
    typing_accessories = Accessory.objects.filter(service_type__in=['typing', 'both']).count()
    
    context = {
        'accessories': accessories,
        'query': query,
        'category_filter': category_filter,
        'service_filter': service_filter,
        'status_filter': status_filter,
        'stats': {
            'total': total_accessories,
            'active': active_accessories,
            'print': print_accessories,
            'typing': typing_accessories,
        }
    }
    return render(request, 'admin_dashboard/accessories.html', context)

@staff_required
def add_accessory_view(request):
    """Add a new accessory"""
    if request.method == 'POST':
        form = AccessoryForm(request.POST)
        if form.is_valid():
            accessory = form.save()
            messages.success(request, f'Accessory "{accessory.name}" added successfully!')
            return redirect('admin_dashboard:accessories')
    else:
        form = AccessoryForm()

    return render(request, 'admin_dashboard/accessory_form.html', {
        'form': form,
        'action': 'add'
    })

@staff_required
def edit_accessory_view(request, accessory_id):
    """Edit an existing accessory"""
    accessory = get_object_or_404(Accessory, id=accessory_id)
    
    if request.method == 'POST':
        form = AccessoryForm(request.POST, instance=accessory)
        if form.is_valid():
            form.save()
            messages.success(request, f'Accessory "{accessory.name}" updated successfully!')
            return redirect('admin_dashboard:accessories')
    else:
        form = AccessoryForm(instance=accessory)

    return render(request, 'admin_dashboard/accessory_form.html', {
        'form': form,
        'accessory': accessory,
        'action': 'edit'
    })

@staff_required
@require_POST
def delete_accessory_view(request, accessory_id):
    """Delete an accessory"""
    accessory = get_object_or_404(Accessory, id=accessory_id)
    name = accessory.name
    accessory.delete()
    messages.success(request, f'Accessory "{name}" deleted successfully!')
    return redirect('admin_dashboard:accessories')

@staff_required
def bulk_edit_accessories_view(request):
    """Bulk edit accessories"""
    if request.method == 'POST':
        form = AccessoryBulkEditForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            accessories = form.cleaned_data['accessories']
            
            if action == 'activate':
                accessories.update(is_active=True)
                messages.success(request, f'{accessories.count()} accessories activated!')
            elif action == 'deactivate':
                accessories.update(is_active=False)
                messages.success(request, f'{accessories.count()} accessories deactivated!')
            elif action == 'delete':
                count = accessories.count()
                accessories.delete()
                messages.success(request, f'{count} accessories deleted!')
            
            return redirect('admin_dashboard:accessories')
    else:
        form = AccessoryBulkEditForm()

    return render(request, 'admin_dashboard/bulk_edit_accessories.html', {
        'form': form
    })

# ============================================================================
# PACKAGE DEALS MANAGEMENT VIEWS
# ============================================================================

@staff_required
def packages_view(request):
    """List all package deals"""
    query = request.GET.get('q', '').strip()
    service_filter = request.GET.get('service', '')
    status_filter = request.GET.get('status', '')
    
    packages = PackageDeal.objects.all()
    
    # Apply filters
    if query:
        packages = packages.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    if service_filter:
        packages = packages.filter(service_type=service_filter)
    
    if status_filter == 'active':
        packages = packages.filter(is_active=True)
    elif status_filter == 'inactive':
        packages = packages.filter(is_active=False)
    
    # Get statistics
    total_packages = PackageDeal.objects.count()
    active_packages = PackageDeal.objects.filter(is_active=True).count()
    
    context = {
        'packages': packages,
        'query': query,
        'service_filter': service_filter,
        'status_filter': status_filter,
        'stats': {
            'total': total_packages,
            'active': active_packages,
        }
    }
    return render(request, 'admin_dashboard/packages.html', context)

@staff_required
def add_package_view(request):
    """Add a new package deal"""
    if request.method == 'POST':
        form = PackageDealForm(request.POST)
        if form.is_valid():
            package = form.save()
            messages.success(request, f'Package deal "{package.name}" added successfully!')
            return redirect('admin_dashboard:packages')
    else:
        form = PackageDealForm()

    return render(request, 'admin_dashboard/package_form.html', {
        'form': form,
        'action': 'add'
    })

@staff_required
def edit_package_view(request, package_id):
    """Edit an existing package deal"""
    package = get_object_or_404(PackageDeal, id=package_id)
    
    if request.method == 'POST':
        form = PackageDealForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, f'Package deal "{package.name}" updated successfully!')
            return redirect('admin_dashboard:packages')
    else:
        form = PackageDealForm(instance=package)

    return render(request, 'admin_dashboard/package_form.html', {
        'form': form,
        'package': package,
        'action': 'edit'
    })

@staff_required
@require_POST
def delete_package_view(request, package_id):
    """Delete a package deal"""
    package = get_object_or_404(PackageDeal, id=package_id)
    name = package.name
    package.delete()
    messages.success(request, f'Package deal "{name}" deleted successfully!')
    return redirect('admin_dashboard:packages')

# ============================================================================
# GOVERNMENT SERVICES MANAGEMENT VIEWS
# ============================================================================

@staff_required
def government_services_view(request):
    """Government services overview dashboard"""
    # Get statistics
    total_services = DigitalService.objects.count()
    active_services = DigitalService.objects.filter(status='active').count()
    total_categories = DigitalServiceCategory.objects.count()
    total_requests = UserServiceRequest.objects.count()
    pending_requests = UserServiceRequest.objects.filter(status='pending').count()
    
    # Get recent requests
    recent_requests = UserServiceRequest.objects.select_related('user', 'service').order_by('-created_at')[:5]
    
    # Get popular services
    popular_services = DigitalService.objects.filter(status='active').order_by('-view_count')[:5]
    
    context = {
        'total_services': total_services,
        'active_services': active_services,
        'total_categories': total_categories,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'recent_requests': recent_requests,
        'popular_services': popular_services,
    }
    return render(request, 'admin_dashboard/government_services.html', context)

@staff_required
def government_requests_view(request):
    """List all government service requests"""
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()
    
    requests = UserServiceRequest.objects.select_related('user', 'service').all()
    
    # Apply filters
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    if query:
        requests = requests.filter(
            Q(title__icontains=query) | 
            Q(user__username__icontains=query) | 
            Q(user__email__icontains=query) |
            Q(service__name__icontains=query)
        )
    
    # Get statistics
    total_requests = UserServiceRequest.objects.count()
    pending_requests = UserServiceRequest.objects.filter(status='pending').count()
    completed_requests = UserServiceRequest.objects.filter(status='completed').count()
    
    context = {
        'requests': requests,
        'status_filter': status_filter,
        'query': query,
        'stats': {
            'total': total_requests,
            'pending': pending_requests,
            'completed': completed_requests,
        }
    }
    return render(request, 'admin_dashboard/government_requests.html', context)

@staff_required
def government_request_detail_view(request, request_id):
    """View detailed information about a government service request"""
    service_request = get_object_or_404(UserServiceRequest, id=request_id)
    
    context = {
        'service_request': service_request,
    }
    return render(request, 'admin_dashboard/government_request_detail.html', context)

@staff_required
@require_POST
def update_government_request_view(request, request_id):
    """Update the status of a government service request"""
    service_request = get_object_or_404(UserServiceRequest, id=request_id)
    
    new_status = request.POST.get('status')
    admin_response = request.POST.get('admin_response', '')
    
    if new_status in ['pending', 'in_progress', 'completed', 'failed', 'cancelled']:
        service_request.status = new_status
        service_request.admin_response = admin_response
        service_request.save()
        
        messages.success(request, f'Request status updated to {new_status}')
    else:
        messages.error(request, 'Invalid status')
    
    return redirect('admin_dashboard:government_request_detail', request_id=request_id)

# ============================================================================
# DIGITAL SHOP MANAGEMENT VIEWS
# ============================================================================

@staff_required
def digital_shop_dashboard(request):
    """Digital shop management dashboard"""
    # Get statistics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_categories = Category.objects.count()
    total_brands = Brand.objects.count()
    
    # Get recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Get low stock products
    low_stock_products = Product.objects.filter(
        stock_quantity__lte=F('low_stock_threshold'),
        stock_quantity__gt=0
    )[:5]
    
    # Get top selling products
    top_products = Product.objects.order_by('-sold_count')[:5]
    
    context = {
        'total_products': total_products,
        'active_products': active_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_categories': total_categories,
        'total_brands': total_brands,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'top_products': top_products,
    }
    
    return render(request, 'admin_dashboard/digital_shop_dashboard.html', context)

@staff_required
def digital_shop_products(request):
    """Manage digital shop products"""
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    status = request.GET.get('status')
    
    products = Product.objects.all()
    
    # Apply filters
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(sku__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if brand_id:
        products = products.filter(brand_id=brand_id)
    
    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)
    elif status == 'featured':
        products = products.filter(is_featured=True)
    elif status == 'new':
        products = products.filter(is_new=True)
    elif status == 'on_sale':
        products = products.filter(is_on_sale=True)
    
    # Get filter options
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    context = {
        'products': products.order_by('-created_at'),
        'categories': categories,
        'brands': brands,
        'filters': {
            'query': query,
            'category_id': category_id,
            'brand_id': brand_id,
            'status': status,
        }
    }
    
    return render(request, 'admin_dashboard/digital_shop_products.html', context)

@staff_required
def digital_shop_add_product(request):
    """Add new product"""
    if request.method == 'POST':
        # Handle product creation
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        description = request.POST.get('description')
        short_description = request.POST.get('short_description')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        price = request.POST.get('price')
        compare_price = request.POST.get('compare_price')
        stock_quantity = request.POST.get('stock_quantity')
        condition = request.POST.get('condition', 'new')
        
        # Create product
        product = Product.objects.create(
            name=name,
            sku=sku,
            description=description,
            short_description=short_description,
            category_id=category_id,
            brand_id=brand_id if brand_id else None,
            price=price,
            compare_price=compare_price if compare_price else None,
            stock_quantity=stock_quantity,
            condition=condition,
        )
        
        # Handle image uploads
        images = request.FILES.getlist('images')
        for i, image in enumerate(images):
            if image:
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    is_primary=(i == 0),  # First image is primary
                    sort_order=i
                )
        
        # Handle attributes
        attribute_names = request.POST.getlist('attribute_name')
        attribute_values = request.POST.getlist('attribute_value')
        
        for name, value in zip(attribute_names, attribute_values):
            if name and value:
                ProductAttribute.objects.create(
                    product=product,
                    name=name,
                    value=value
                )
        
        messages.success(request, _('Product created successfully!'))
        return redirect('admin_dashboard:digital_shop_products')
    
    # Get form data
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    context = {
        'categories': categories,
        'brands': brands,
    }
    
    return render(request, 'admin_dashboard/digital_shop_add_product.html', context)

@staff_required
def digital_shop_edit_product(request, product_id):
    """Edit product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        # Handle product update
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.description = request.POST.get('description')
        product.short_description = request.POST.get('short_description')
        product.category_id = request.POST.get('category')
        product.brand_id = request.POST.get('brand') if request.POST.get('brand') else None
        product.price = request.POST.get('price')
        product.compare_price = request.POST.get('compare_price') if request.POST.get('compare_price') else None
        product.stock_quantity = request.POST.get('stock_quantity')
        product.condition = request.POST.get('condition', 'new')
        
        # Handle status flags
        product.is_active = 'is_active' in request.POST
        product.is_featured = 'is_featured' in request.POST
        product.is_bestseller = 'is_bestseller' in request.POST
        product.is_new = 'is_new' in request.POST
        product.is_on_sale = 'is_on_sale' in request.POST
        
        product.save()
        
        # Handle new image uploads
        images = request.FILES.getlist('images')
        for i, image in enumerate(images):
            if image:
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    sort_order=product.images.count() + i
                )
        
        # Handle attributes update
        ProductAttribute.objects.filter(product=product).delete()
        attribute_names = request.POST.getlist('attribute_name')
        attribute_values = request.POST.getlist('attribute_value')
        
        for name, value in zip(attribute_names, attribute_values):
            if name and value:
                ProductAttribute.objects.create(
                    product=product,
                    name=name,
                    value=value
                )
        
        messages.success(request, _('Product updated successfully!'))
        return redirect('admin_dashboard:digital_shop_products')
    
    # Get form data
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    context = {
        'product': product,
        'categories': categories,
        'brands': brands,
    }
    
    return render(request, 'admin_dashboard/digital_shop_edit_product.html', context)

@staff_required
@require_POST
def digital_shop_delete_product(request, product_id):
    """Delete product"""
    product = get_object_or_404(Product, id=product_id)
    product_name = product.name
    product.delete()
    messages.success(request, _(f'Product "{product_name}" deleted successfully.'))
    return redirect('admin_dashboard:digital_shop_products')

@staff_required
def digital_shop_categories(request):
    """Manage categories"""
    categories = Category.objects.all().order_by('sort_order')
    
    if request.method == 'POST':
        # Handle category creation/update
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        icon = request.POST.get('icon', 'fas fa-box')
        color = request.POST.get('color', 'primary')
        parent_id = request.POST.get('parent') if request.POST.get('parent') else None
        sort_order = request.POST.get('sort_order', 0)
        is_active = 'is_active' in request.POST
        is_featured = 'is_featured' in request.POST
        
        category_id = request.POST.get('category_id')
        
        if category_id:
            # Update existing category
            category = get_object_or_404(Category, id=category_id)
            category.name = name
            category.slug = slug
            category.description = description
            category.icon = icon
            category.color = color
            category.parent_id = parent_id
            category.sort_order = sort_order
            category.is_active = is_active
            category.is_featured = is_featured
            category.save()
            messages.success(request, _('Category updated successfully!'))
        else:
            # Create new category
            Category.objects.create(
                name=name,
                slug=slug,
                description=description,
                icon=icon,
                color=color,
                parent_id=parent_id,
                sort_order=sort_order,
                is_active=is_active,
                is_featured=is_featured,
            )
            messages.success(request, _('Category created successfully!'))
        
        return redirect('admin_dashboard:digital_shop_categories')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'admin_dashboard/digital_shop_categories.html', context)

@staff_required
def digital_shop_brands(request):
    """Manage brands"""
    brands = Brand.objects.all().order_by('name')
    
    if request.method == 'POST':
        # Handle brand creation/update
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        website = request.POST.get('website')
        is_active = 'is_active' in request.POST
        is_featured = 'is_featured' in request.POST
        
        brand_id = request.POST.get('brand_id')
        
        if brand_id:
            # Update existing brand
            brand = get_object_or_404(Brand, id=brand_id)
            brand.name = name
            brand.slug = slug
            brand.description = description
            brand.website = website
            brand.is_active = is_active
            brand.is_featured = is_featured
            brand.save()
            messages.success(request, _('Brand updated successfully!'))
        else:
            # Create new brand
            Brand.objects.create(
                name=name,
                slug=slug,
                description=description,
                website=website,
                is_active=is_active,
                is_featured=is_featured,
            )
            messages.success(request, _('Brand created successfully!'))
        
        return redirect('admin_dashboard:digital_shop_brands')
    
    context = {
        'brands': brands,
    }
    
    return render(request, 'admin_dashboard/digital_shop_brands.html', context)

@staff_required
def digital_shop_orders(request):
    """Manage orders"""
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status')
    
    orders = Order.objects.all()
    
    if query:
        orders = orders.filter(
            Q(order_number__icontains=query) | 
            Q(customer_name__icontains=query) | 
            Q(customer_email__icontains=query)
        )
    
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders.order_by('-created_at'),
        'filters': {
            'query': query,
            'status': status,
        }
    }
    
    return render(request, 'admin_dashboard/digital_shop_orders.html', context)

@staff_required
def digital_shop_order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Update order status
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '')
        
        if new_status in ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded']:
            order.status = new_status
            order.admin_notes = admin_notes
            order.save()
            messages.success(request, _('Order status updated successfully.'))
        else:
            messages.error(request, _('Invalid status provided.'))
        
        return redirect('admin_dashboard:digital_shop_order_detail', order_id=order_id)
    
    context = {
        'order': order,
    }
    
    return render(request, 'admin_dashboard/digital_shop_order_detail.html', context)

@login_required
def accessories_management(request):
    """Manage accessories for print and typing services"""
    accessories = Accessory.objects.all()
    
    # Apply filters
    category = request.GET.get('category')
    service_type = request.GET.get('service_type')
    status = request.GET.get('status')
    search = request.GET.get('search')
    
    if category:
        accessories = accessories.filter(category=category)
    if service_type:
        accessories = accessories.filter(service_type=service_type)
    if status == 'active':
        accessories = accessories.filter(is_active=True)
    elif status == 'inactive':
        accessories = accessories.filter(is_active=False)
    if search:
        accessories = accessories.filter(name__icontains=search)
    
    # Pagination
    paginator = Paginator(accessories, 12)
    page_number = request.GET.get('page')
    accessories = paginator.get_page(page_number)
    
    context = {
        'accessories': accessories,
    }
    return render(request, 'admin_dashboard/accessories_management.html', context)

@login_required
@require_http_methods(["GET"])
def get_accessory(request, accessory_id):
    """Get accessory data for editing"""
    try:
        accessory = Accessory.objects.get(id=accessory_id)
        data = {
            'id': accessory.id,
            'name': accessory.name,
            'description': accessory.description,
            'base_price': float(accessory.base_price),
            'category': accessory.category,
            'service_type': accessory.service_type,
            'sort_order': accessory.sort_order,
            'is_active': accessory.is_active,
            'is_featured': accessory.is_featured,
            'color': accessory.color,
        }
        return JsonResponse(data)
    except Accessory.DoesNotExist:
        return JsonResponse({'error': 'Accessory not found'}, status=404)

@login_required
@require_http_methods(["POST"])
def save_accessory(request):
    """Save or update accessory"""
    try:
        accessory_id = request.POST.get('accessory_id')
        
        if accessory_id:
            # Update existing accessory
            accessory = Accessory.objects.get(id=accessory_id)
        else:
            # Create new accessory
            accessory = Accessory()
        
        # Update fields
        accessory.name = request.POST.get('name')
        accessory.description = request.POST.get('description', '')
        accessory.base_price = request.POST.get('base_price')
        accessory.category = request.POST.get('category')
        accessory.service_type = request.POST.get('service_type')
        accessory.sort_order = int(request.POST.get('sort_order', 0))
        accessory.is_active = request.POST.get('is_active') == 'on'
        accessory.is_featured = request.POST.get('is_featured') == 'on'
        accessory.color = request.POST.get('color', '#007bff')
        
        # Handle image upload
        if 'image' in request.FILES:
            accessory.image = request.FILES['image']
        
        accessory.save()
        
        return JsonResponse({'success': True, 'message': 'لوازم جانبی با موفقیت ذخیره شد'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def delete_accessory(request, accessory_id):
    """Delete accessory"""
    try:
        accessory = Accessory.objects.get(id=accessory_id)
        accessory.delete()
        return JsonResponse({'success': True, 'message': 'لوازم جانبی با موفقیت حذف شد'})
    except Accessory.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'لوازم جانبی یافت نشد'}, status=404)