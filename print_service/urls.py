from django.urls import path
from . import views

app_name = 'print_service'

urlpatterns = [
    # Public Order URLs
    path('', views.order_create, name='order_create'),
    path('track/', views.order_track, name='order_track'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/summary/', views.order_summary, name='order_summary'),
    path('order/<int:order_id>/submitted/', views.order_submitted, name='order_submitted'),
    path('debug-orders/', views.order_debug_list, name='order_debug_list'),
    path('track-order/', views.unified_order_track, name='unified_order_track'),

    # My Orders (for authenticated users)
    path('my-orders/', views.my_orders, name='my_orders'),

    # Payment URLs
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),

    # API (for admin panel)
    # path('api/order/<int:order_id>/status/', views.update_order_status, name='update_status'),

    # Staff dashboard + actions
    path('admin-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('admin-dashboard/approve/<int:order_id>/', views.approve_payment, name='approve_payment'),
    path('admin-dashboard/reject/<int:order_id>/', views.reject_payment, name='reject_payment'),
    path('admin-dashboard/mark-printing/<int:order_id>/', views.mark_printing, name='mark_printing'),
    path('admin-dashboard/mark-ready/<int:order_id>/', views.mark_ready, name='mark_ready'),
    path('admin-dashboard/mark-completed/<int:order_id>/', views.mark_completed, name='mark_completed'),
    path('admin-dashboard/bank-settings/', views.bank_settings_view, name='bank_settings'),
    # path('admin-settings/', views.staff_settings, name='staff_settings'),
    
    # Store interface
    path('store/', views.store_order, name='store_order'),
    path('api/pricing/', views.pricing_api, name='pricing_api'),
    path('api/accessories/', views.accessories_api, name='accessories_api'),
    path('api/typing-accessories/', views.typing_accessories_api, name='typing_accessories_api'),
    
    # API endpoints for React frontend
    path('api/create/', views.api_create_order, name='api_create_order'),
    path('api/my-orders/', views.api_my_orders, name='api_my_orders'),
]