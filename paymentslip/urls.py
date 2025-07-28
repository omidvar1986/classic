from django.urls import path
from .views import upload_payment_slip

app_name = 'paymentslip'

urlpatterns = [
    path('upload/<str:order_type>/<int:order_id>/', upload_payment_slip, name='upload'),
] 