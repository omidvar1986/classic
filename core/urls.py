from django.urls import path
from . import views

app_name = 'core'
 
urlpatterns = [
    path('', views.home, name='home'),
    path('redirect/', views.redirect_to_print_service, name='redirect_to_print'),
    path('change-language/', views.change_language, name='change_language'),
] 