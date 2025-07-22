from django.urls import path
from . import views

app_name = 'typing_service'

urlpatterns = [
    # Page for creating a new order
    path('create/', views.order_create_view, name='order_create'),

    # Central page for tracking an order, uploading payment, and final approval
    path('track/', views.track_order_view, name='track_order'),

    # Confirmation page after order submission
    path('submitted/<int:order_id>/', views.order_submitted_view, name='order_submitted'),
]