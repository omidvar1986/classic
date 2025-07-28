from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentSlipUploadForm

# Create your views here.

def upload_payment_slip(request, order_type, order_id):
    # order_type: 'print' or 'typing'
    if order_type == 'print':
        from print_service.models import PrintOrder as OrderModel
    elif order_type == 'typing':
        from typing_service.models import TypingOrder as OrderModel
    else:
        raise ValueError("Invalid order type")
    order = get_object_or_404(OrderModel, id=order_id)

    if request.method == 'POST':
        form = PaymentSlipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            order.payment_slip = form.cleaned_data['payment_slip']
            order.status = 'awaiting_approval'
            order.save()
            return redirect('print_service:order_track' if order_type == 'print' else 'typing_service:track_order')
    else:
        form = PaymentSlipUploadForm()
    return render(request, 'paymentslip/upload.html', {'form': form, 'order': order, 'order_type': order_type})
