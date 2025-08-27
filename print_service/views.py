from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
from .forms import PrintOrderForm, UploadedFileForm
from .models import PrintOrder, UploadedFile
from django.urls import reverse
import os
import json
from django.contrib.admin.views.decorators import staff_member_required
from typing_service.models import TypingOrder
from .models import PaymentSettings
from .forms import PaymentSettingsForm
from .models import PrintPriceSettings

# -------------------------
# سفارش جدید و آپلود فایل
# -------------------------
@login_required
def order_create(request):
    if request.method == 'POST':
        order_form = PrintOrderForm(request.POST)
        file_form = UploadedFileForm(request.POST, request.FILES)
        if order_form.is_valid() and file_form.is_valid():
            order = order_form.save(commit=False)
            # Set email from authenticated user
            if request.user.is_authenticated:
                order.email = request.user.email
            order.save()
            
            uploaded_file = file_form.save(commit=False)
            uploaded_file.order = order
            uploaded_file.save()
            
            # Handle selected accessories
            import json
            selected_accessories = request.POST.get('selected_accessories')
            if selected_accessories:
                try:
                    accessories_data = json.loads(selected_accessories)
                    from .models import Accessory, PrintOrderAccessory
                    for acc_data in accessories_data:
                        accessory_id = acc_data.get('id')
                        quantity = acc_data.get('quantity', 1)
                        try:
                            accessory = Accessory.objects.get(id=accessory_id)
                            PrintOrderAccessory.objects.create(
                                order=order,
                                accessory=accessory,
                                quantity=quantity,
                                price=accessory.base_price * quantity
                            )
                        except Accessory.DoesNotExist:
                            continue
                except (json.JSONDecodeError, ValueError):
                    pass
            
            return redirect('print_service:order_submitted', order_id=order.id)
    else:
        order_form = PrintOrderForm()
        file_form = UploadedFileForm()
    
    # Get accessories grouped by category
    from .models import Accessory, PrintPriceSettings
    accessories = Accessory.objects.filter(is_active=True, service_type__in=['print', 'both'])
    accessories_by_category = {}
    for accessory in accessories:
        if accessory.category not in accessories_by_category:
            accessories_by_category[accessory.category] = []
        accessories_by_category[accessory.category].append(accessory)
    
    # Get base price from settings
    try:
        price_settings = PrintPriceSettings.objects.first()
        base_price = price_settings.base_price_per_page if price_settings else 50000
    except:
        base_price = 50000
    
    return render(request, 'print_service/order_create.html', {
        'order_form': order_form,
        'file_form': file_form,
        'accessories_by_category': accessories_by_category,
        'base_price': base_price,
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
    # payment_form = PrintOrderSlipForm(instance=order) if order else PrintOrderSlipForm()
    # if request.method == 'POST' and order:
    #     if 'upload_slip' in request.POST:
    #         payment_form = PrintOrderSlipForm(request.POST, request.FILES, instance=order)
    #         if payment_form.is_valid():
    #             order.status = 'awaiting_approval'
    #             payment_form.save()
    #             from django.contrib import messages
    #             messages.success(request, 'Your payment slip has been uploaded and is awaiting approval.')
    #             from django.urls import reverse
    #             return redirect(f"{reverse('print_service:order_track')}?order_id={order.id}&email={order.email}")

    context = {
        'order': order,
        'progress_steps': progress_steps,
        'current_step_index': current_step_index,
        'error': error,
        # 'payment_form': payment_form,
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
    return render(request, 'print_service/order_list.html', {'orders': orders})

@login_required
def my_orders(request):
    """My Orders page for authenticated users"""
    user_email = request.user.email
    
    orders = PrintOrder.objects.filter(email=user_email).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'total_orders': orders.count(),
        'debug_email': user_email,  # For debugging
    }
    
    return render(request, 'print_service/my_orders.html', context)

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

def pricing_api(request):
    """API endpoint for pricing data"""
    try:
        settings = PrintPriceSettings.objects.first()
        if not settings:
            # Create default settings if none exist
            settings = PrintPriceSettings.objects.create()
        
        data = {
            'base_price_per_page': settings.base_price_per_page,
            'color_price_multiplier': float(settings.color_price_multiplier),
            'double_sided_discount': float(settings.double_sided_discount),
            'a4_price': settings.a4_price,
            'a3_price': settings.a3_price,
            'a5_price': settings.a5_price,
            'letter_price': settings.letter_price,
            'bulk_discount_10': float(settings.bulk_discount_10),
            'bulk_discount_50': float(settings.bulk_discount_50),
            'bulk_discount_100': float(settings.bulk_discount_100),
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def store_order(request):
    """Store-like order interface"""
    from .models import Accessory
    accessories = Accessory.objects.filter(is_active=True).order_by('category', 'sort_order')
    
    context = {
        'accessories': accessories,
    }
    return render(request, 'print_service/store_order.html', context)


def accessories_api(request):
    """API endpoint for accessories data"""
    from .models import Accessory
    try:
        accessories = Accessory.objects.filter(is_active=True, service_type__in=['print', 'both']).order_by('category', 'sort_order')
        
        # Group accessories by category
        accessories_by_category = {}
        for accessory in accessories:
            if accessory.category not in accessories_by_category:
                accessories_by_category[accessory.category] = []
            accessories_by_category[accessory.category].append({
                'id': accessory.id,
                'name': accessory.name,
                'description': accessory.description,
                'base_price': float(accessory.base_price),
                'category': accessory.category,
                'service_type': accessory.service_type,
                'is_active': accessory.is_active,
                'is_featured': accessory.is_featured,
                'icon': accessory.icon,
                'color': accessory.color,
            })
        
        return JsonResponse({
            'accessories_by_category': accessories_by_category,
            'success': True
        })
    except Exception as e:
        return JsonResponse({'error': str(e), 'success': False}, status=500)


def typing_accessories_api(request):
    """API endpoint for typing accessories data"""
    from .models import Accessory
    try:
        accessories = Accessory.objects.filter(is_active=True, service_type__in=['typing', 'both']).order_by('category', 'sort_order')
        
        # Group accessories by category
        accessories_by_category = {}
        for accessory in accessories:
            if accessory.category not in accessories_by_category:
                accessories_by_category[accessory.category] = []
            accessories_by_category[accessory.category].append({
                'id': accessory.id,
                'name': accessory.name,
                'description': accessory.description,
                'base_price': float(accessory.base_price),
                'category': accessory.category,
                'service_type': accessory.service_type,
                'is_active': accessory.is_active,
                'is_featured': accessory.is_featured,
                'icon': accessory.icon,
                'color': accessory.color,
            })
        
        return JsonResponse({
            'accessories_by_category': accessories_by_category,
            'success': True
        })
    except Exception as e:
        return JsonResponse({'error': str(e), 'success': False}, status=500)

# API Endpoints for React Frontend
@csrf_exempt
def api_create_order(request):
    """API endpoint for creating print orders"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract data from request
            email = data.get('email', request.user.email if request.user.is_authenticated else '')
            phone = data.get('phone', '')
            pages = int(data.get('pages', 1))
            copies = int(data.get('copies', 1))
            paper_size = data.get('paper_size', 'A4')
            color_type = data.get('color_type', 'black_white')
            double_sided = data.get('double_sided', False)
            notes = data.get('notes', '')
            
            # Map frontend fields to model fields
            color_mode = 'color' if color_type == 'color' else 'bw'
            side_type = 'double' if double_sided else 'single'
            
            # Create the order
            order = PrintOrder.objects.create(
                name=data.get('name', 'Customer'),  # Default name if not provided
                email=email,
                phone=phone,
                color_mode=color_mode,
                side_type=side_type,
                paper_size=paper_size,
                num_copies=copies,
                delivery_method='pickup',
                payment_method='online',
                status='pending'
            )
            
            return JsonResponse({
                'success': True,
                'message': 'سفارش چاپ با موفقیت ثبت شد',
                'order_id': order.id,
                'order_data': {
                    'id': order.id,
                    'name': order.name,
                    'email': order.email,
                    'phone': order.phone,
                    'paper_size': order.paper_size,
                    'color_mode': order.color_mode,
                    'side_type': order.side_type,
                    'num_copies': order.num_copies,
                    'delivery_method': order.delivery_method,
                    'payment_method': order.payment_method,
                    'status': order.status,
                    'created_at': order.created_at.isoformat()
                }
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

@csrf_exempt  
def api_my_orders(request):
    """API endpoint to get user's print orders"""
    if request.method == 'GET':
        try:
            email = request.GET.get('email')
            if not email and request.user.is_authenticated:
                email = request.user.email
            
            if not email:
                return JsonResponse({
                    'success': False,
                    'message': 'ایمیل مورد نیاز است'
                }, status=400)
            
            orders = PrintOrder.objects.filter(email__iexact=email).order_by('-created_at')
            
            orders_data = []
            for order in orders:
                # Get accessories for this order
                accessories = order.accessories.all()
                accessories_data = [{
                    'name': acc.accessory.name,
                    'quantity': acc.quantity,
                    'price': float(acc.price)
                } for acc in accessories]
                
                order_data = {
                    'id': order.id,
                    'name': order.name,
                    'email': order.email,
                    'phone': order.phone,
                    'paper_size': order.paper_size,
                    'color_mode': order.color_mode,
                    'side_type': order.side_type,
                    'num_copies': order.num_copies,
                    'delivery_method': order.delivery_method,
                    'payment_method': order.payment_method,
                    'status': order.status,
                    'created_at': order.created_at.isoformat(),
                    'accessories': accessories_data,
                    'total_price': float(order.get_total_price())
                }
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

