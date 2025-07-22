from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('approve/<str:service_type>/<int:order_id>/', views.approve_payment_view, name='approve_payment'),
    path('reject/<str:service_type>/<int:order_id>/', views.reject_payment_view, name='reject_payment'),
    path('review/<str:service_type>/<int:order_id>/', views.review_payment_view, name='review_payment'),
    path('delete/<str:service_type>/<int:order_id>/', views.delete_order_view, name='delete_order'),
    path('final-approve/<int:order_id>/', views.approve_final_download, name='approve_final_download'),
    path('finalize/<int:order_id>/', views.finalize_order, name='finalize_order'),
]