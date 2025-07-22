# admin_dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from print_service.models import PrintOrder, PaymentSettings
from typing_service.models import TypingOrder, TypingPriceSettings
from print_service.forms import AdminPaymentReviewForm
from django.db.models import Q
from typing_service.forms import FinalApprovalForm, TypingPriceSettingsForm
from django.utils.translation import gettext_lazy as _

# فقط کاربران staff دسترسی داشته باشند
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

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
    # Get the first settings object, or create one if it doesn't exist
    settings, created = TypingPriceSettings.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        form = TypingPriceSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, _('Pricing settings have been updated successfully.'))
            return redirect('admin_dashboard:settings')
    else:
        form = TypingPriceSettingsForm(instance=settings)

    return render(request, 'admin_dashboard/settings.html', {'form': form})

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