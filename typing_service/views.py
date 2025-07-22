from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from .models import TypingOrder
from .forms import TypingOrderForm, PaymentSlipForm
from print_service.models import PaymentSettings # Import settings


def order_create_view(request):
    """
    Allows a user to create a new typing order and sends a confirmation email.
    """
    if request.method == 'POST':
        form = TypingOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()

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
    return render(request, 'typing_service/order_create.html', {'form': form})


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
    steps = [
        'pending_review',
        'awaiting_payment',
        'awaiting_approval',
        'in_progress',
        'awaiting_final_approval',
        'completed'
    ]
    current_step_index = -1
    if order and order.status in steps:
        current_step_index = steps.index(order.status)

    # --- Define progress steps and bank info for the template ---
    bank_info = PaymentSettings.objects.first() # Get bank details
    steps = [
        'pending_review',
        'awaiting_payment',
        'awaiting_approval',
        'in_progress',
        'awaiting_final_approval',
        'completed'
    ]
    current_step_index = -1
    if order and order.status in steps:
        current_step_index = steps.index(order.status)

    # --- Handle POST requests for payment slip upload and final approval ---
    if request.method == 'POST' and order:
        # Handle payment slip upload
        if 'upload_slip' in request.POST:
            payment_form = PaymentSlipForm(request.POST, request.FILES, instance=order)
            if payment_form.is_valid():
                order.status = 'awaiting_approval'
                payment_form.save()
                messages.success(request, _('Your payment slip has been uploaded and is awaiting approval.'))
                return redirect(f"{request.path}?order_id={order.id}&email={order.user_email}")
        
        # Handle final user approval
        elif 'final_user_approval' in request.POST:
            order.final_approved_by_user = True
            order.delivery_option = request.POST.get('delivery_option')
            order.status = 'completed'
            order.save()
            messages.success(request, _('Thank you for your final approval. Your order is now complete.'))
            return redirect(f"{request.path}?order_id={order.id}&email={order.user_email}")

    # --- Prepare context for the template ---
    payment_form = PaymentSlipForm(instance=order) if order else PaymentSlipForm()
    
    context = {
        'order': order,
        'error': error,
        'payment_form': payment_form,
        'query_params': {'order_id': order.id, 'email': order.user_email} if order else {},
        'progress_steps': steps,
        'current_step_index': current_step_index,
        'bank_info': bank_info, # Add bank info to context
    }
    return render(request, 'typing_service/track_order.html', context)