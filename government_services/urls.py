from django.urls import path
from . import views

app_name = 'government_services'

urlpatterns = [
    # Main dashboard
    path('', views.digital_life_dashboard, name='digital_life_dashboard'),
    
    # Service management
    path('services/', views.service_list, name='service_list'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('services/<int:service_id>/request/', views.create_service_request, name='create_service_request'),
    path('services/<int:service_id>/guide/', views.service_guide, name='service_guide'),
    
    # User dashboard and requests
    path('my-dashboard/', views.my_dashboard, name='my_dashboard'),
    path('requests/<uuid:request_id>/edit/', views.edit_request, name='edit_request'),
    path('requests/<uuid:request_id>/track/', views.track_request, name='track_request'),
    
    # Categories and life events
    path('category/<int:category_id>/', views.category_services, name='category_services'),
    path('life-event/<int:event_id>/', views.life_event_services, name='life_event_services'),
    
    # Quick actions
    path('quick-action/<int:action_id>/', views.quick_action, name='quick_action'),
    
    # Reviews and feedback
    path('services/<int:service_id>/review/', views.submit_review, name='submit_review'),
    path('feedback/', views.feedback, name='feedback'),
    
    # Support and contact
    path('contact/', views.contact, name='contact'),
    path('statistics/', views.service_statistics, name='statistics'),
    
    # API endpoints
    path('api/search/', views.service_search_api, name='service_search_api'),
] 