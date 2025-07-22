from django.urls import path
from . import views

app_name = 'print_service'

urlpatterns = [
    # Public Order URLs
    path('', views.order_create, name='order_create'),
    path('track/', views.order_track, name='order_track'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    # Payment URLs
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('order/<int:order_id>/payment-upload/', views.payment_slip_upload, name='payment_slip_upload'),

    # API (for admin panel)
    # path('api/order/<int:order_id>/status/', views.update_order_status, name='update_status'),

    # Staff dashboard + actions
    # path('admin-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    # path('admin-dashboard/approve/<int:order_id>/', views.approve_payment, name='approve_payment'),
    # path('admin-dashboard/reject/<int:order_id>/', views.reject_payment, name='reject_payment'),
    # path('admin-dashboard/review/<int:order_id>/', views.review_payment, name='review_payment'),
    # path('admin-settings/', views.staff_settings, name='staff_settings'),
]