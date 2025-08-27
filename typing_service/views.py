from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import TypingOrder
from .forms import TypingOrderForm
from print_service.models import PaymentSettings # Import settings


@login_required
def order_create_view(request):
    """
    Allows a user to create a new typing order and sends a confirmation email.
    """
    if request.method == 'POST':
        form = TypingOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            # Set email from authenticated user
            if request.user.is_authenticated:
                order.user_email = request.user.email
            order.save()

            # Handle selected accessories
            import json
            selected_accessories = request.POST.get('selected_accessories')
            if selected_accessories:
                try:
                    accessories_data = json.loads(selected_accessories)
                    from print_service.models import Accessory
                    from .models import TypingOrderAccessory
                    for acc_data in accessories_data:
                        accessory_id = acc_data.get('id')
                        quantity = acc_data.get('quantity', 1)
                        try:
                            accessory = Accessory.objects.get(id=accessory_id)
                            TypingOrderAccessory.objects.create(
                                order=order,
                                accessory=accessory,
                                quantity=quantity,
                                price=accessory.base_price * quantity
                            )
                        except Accessory.DoesNotExist:
                            continue
                except (json.JSONDecodeError, ValueError):
                    pass

            # Send confirmation email
            if order.user_email:
                subject = _('Your Typing Order #{id} has been submitted!').format(id=order.id)
                track_url = request.build_absolute_uri(
                    reverse('typing_service:track_order') + f'?order_id={order.id}&email={order.user_email}'
                )
                html_message = render_to_string('typing_service/emails/order_confirmation.html', {
                    'order': order,
                    'track_url': track_url,
                })
                send_mail(
                    subject,
                    '', # Plain text version (optional)
                    'noreply@smartoffice.com',
                    [order.user_email],
                    html_message=html_message,
                    fail_silently=True # Prevents crashing if email fails
                )

            return redirect('typing_service:order_submitted', order_id=order.id)
    else:
        form = TypingOrderForm()
    
    # Get accessories grouped by category
    from print_service.models import Accessory
    accessories = Accessory.objects.filter(is_active=True, service_type__in=['typing', 'both'])
    accessories_by_category = {}
    for accessory in accessories:
        if accessory.category not in accessories_by_category:
            accessories_by_category[accessory.category] = []
        accessories_by_category[accessory.category].append(accessory)
    
    return render(request, 'typing_service/order_create.html', {
        'form': form,
        'accessories_by_category': accessories_by_category,
    })


def order_submitted_view(request, order_id):
    order = get_object_or_404(TypingOrder, id=order_id)
    return render(request, 'typing_service/order_submitted.html', {'order': order})


def track_order_view(request):
    """
    Central hub for the user to track their order, upload payment slips,
    and give final approval.
    """
    order = None
    error = None
    order_id = request.GET.get('order_id') or request.POST.get('order_id_hidden')
    email = request.GET.get('email')

    # --- Find the order ---
    if order_id:
        try:
            query_kwargs = {'id': order_id}
            if email:
                query_kwargs['user_email'] = email
            order = TypingOrder.objects.get(**query_kwargs)
        except TypingOrder.DoesNotExist:
            error = _("No order found with the provided details.")

    # --- Define progress steps for the template ---
    progress_steps = [
        'pending_review',
        'awaiting_payment',
        'awaiting_approval',
        'in_progress',
        'awaiting_final_approval',
        'completed',
    ]
    current_step_index = 0
    if order and order.status in progress_steps:
        current_step_index = progress_steps.index(order.status)

    # --- Define progress steps and bank info for the template ---
    bank_info = PaymentSettings.objects.first() # Get bank details

    # --- Handle POST requests for final approval ---
    if request.method == 'POST' and order:
        if 'final_user_approval' in request.POST:
            order.final_approved_by_user = True
            order.delivery_option = request.POST.get('delivery_option')
            order.status = 'completed'
            order.save()
            messages.success(request, _('Thank you for your final approval. Your order is now complete.'))
            return redirect(f"{request.path}?order_id={order.id}&email={order.user_email}")

    context = {
        'order': order,
        'error': error,
        'progress_steps': progress_steps,
        'current_step_index': current_step_index,
        'bank_info': bank_info, # Add bank info to context
    }
    return render(request, 'typing_service/track_order.html', context)


@login_required
def my_orders(request):
    """My Orders page for authenticated users"""
    user_email = request.user.email
    
    orders = TypingOrder.objects.filter(user_email=user_email).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'total_orders': orders.count(),
        'debug_email': user_email,  # For debugging
    }
    
    return render(request, 'typing_service/my_orders.html', context)


# API Endpoints for React Frontend
@csrf_exempt
@require_http_methods(["POST"])
def api_create_order(request):
    """API endpoint to create a typing order"""
    try:
        data = json.loads(request.body)
        
        # Create order
        order = TypingOrder.objects.create(
            user_name=data.get('user_name', ''),
            user_email=data.get('user_email', ''),
            user_phone=data.get('user_phone', ''),
            description=data.get('description', ''),
            page_count=data.get('page_count', 1),
            delivery_option=data.get('delivery_option', 'email'),
            status='pending_review'
        )
        
        # Handle accessories if provided
        accessories = data.get('accessories', [])
        if accessories:
            from print_service.models import Accessory
            from .models import TypingOrderAccessory
            for acc_data in accessories:
                try:
                    accessory = Accessory.objects.get(id=acc_data['id'])
                    TypingOrderAccessory.objects.create(
                        order=order,
                        accessory=accessory,
                        quantity=acc_data.get('quantity', 1),
                        price=accessory.base_price * acc_data.get('quantity', 1)
                    )
                except Accessory.DoesNotExist:
                    continue
        
        return JsonResponse({
            'success': True,
            'message': 'سفارش تایپ با موفقیت ثبت شد',
            'order_id': order.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در ثبت سفارش: {str(e)}'
        }, status=400)


@require_http_methods(["GET"])
def api_user_orders(request):
    """API endpoint to get user's typing orders"""
    user_email = request.GET.get('email')
    
    if not user_email:
        return JsonResponse({
            'success': False,
            'message': 'ایمیل کاربر الزامی است'
        }, status=400)
    
    try:
        orders = TypingOrder.objects.filter(user_email=user_email).order_by('-created_at')
        
        orders_data = []
        for order in orders:
            # Get accessories for this order
            accessories = order.accessories.all()
            accessories_data = [{
                'name': acc.accessory.name,
                'quantity': acc.quantity,
                'price': acc.price
            } for acc in accessories]
            
            orders_data.append({
                'id': order.id,
                'user_name': order.user_name,
                'user_phone': order.user_phone,
                'description': order.description,
                'page_count': order.page_count,
                'delivery_option': order.delivery_option,
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'accessories': accessories_data,
                'total_price': order.get_total_price() if hasattr(order, 'get_total_price') else 0
            })
        
        return JsonResponse({
            'success': True,
            'orders': orders_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در بازیابی سفارشات: {str(e)}'
        }, status=400)


@require_http_methods(["GET"])
def api_accessories(request):
    """API endpoint to get available accessories for typing service"""
    try:
        from print_service.models import Accessory
        
        accessories = Accessory.objects.filter(
            is_active=True,
            service_type__in=['typing', 'both']
        )
        
        accessories_by_category = {}
        for accessory in accessories:
            if accessory.category not in accessories_by_category:
                accessories_by_category[accessory.category] = []
            
            accessories_by_category[accessory.category].append({
                'id': accessory.id,
                'name': accessory.name,
                'description': accessory.description,
                'base_price': accessory.base_price,
                'category': accessory.category
            })
        
        return JsonResponse({
            'success': True,
            'accessories_by_category': accessories_by_category
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در بازیابی لوازم جانبی: {str(e)}'
        }, status=400)


def debug_accessories(request):
    """Debug view to check accessories data"""
    from print_service.models import Accessory
    from .forms import TypingOrderForm
    
    form = TypingOrderForm()
    
    # Get accessories grouped by category
    accessories = Accessory.objects.filter(is_active=True, service_type__in=['typing', 'both'])
    accessories_by_category = {}
    for accessory in accessories:
        if accessory.category not in accessories_by_category:
            accessories_by_category[accessory.category] = []
        accessories_by_category[accessory.category].append(accessory)
    
    return render(request, 'typing_service/debug_accessories.html', {
        'form': form,
        'accessories_by_category': accessories_by_category,
    })
