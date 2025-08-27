from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.urls import reverse
from print_service.models import PrintOrder
from typing_service.models import TypingOrder
import json

# Create your views here.

# Login view
@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to authenticate with email as username first
        user = authenticate(request, username=email, password=password)
        
        # If that fails, try to find user by email and authenticate with username
        if user is None:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')

# Logout view

def logout_view(request):
    logout(request)
    return redirect(reverse('core:home'))

# Register view

def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=email).exists():
            messages.error(request, 'Email is already registered.')
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            login(request, user)
            return redirect('accounts:dashboard')
    return render(request, 'accounts/register.html')

# (Password reset views can be added next)

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='accounts/password_reset_email.html',
                subject_template_name='accounts/password_reset_subject.txt',
            )
            return redirect('accounts:password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})

def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'accounts/password_reset_invalid.html')

def password_reset_complete(request):
    return render(request, 'accounts/password_reset_complete.html')

@login_required
def dashboard(request):
    user = request.user
    # Show orders for this user (by email)
    print_orders = PrintOrder.objects.filter(email__iexact=user.email).order_by('-created_at')
    typing_orders = TypingOrder.objects.filter(user_email__iexact=user.email).order_by('-created_at')
    return render(request, 'accounts/dashboard.html', {
        'print_orders': print_orders,
        'typing_orders': typing_orders,
        'user': user,
    })

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff or u.is_superuser)(view_func)

@staff_required
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

@staff_required
def user_management(request):
    # Redirect to the comprehensive user management in admin_dashboard app
    return redirect('admin_dashboard:user_management')

@csrf_exempt
def api_login(request):
    """API endpoint for React frontend login"""
    if request.method == 'OPTIONS':
        # Handle CORS preflight
        response = JsonResponse({'status': 'ok'})
        return response
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            # Find user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'کاربری با این ایمیل یافت نشد'
                }, status=400)
            
            # Authenticate user
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'token': 'dummy-token',  # In production, use JWT tokens
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_staff': user.is_staff,
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'رمز عبور اشتباه است'
                }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'داده‌های ارسالی نامعتبر است'
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def api_logout(request):
    """API endpoint for React frontend logout"""
    if request.method == 'OPTIONS':
        # Handle CORS preflight
        response = JsonResponse({'status': 'ok'})
        return response
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'خروج موفقیت‌آمیز بود'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@login_required
def api_profile(request):
    """API endpoint to get user profile"""
    if request.method == 'GET':
        return JsonResponse({
            'success': True,
            'user': {
                'id': request.user.id,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_staff': request.user.is_staff,
            }
        })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def api_register(request):
    """API endpoint for React frontend registration"""
    if request.method == 'OPTIONS':
        # Handle CORS preflight
        response = JsonResponse({'status': 'ok'})
        return response
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'کاربری با این ایمیل قبلاً ثبت شده است'
                }, status=400)
            
            # Create user
            username = email.split('@')[0]  # Use email prefix as username
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Login user
            login(request, user)
            
            return JsonResponse({
                'success': True,
                'token': 'dummy-token',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'داده‌های ارسالی نامعتبر است'
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
