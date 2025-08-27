from django.urls import path
from . import views

app_name = 'digital_shop'

urlpatterns = [
    # Main pages
    path('', views.shop_home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Categories and brands
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('brand/<slug:slug>/', views.brand_detail, name='brand_detail'),
    
    # Shopping cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('cart/apply-coupon/', views.apply_coupon, name='apply_coupon'),
    
    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Reviews
    path('product/<int:product_id>/review/', views.submit_review, name='submit_review'),
    
    # Search
    path('search/', views.search_products, name='search_products'),
    
    # Static pages
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact_us, name='contact'),
    path('terms/', views.terms_conditions, name='terms'),
    path('privacy/', views.privacy_policy, name='privacy'),

    # Payment URLs
    path('order/<int:order_id>/payment/', views.payment_page, name='payment_page'),
    path('order/<int:order_id>/detail/', views.order_detail, name='order_detail'),
    
    # API endpoints for React frontend
    path('api/products/', views.api_products, name='api_products'),
    path('api/product/<int:product_id>/', views.api_product_detail, name='api_product_detail'),
    path('api/cart/', views.api_cart, name='api_cart'),
    path('api/cart/add/', views.api_add_to_cart, name='api_add_to_cart'),
    path('api/cart/update/<int:item_id>/', views.api_update_cart_item, name='api_update_cart_item'),
    path('api/cart/remove/<int:item_id>/', views.api_remove_cart_item, name='api_remove_cart_item'),
    path('api/checkout/', views.api_checkout, name='api_checkout'),
    path('api/orders/', views.api_my_orders, name='api_my_orders'),
    path('api/create-order/', views.api_create_order, name='api_create_order'),
    path('api/orders/<int:order_id>/payment-receipts/', views.api_upload_payment_receipt, name='api_upload_payment_receipt'),
    
    # Admin API endpoints for React admin panel
    path('api/admin/products/', views.api_admin_products, name='api_admin_products'),
    path('api/admin/products/create/', views.api_admin_create_product, name='api_admin_create_product'),
    path('api/admin/products/<int:product_id>/', views.api_admin_update_product, name='api_admin_update_product'),
    path('api/admin/products/<int:product_id>/delete/', views.api_admin_delete_product, name='api_admin_delete_product'),
] 