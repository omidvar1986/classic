from django.urls import path
from . import views

app_name = 'typing_service'

urlpatterns = [
    # Page for creating a new order
    path('create/', views.order_create_view, name='order_create'),

    # Central page for tracking an order, uploading payment, and final approval
    path('track/', views.track_order_view, name='track_order'),

    # My Orders (for authenticated users)
    path('my-orders/', views.my_orders, name='my_orders'),

    # Confirmation page after order submission
    path('submitted/<int:order_id>/', views.order_submitted_view, name='order_submitted'),
    
    # API endpoints for React frontend
    path('api/create/', views.api_create_order, name='api_create_order'),
    path('api/orders/', views.api_user_orders, name='api_user_orders'),
    path('api/accessories/', views.api_accessories, name='api_accessories'),
    
    # Debug URL
    path('debug/accessories/', views.debug_accessories, name='debug_accessories'),
]
