from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count, Sum
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import uuid

from .models import (
    DigitalService, DigitalServiceCategory, UserServiceRequest, 
    ServiceReview, ServiceStep, UserProfile, ServiceNotification,
    LifeEvent, QuickAction
)
from .forms import (
    ServiceRequestForm, ServiceReviewForm, ServiceSearchForm,
    ServiceFilterForm, ContactForm, ServiceFeedbackForm
)

def digital_life_dashboard(request):
    """Main Digital Life Assistant dashboard"""
    if request.user.is_authenticated:
        # Get user profile or create one
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Get user's active requests
        active_requests = UserServiceRequest.objects.filter(
            user=request.user,
            status__in=['submitted', 'in_progress', 'pending_documents', 'pending_payment', 'under_review']
        ).order_by('-created_at')[:5]
        
        # Get user's recent completed services
        recent_completed = UserServiceRequest.objects.filter(
            user=request.user,
            status='completed'
        ).order_by('-completed_at')[:3]
        
        # Get recommended services based on user activity
        recommended_services = get_recommended_services(request.user)
        
        # Get quick actions
        quick_actions = QuickAction.objects.filter(is_active=True).order_by('sort_order')[:6]
        
        # Get life events
        life_events = LifeEvent.objects.filter(is_active=True).order_by('sort_order')[:4]
        
        # Get notifications
        notifications = [n for n in ServiceNotification.objects.filter(is_active=True) if n.is_current][:3]
        
        # Calculate user stats
        total_requests = UserServiceRequest.objects.filter(user=request.user).count()
        completed_requests = UserServiceRequest.objects.filter(user=request.user, status='completed').count()
        pending_requests = UserServiceRequest.objects.filter(
            user=request.user,
            status__in=['submitted', 'in_progress', 'pending_documents', 'pending_payment', 'under_review']
        ).count()
        
        context = {
            'profile': profile,
            'active_requests': active_requests,
            'recent_completed': recent_completed,
            'recommended_services': recommended_services,
            'quick_actions': quick_actions,
            'life_events': life_events,
            'notifications': notifications,
            'total_requests': total_requests,
            'completed_requests': completed_requests,
            'pending_requests': pending_requests,
        }
    else:
        # For non-authenticated users, show public dashboard
        featured_services = DigitalService.objects.filter(
            is_featured=True, status='active'
        )[:6]
        
        popular_services = DigitalService.objects.filter(
            is_popular=True, status='active'
        )[:6]
        
        new_services = DigitalService.objects.filter(
            is_new=True, status='active'
        )[:4]
        
        life_events = LifeEvent.objects.filter(is_active=True).order_by('sort_order')[:4]
        
        context = {
            'featured_services': featured_services,
            'popular_services': popular_services,
            'new_services': new_services,
            'life_events': life_events,
        }
    
    return render(request, 'government_services/digital_life_dashboard.html', context)

def get_recommended_services(user):
    """Get personalized service recommendations for user"""
    # Get user's completed services
    completed_services = UserServiceRequest.objects.filter(
        user=user, status='completed'
    ).values_list('service__category_id', flat=True)
    
    # Find services in categories user has used before
    if completed_services:
        recommended = DigitalService.objects.filter(
            category_id__in=completed_services,
            status='active'
        ).exclude(
            requests__user=user
        ).order_by('-view_count')[:6]
    else:
        # If no completed services, show popular services
        recommended = DigitalService.objects.filter(
            status='active', is_popular=True
        ).order_by('-view_count')[:6]
    
    return recommended

def service_list(request):
    """Enhanced services listing page with smart filtering"""
    # Get search and filter parameters
    search_form = ServiceSearchForm(request.GET)
    filter_form = ServiceFilterForm(request.GET)
    
    # Start with all active services
    services = DigitalService.objects.filter(status='active')
    
    # Apply search filters
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        difficulty = search_form.cleaned_data.get('difficulty')
        status = search_form.cleaned_data.get('status')
        
        if query:
            services = services.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(short_description__icontains=query) |
                Q(category__name__icontains=query)
            )
        
        if category:
            services = services.filter(category=category)
        
        if difficulty:
            services = services.filter(difficulty=difficulty)
        
        if status:
            services = services.filter(status=status)
    
    # Apply advanced filters
    if filter_form.is_valid():
        featured_only = filter_form.cleaned_data.get('featured_only')
        popular_only = filter_form.cleaned_data.get('popular_only')
        new_only = filter_form.cleaned_data.get('new_only')
        automated_only = filter_form.cleaned_data.get('automated_only')
        express_lane_only = filter_form.cleaned_data.get('express_lane_only')
        sort_by = filter_form.cleaned_data.get('sort_by')
        
        if featured_only:
            services = services.filter(is_featured=True)
        
        if popular_only:
            services = services.filter(is_popular=True)
        
        if new_only:
            services = services.filter(is_new=True)
        
        if automated_only:
            services = services.filter(is_automated=True)
        
        if express_lane_only:
            services = services.filter(has_express_lane=True)
        
        if sort_by:
            services = services.order_by(sort_by)
        else:
            services = services.order_by('sort_order', 'name')
    
    # Pagination
    paginator = Paginator(services, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for sidebar
    categories = DigitalServiceCategory.objects.filter(is_active=True)
    
    # Get featured and popular services
    featured_services = DigitalService.objects.filter(
        is_featured=True, status='active'
    )[:6]
    
    popular_services = DigitalService.objects.filter(
        is_popular=True, status='active'
    )[:6]
    
    # Get quick actions
    quick_actions = QuickAction.objects.filter(is_active=True).order_by('sort_order')[:4]
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'filter_form': filter_form,
        'categories': categories,
        'featured_services': featured_services,
        'popular_services': popular_services,
        'quick_actions': quick_actions,
        'total_services': services.count(),
    }
    
    return render(request, 'government_services/service_list.html', context)

def service_detail(request, service_id):
    """Enhanced detailed view of a digital service"""
    service = get_object_or_404(DigitalService, id=service_id, status='active')
    
    # Increment view count
    service.increment_view_count()
    
    # Get related data
    steps = service.steps.filter(is_active=True).order_by('step_number')
    reviews = service.reviews.filter(is_verified=True).order_by('-created_at')[:5]
    notifications = [n for n in service.notifications.filter(is_active=True) if n.is_current]
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Get related services
    related_services = DigitalService.objects.filter(
        category=service.category,
        status='active'
    ).exclude(id=service.id)[:4]
    
    # Get life events that include this service
    life_events = service.life_events.filter(is_active=True)[:3]
    
    # Check if user has any requests for this service
    user_requests = None
    if request.user.is_authenticated:
        user_requests = UserServiceRequest.objects.filter(
            user=request.user, service=service
        ).order_by('-created_at')[:3]
    
    # Forms
    request_form = ServiceRequestForm()
    review_form = ServiceReviewForm()
    
    context = {
        'service': service,
        'steps': steps,
        'reviews': reviews,
        'notifications': notifications,
        'avg_rating': avg_rating,
        'related_services': related_services,
        'life_events': life_events,
        'user_requests': user_requests,
        'request_form': request_form,
        'review_form': review_form,
    }
    
    return render(request, 'government_services/service_detail.html', context)

@login_required
def create_service_request(request, service_id):
    """Create a new service request with enhanced workflow"""
    service = get_object_or_404(DigitalService, id=service_id, status='active')
    
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.service = service
            service_request.request_id = str(uuid.uuid4())
            
            # Set initial progress based on service complexity
            if service.difficulty == 'easy':
                service_request.progress_percentage = 25
            elif service.difficulty == 'medium':
                service_request.progress_percentage = 15
            else:
                service_request.progress_percentage = 10
            
            service_request.save()
            
            # Award points to user
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.points += 10
            profile.save()
            
            messages.success(request, _('Your service request has been submitted successfully! You earned 10 points!'))
            return redirect('government_services:service_detail', service_id=service_id)
    else:
        form = ServiceRequestForm()
    
    # Get service steps for guidance
    steps = service.steps.filter(is_active=True).order_by('step_number')
    
    context = {
        'form': form,
        'service': service,
        'steps': steps,
    }
    
    return render(request, 'government_services/create_request.html', context)

@login_required
def my_dashboard(request):
    """Personal user dashboard"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get user's requests by status
    active_requests = UserServiceRequest.objects.filter(
        user=request.user,
        status__in=['submitted', 'in_progress', 'pending_documents', 'pending_payment', 'under_review']
    ).order_by('-created_at')
    
    completed_requests = UserServiceRequest.objects.filter(
        user=request.user,
        status='completed'
    ).order_by('-completed_at')[:10]
    
    draft_requests = UserServiceRequest.objects.filter(
        user=request.user,
        status='draft'
    ).order_by('-created_at')
    
    # Get user's service history
    service_history = UserServiceRequest.objects.filter(
        user=request.user
    ).values('service__name', 'service__category__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Get recommended services
    recommended_services = get_recommended_services(request.user)
    
    # Calculate statistics
    total_requests = UserServiceRequest.objects.filter(user=request.user).count()
    completed_count = UserServiceRequest.objects.filter(user=request.user, status='completed').count()
    success_rate = (completed_count / total_requests * 100) if total_requests > 0 else 0
    
    context = {
        'profile': profile,
        'active_requests': active_requests,
        'completed_requests': completed_requests,
        'draft_requests': draft_requests,
        'service_history': service_history,
        'recommended_services': recommended_services,
        'total_requests': total_requests,
        'completed_count': completed_count,
        'success_rate': success_rate,
    }
    
    return render(request, 'government_services/my_dashboard.html', context)

@login_required
def life_event_services(request, event_id):
    """Show services related to a life event"""
    life_event = get_object_or_404(LifeEvent, id=event_id, is_active=True)
    services = life_event.services.filter(status='active').order_by('sort_order', 'name')
    
    context = {
        'life_event': life_event,
        'services': services,
    }
    
    return render(request, 'government_services/life_event_services.html', context)

@login_required
def quick_action(request, action_id):
    """Handle quick action requests"""
    quick_action = get_object_or_404(QuickAction, id=action_id, is_active=True)
    service = quick_action.service
    
    # Create a draft request automatically
    service_request = UserServiceRequest.objects.create(
        user=request.user,
        service=service,
        title=f"Quick Request: {service.name}",
        description=f"Quick action request for {service.name}",
        status='draft',
        progress_percentage=10
    )
    
    messages.success(request, _('Quick action initiated! Please complete your request details.'))
    return redirect('government_services:edit_request', request_id=service_request.request_id)

@login_required
def edit_request(request, request_id):
    """Edit a service request"""
    service_request = get_object_or_404(UserServiceRequest, request_id=request_id, user=request.user)
    
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES, instance=service_request)
        if form.is_valid():
            service_request = form.save()
            if service_request.status == 'draft':
                service_request.status = 'submitted'
                service_request.submitted_at = timezone.now()
                service_request.save()
                messages.success(request, _('Your request has been submitted successfully!'))
            else:
                messages.success(request, _('Your request has been updated successfully!'))
            return redirect('government_services:my_dashboard')
    else:
        form = ServiceRequestForm(instance=service_request)
    
    context = {
        'form': form,
        'service_request': service_request,
    }
    
    return render(request, 'government_services/edit_request.html', context)

@login_required
@require_POST
def submit_review(request, service_id):
    """Submit a service review with enhanced feedback"""
    service = get_object_or_404(DigitalService, id=service_id, status='active')
    
    form = ServiceReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.service = service
        
        # Check if user already reviewed this service
        existing_review = ServiceReview.objects.filter(
            user=request.user, service=service
        ).first()
        
        if existing_review:
            existing_review.rating = review.rating
            existing_review.comment = review.comment
            existing_review.ease_of_use = review.ease_of_use
            existing_review.speed = review.speed
            existing_review.helpfulness = review.helpfulness
            existing_review.save()
            messages.success(request, _('Your review has been updated!'))
        else:
            review.save()
            # Award points for leaving a review
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.points += 5
            profile.save()
            messages.success(request, _('Thank you for your review! You earned 5 points!'))
    
    return redirect('government_services:service_detail', service_id=service_id)

def category_services(request, category_id):
    """Show services by category with enhanced display"""
    category = get_object_or_404(DigitalServiceCategory, id=category_id, is_active=True)
    services = DigitalService.objects.filter(
        category=category, status='active'
    ).order_by('sort_order', 'name')
    
    # Pagination
    paginator = Paginator(services, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get related categories
    related_categories = DigitalServiceCategory.objects.filter(
        is_active=True
    ).exclude(id=category.id)[:4]
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'related_categories': related_categories,
        'total_services': services.count(),
    }
    
    return render(request, 'government_services/category_services.html', context)

def contact(request):
    """Enhanced contact form for support"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you would typically send an email or save to database
            messages.success(request, _('Thank you for your message. We will get back to you soon!'))
            return redirect('government_services:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'government_services/contact.html', context)

def feedback(request):
    """Enhanced feedback form"""
    if request.method == 'POST':
        form = ServiceFeedbackForm(request.POST)
        if form.is_valid():
            # Here you would typically save feedback to database
            messages.success(request, _('Thank you for your feedback!'))
            return redirect('government_services:feedback')
    else:
        form = ServiceFeedbackForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'government_services/feedback.html', context)

def service_statistics(request):
    """Show enhanced service statistics"""
    total_services = DigitalService.objects.filter(status='active').count()
    total_categories = DigitalServiceCategory.objects.filter(is_active=True).count()
    total_requests = UserServiceRequest.objects.count()
    total_reviews = ServiceReview.objects.count()
    
    # Most popular services
    popular_services = DigitalService.objects.filter(
        status='active'
    ).order_by('-view_count')[:10]
    
    # Categories with most services
    category_stats = DigitalServiceCategory.objects.filter(
        is_active=True
    ).annotate(
        service_count=Count('services')
    ).order_by('-service_count')[:10]
    
    # Recent requests
    recent_requests = UserServiceRequest.objects.select_related(
        'user', 'service'
    ).order_by('-created_at')[:5]
    
    # User statistics
    if request.user.is_authenticated:
        user_stats = UserServiceRequest.objects.filter(user=request.user).aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            in_progress=Count('id', filter=Q(status__in=['submitted', 'in_progress', 'pending_documents', 'pending_payment', 'under_review']))
        )
    else:
        user_stats = None
    
    context = {
        'total_services': total_services,
        'total_categories': total_categories,
        'total_requests': total_requests,
        'total_reviews': total_reviews,
        'popular_services': popular_services,
        'category_stats': category_stats,
        'recent_requests': recent_requests,
        'user_stats': user_stats,
    }
    
    return render(request, 'government_services/statistics.html', context)

@csrf_exempt
def service_search_api(request):
    """Enhanced API endpoint for service search"""
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if query:
            services = DigitalService.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(short_description__icontains=query),
                status='active'
            )[:10]
            
            results = []
            for service in services:
                results.append({
                    'id': service.id,
                    'name': service.name,
                    'description': service.short_description or service.description[:100] + '...' if len(service.description) > 100 else service.description,
                    'category': service.category.name,
                    'difficulty': service.get_difficulty_display(),
                    'icon': service.icon,
                    'color': service.color,
                    'url': reverse('government_services:service_detail', args=[service.id])
                })
            
            return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})

def service_guide(request, service_id):
    """Enhanced service guide with steps"""
    service = get_object_or_404(DigitalService, id=service_id, status='active')
    steps = service.steps.filter(is_active=True).order_by('step_number')
    
    context = {
        'service': service,
        'steps': steps,
    }
    
    return render(request, 'government_services/service_guide.html', context)

@login_required
def track_request(request, request_id):
    """Track a specific service request"""
    service_request = get_object_or_404(UserServiceRequest, request_id=request_id, user=request.user)
    
    # Get service steps for progress tracking
    steps = service_request.service.steps.filter(is_active=True).order_by('step_number')
    
    context = {
        'service_request': service_request,
        'steps': steps,
    }
    
    return render(request, 'government_services/track_request.html', context)
