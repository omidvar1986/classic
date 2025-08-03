from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from .models import TypingOrder
from .forms import TypingOrderForm
from print_service.models import PaymentSettings # Import settings


def order_create_view(request):
    """
    Allows a user to create a new typing order and sends a confirmation email.
    """
    if request.method == 'POST':
        form = TypingOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()

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