from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .forms import PrintOrderForm, UploadedFileForm
from .models import PrintOrder, UploadedFile
from django.urls import reverse
import os
from django.contrib.admin.views.decorators import staff_member_required
from typing_service.models import TypingOrder
from .models import PaymentSettings
from .forms import PaymentSettingsForm

# -------------------------
# سفارش جدید و آپلود فایل
# -------------------------
def order_create(request):
    if request.method == 'POST':
        order_form = PrintOrderForm(request.POST)
        file_form = UploadedFileForm(request.POST, request.FILES)
        if order_form.is_valid() and file_form.is_valid():
            order = order_form.save()
            uploaded_file = file_form.save(commit=False)
            uploaded_file.order = order
            uploaded_file.save()
            return redirect('print_service:order_submitted', order_id=order.id)
    else:
        order_form = PrintOrderForm()
        file_form = UploadedFileForm()
    return render(request, 'print_service/order_create.html', {
        'order_form': order_form,
        'file_form': file_form,
    })

def order_submitted(request, order_id):
    order = get_object_or_404(PrintOrder, id=order_id)
    return render(request, 'print_service/order_submitted.html', {'order': order})

def order_summary(request):
    order_data = request.session.get('order_data')
    file_names = request.session.get('order_files', [])
    if not order_data:
        return redirect('print_service:order_create')
    if request.method == 'POST':
        # Save order and files to DB
        order = PrintOrder.objects.create(**order_data)
        files_data = request.session.get('order_files_data', [])
        content_types = request.session.get('order_files_content_type', [])
        original_names = request.session.get('order_files_original_names', [])
        for idx, file_content in enumerate(files_data):
            from django.core.files.base import ContentFile
            UploadedFile.objects.create(
                order=order,
                file=ContentFile(file_content, name=original_names[idx])
            )
        # Clean up session
        for key in ['order_data', 'order_files', 'order_files_data', 'order_files_content_type', 'order_files_original_names']:
            if key in request.session:
                del request.session[key]
        messages.success(request, f'Order #{order.id} created successfully!')
        if order.payment_method == 'online':
            return redirect('print_service:payment_slip_upload', order_id=order.id)
        else:
            return redirect('print_service:order_detail', order_id=order.id)
    return render(request, 'print_service/order_summary.html', {
        'order_data': order_data,
        'file_names': file_names,
    })

# -------------------------
# جزئیات و پیگیری سفارش
# -------------------------
def order_detail(request, order_id):
    order = get_object_or_404(PrintOrder, id=order_id)
    return render(request, 'print_service/order_detail.html', {
        'order': order,
        'files': order.files.all(),
    })

def order_track(request):
    order = None
    error = None
    order_id = request.GET.get('order_id')
    email = request.GET.get('email')
    if email:
        email = email.strip().lower()
    if order_id:
        order_id = str(order_id).strip()

    # Find the order
    if order_id and email:
        try:
            order = PrintOrder.objects.get(id=order_id, email__iexact=email)
        except PrintOrder.DoesNotExist:
            error = "No order found with this ID and email."
    elif order_id:
        try:
            order = PrintOrder.objects.get(id=order_id)
        except PrintOrder.DoesNotExist:
            error = "No order found with this ID."
    elif email:
        orders = PrintOrder.objects.filter(email__iexact=email).order_by('-created_at')
        if orders.exists():
            order = orders.first()
            if orders.count() > 1:
                error = f'Found {orders.count()} orders. Showing the most recent one.'
        else:
            error = 'No orders found with this email.'

    # Define progress steps in order
    progress_steps = [
        'pending',
        'awaiting_payment',
        'awaiting_approval',
        'processing',
        'ready',
        'completed',
        'rejected',
        'cancelled',
    ]
    current_step_index = 0
    if order and order.status in progress_steps:
        current_step_index = progress_steps.index(order.status)

    # --- Get bank info ---
    from .models import PaymentSettings
    bank_info = PaymentSettings.objects.first()
    print(f"[DEBUG] Bank info: {bank_info}")
    if bank_info:
        print(f"[DEBUG] Bank name: {bank_info.bank_name}")
    else:
        print("[DEBUG] No bank info found")

    # --- Handle payment slip upload ---
    from .forms import PrintOrderSlipForm
    payment_form = PrintOrderSlipForm(instance=order) if order else PrintOrderSlipForm()
    if request.method == 'POST' and order:
        if 'upload_slip' in request.POST:
            payment_form = PrintOrderSlipForm(request.POST, request.FILES, instance=order)
            if payment_form.is_valid():
                order.status = 'awaiting_approval'
                payment_form.save()
                from django.contrib import messages
                messages.success(request, 'Your payment slip has been uploaded and is awaiting approval.')
                from django.urls import reverse
                return redirect(f"{reverse('print_service:order_track')}?order_id={order.id}&email={order.email}")

    context = {
        'order': order,
        'progress_steps': progress_steps,
        'current_step_index': current_step_index,
        'error': error,
        'payment_form': payment_form,
        'bank_info': bank_info,
        'order_id': order_id or '',
        'email': email or '',
    }
    return render(request, 'print_service/order_track.html', context)

def unified_order_track(request):
    order_id = request.GET.get('order_id')
    email = request.GET.get('email')
    order = None
    order_type = None
    error = None
    if email:
        email = email.strip().lower()
    if order_id:
        order_id = str(order_id).strip()

    # Try to find in PrintOrder
    if order_id and email:
        try:
            order = PrintOrder.objects.get(id=order_id, email__iexact=email)
            order_type = 'print'
        except PrintOrder.DoesNotExist:
            pass
        if not order:
            try:
                order = TypingOrder.objects.get(id=order_id, user_email__iexact=email)
                order_type = 'typing'
            except TypingOrder.DoesNotExist:
                error = "No order found with this ID and email."
    elif order_id:
        try:
            order = PrintOrder.objects.get(id=order_id)
            order_type = 'print'
        except PrintOrder.DoesNotExist:
            try:
                order = TypingOrder.objects.get(id=order_id)
                order_type = 'typing'
            except TypingOrder.DoesNotExist:
                error = "No order found with this ID."
    elif email:
        print_orders = PrintOrder.objects.filter(email__iexact=email).order_by('-created_at')
        typing_orders = TypingOrder.objects.filter(user_email__iexact=email).order_by('-created_at')
        if print_orders.exists():
            order = print_orders.first()
            order_type = 'print'
            if print_orders.count() > 1:
                error = f'Found {print_orders.count()} print orders. Showing the most recent one.'
        elif typing_orders.exists():
            order = typing_orders.first()
            order_type = 'typing'
            if typing_orders.count() > 1:
                error = f'Found {typing_orders.count()} typing orders. Showing the most recent one.'
        else:
            error = 'No orders found with this email.'

    # Set progress steps and current step index based on order type
    if order_type == 'print':
        progress_steps = [
            'pending', 'awaiting_payment', 'awaiting_approval', 'processing', 'ready', 'completed', 'rejected', 'cancelled'
        ]
    elif order_type == 'typing':
        progress_steps = [
            'pending_review',
            'awaiting_payment',
            'awaiting_approval',
            'in_progress',
            'awaiting_final_approval',
            'completed',
            'rejected',
            'cancelled',
        ]
    else:
        progress_steps = []
    current_step_index = 0
    if order and order.status in progress_steps:
        current_step_index = progress_steps.index(order.status)

    context = {
        'order': order,
        'order_type': order_type,
        'error': error,
        'order_id': order_id or '',
        'email': email or '',
        'progress_steps': progress_steps,
        'current_step_index': current_step_index,
    }
    return render(request, 'print_service/unified_order_track.html', context)

def order_list(request):
    orders = PrintOrder.objects.all().order_by('-created_at')
    paginator = Paginator(orders, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'print_service/order_list.html', {'page_obj': page_obj})

def order_debug_list(request):
    orders = PrintOrder.objects.all().order_by('-created_at')
    return render(request, 'print_service/order_debug_list.html', {'orders': orders})

# -------------------------
# صفحه پرداخت و فیش پرداخت
# -------------------------
def payment_page(request, order_id):
    order = get_object_or_404(PrintOrder, id=order_id)

    base_price = 5000
    if order.color_mode == 'color':
        base_price += 2000
    if order.side_type == 'double':
        base_price += 1000
    if order.num_copies > 1:
        base_price += (order.num_copies - 1) * 1000

    bank_info = {
        'bank_name': 'ملی',
        'account_number': '1234567890',
        'account_holder': 'دفتر هوشمند',
        'card_number': '6037-1234-5678-9012'
    }

    return render(request, 'print_service/payment_page.html', {
        'order': order,
        'amount': base_price,
        'bank_info': bank_info,
    })

# -------------------------
# داشبورد ادمین (استاف)
# -------------------------
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

def staff_dashboard(request):
    status_filter = request.GET.get('status')
    orders = PrintOrder.objects.all().order_by('-created_at')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'print_service/staff_dashboard.html', {'orders': orders, 'status_filter': status_filter})

@staff_member_required
def approve_payment(request, order_id):
    order = get_object_or_404(PrintOrder, id=order_id)
    order.payment_status = 'approved'
    order.status = 'processing'
    order.is_paid = True
    order.save()
    messages.success(request, f'Payment for order #{order.id} approved.')
    return redirect('print_service:staff_dashboard')

@staff_member_required
def reject_payment(request, order_id):
    order = get_object_or_404(PrintOrder, id=order_id)
    order.payment_status = 'rejected'
    order.status = 'rejected'
    order.save()
    messages.error(request, f'Payment for order #{order.id} rejected.')
    return redirect('print_service:staff_dashboard')

@staff_member_required
def mark_printing(request, order_id):
    order = get_object_or_404(PrintOrder, id=order_id)
    order.status = 'processing'
    order.save()
    messages.info(request, f'Order #{order.id} marked as printing.')
    return redirect('print_service:staff_dashboard')

@staff_member_required
def mark_ready(request, order_id):
    order = get_object_or_404(PrintOrder, id=order_id)
    order.status = 'ready'
    order.save()
    messages.info(request, f'Order #{order.id} marked as ready for pickup/delivery.')
    return redirect('print_service:staff_dashboard')

@staff_member_required
def mark_completed(request, order_id):
    order = get_object_or_404(PrintOrder, id=order_id)
    order.status = 'completed'
    order.save()
    messages.success(request, f'Order #{order.id} marked as completed.')
    return redirect('print_service:staff_dashboard')

@staff_member_required
def bank_settings_view(request):
    """Admin view for managing bank account settings"""
    try:
        payment_settings = PaymentSettings.objects.first()
        if not payment_settings:
            payment_settings = PaymentSettings.objects.create(
                bank_name="",
                account_number="",
                card_number="",
                shaba_number=""
            )
    except:
        payment_settings = PaymentSettings.objects.create(
            bank_name="",
            account_number="",
            card_number="",
            shaba_number=""
        )
    
    if request.method == 'POST':
        form = PaymentSettingsForm(request.POST, instance=payment_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank account details updated successfully!')
            return redirect('print_service:bank_settings')
    else:
        form = PaymentSettingsForm(instance=payment_settings)
    
    context = {
        'form': form,
        'payment_settings': payment_settings,
    }
    return render(request, 'print_service/bank_settings.html', context)

