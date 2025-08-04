from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('approve/<str:service_type>/<int:order_id>/', views.approve_payment_view, name='approve_payment'),
    path('reject/<str:service_type>/<int:order_id>/', views.reject_payment_view, name='reject_payment'),
    path('delete/<str:service_type>/<int:order_id>/', views.delete_order_view, name='delete_order'),
    path('review/<str:service_type>/<int:order_id>/', views.review_payment_view, name='review_payment'),
    path('approve-final/<int:order_id>/', views.approve_final_download, name='approve_final_download'),
    path('finalize/<int:order_id>/', views.finalize_order, name='finalize_order'),
    path('direct-access/', views.direct_admin_access, name='direct_access'),
    
    # Settings Management
    path('settings/', views.settings_dashboard, name='settings_dashboard'),
    path('settings/print-pricing/', views.print_pricing, name='print_pricing'),
    path('settings/save-print-pricing/', views.save_print_pricing, name='save_print_pricing'),
    path('settings/typing-pricing/', views.typing_pricing, name='typing_pricing'),
    path('settings/save-typing-pricing/', views.save_typing_pricing, name='save_typing_pricing'),
    path('settings/packages/', views.packages_management, name='packages_management'),
    path('settings/payment/', views.payment_settings, name='payment_settings'),
    
    # Accessories Management URLs
    path('accessories/', views.accessories_view, name='accessories'),
    path('accessories/add/', views.add_accessory_view, name='add_accessory'),
    path('accessories/<int:accessory_id>/edit/', views.edit_accessory_view, name='edit_accessory'),
    path('accessories/<int:accessory_id>/delete/', views.delete_accessory_view, name='delete_accessory'),
    path('accessories/bulk-edit/', views.bulk_edit_accessories_view, name='bulk_edit_accessories'),
    
    # Package Deals Management URLs
    path('packages/', views.packages_view, name='packages'),
    path('packages/add/', views.add_package_view, name='add_package'),
    path('packages/<int:package_id>/edit/', views.edit_package_view, name='edit_package'),
    path('packages/<int:package_id>/delete/', views.delete_package_view, name='delete_package'),
    
    # User Management URLs
    path('users/', views.user_management_view, name='user_management'),
    path('users/<int:user_id>/', views.user_detail_view, name='user_detail'),
    path('users/<int:user_id>/edit/', views.edit_user_view, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user_view, name='delete_user'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status_view, name='toggle_user_status'),
    path('users/<int:user_id>/toggle-staff/', views.toggle_staff_status_view, name='toggle_staff_status'),
    path('users/statistics/', views.user_statistics_view, name='user_statistics'),
    
    # Government Services Management URLs
    path('government-services/', views.government_services_view, name='government_services'),
    path('government-services/requests/', views.government_requests_view, name='government_requests'),
    path('government-services/requests/<int:request_id>/', views.government_request_detail_view, name='government_request_detail'),
    path('government-services/requests/<int:request_id>/update/', views.update_government_request_view, name='update_government_request'),
    
    # Digital Shop Management URLs
    path('digital-shop/', views.digital_shop_dashboard, name='digital_shop_dashboard'),
    path('digital-shop/products/', views.digital_shop_products, name='digital_shop_products'),
    path('digital-shop/products/add/', views.digital_shop_add_product, name='digital_shop_add_product'),
    path('digital-shop/products/<int:product_id>/edit/', views.digital_shop_edit_product, name='digital_shop_edit_product'),
    path('digital-shop/products/<int:product_id>/delete/', views.digital_shop_delete_product, name='digital_shop_delete_product'),
    path('digital-shop/categories/', views.digital_shop_categories, name='digital_shop_categories'),
    path('digital-shop/brands/', views.digital_shop_brands, name='digital_shop_brands'),
    path('digital-shop/orders/', views.digital_shop_orders, name='digital_shop_orders'),
    path('digital-shop/orders/<int:order_id>/', views.digital_shop_order_detail, name='digital_shop_order_detail'),
    
    # Accessories Management
    path('accessories/', views.accessories_management, name='accessories_management'),
    path('accessories/<int:accessory_id>/edit/', views.get_accessory, name='get_accessory'),
    path('accessories/save/', views.save_accessory, name='save_accessory'),
    path('accessories/<int:accessory_id>/delete/', views.delete_accessory, name='delete_accessory'),

    # Payment Receipts Management
    path('payment-receipts/', views.payment_receipts_management, name='payment_receipts_management'),
    path('payment-receipts/<int:receipt_id>/approve/', views.approve_payment_receipt, name='approve_payment_receipt'),
    path('payment-receipts/<int:receipt_id>/reject/', views.reject_payment_receipt, name='reject_payment_receipt'),
]