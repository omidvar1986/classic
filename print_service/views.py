from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .forms import AdminPaymentReviewForm  
from .models import PrintOrder, UploadedFile
from .forms import PrintOrderForm, UploadedFileForm, PrintOrderSlipForm

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

            messages.success(request, f'Order #{order.id} created successfully!')

            if order.payment_method == 'online':
                return redirect('print_service:payment_slip_upload', order_id=order.id)
            else:
                return redirect('print_service:order_detail', order_id=order.id)
    else:
        order_form = PrintOrderForm()
        file_form = UploadedFileForm()

    return render(request, 'print_service/order_create.html', {
        'order_form': order_form,
        'file_form': file_form,
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
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        email = request.POST.get('email')

        if order_id:
            try:
                order = PrintOrder.objects.get(id=order_id)
            except PrintOrder.DoesNotExist:
                messages.error(request, 'Order not found with this ID.')
        elif email:
            orders = PrintOrder.objects.filter(email=email).order_by('-created_at')
            if orders.exists():
                order = orders.first()
                if orders.count() > 1:
                    messages.info(request, f'Found {orders.count()} orders. Showing the most recent one.')
            else:
                messages.error(request, 'No orders found with this email.')

    return render(request, 'print_service/order_track.html', {'order': order})

def order_list(request):
    orders = PrintOrder.objects.all().order_by('-created_at')
    paginator = Paginator(orders, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'print_service/order_list.html', {'page_obj': page_obj})

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

def payment_slip_upload(request, order_id):
    order = get_object_or_404(PrintOrder, id=order_id)
    if request.method == 'POST':
        form = PrintOrderSlipForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment slip uploaded successfully!')
            return redirect('print_service:order_detail', order_id=order.id)
    else:
        form = PrintOrderSlipForm(instance=order)

    return render(request, 'print_service/payment_upload.html', {
        'order': order,
        'form': form,
    })

# -------------------------
# داشبورد ادمین (استاف)
# -------------------------
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

