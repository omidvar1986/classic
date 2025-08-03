from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from government_services.models import (
    DigitalServiceCategory, DigitalService, LifeEvent, 
    QuickAction, ServiceStep, ServiceNotification
)
from django.utils import timezone

class Command(BaseCommand):
    help = 'Set up sample data for Digital Life Assistant'

    def handle(self, *args, **options):
        self.stdout.write('Setting up Digital Life Assistant sample data...')
        
        # Create categories
        categories = self.create_categories()
        
        # Create services
        services = self.create_services(categories)
        
        # Create life events
        life_events = self.create_life_events(services)
        
        # Create quick actions
        quick_actions = self.create_quick_actions(services)
        
        # Create service steps
        self.create_service_steps(services)
        
        # Create notifications
        self.create_notifications(services)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created:\n'
                f'- {len(categories)} categories\n'
                f'- {len(services)} services\n'
                f'- {len(life_events)} life events\n'
                f'- {len(quick_actions)} quick actions\n'
                f'Digital Life Assistant is ready!'
            )
        )

    def create_categories(self):
        categories_data = [
            {
                'name': 'Identity & Documents',
                'description': 'National ID, passport, birth certificate, and other identity documents',
                'icon': 'fas fa-id-card',
                'color': 'primary',
                'gradient_start': '#007bff',
                'gradient_end': '#0056b3',
                'is_featured': True,
                'sort_order': 1
            },
            {
                'name': 'Business & Entrepreneurship',
                'description': 'Business registration, licenses, permits, and corporate services',
                'icon': 'fas fa-briefcase',
                'color': 'success',
                'gradient_start': '#28a745',
                'gradient_end': '#1e7e34',
                'is_featured': True,
                'sort_order': 2
            },
            {
                'name': 'Education & Training',
                'description': 'Student services, certificates, academic records, and training programs',
                'icon': 'fas fa-graduation-cap',
                'color': 'info',
                'gradient_start': '#17a2b8',
                'gradient_end': '#117a8b',
                'sort_order': 3
            },
            {
                'name': 'Health & Medical',
                'description': 'Health insurance, medical certificates, pharmacy licenses, and health services',
                'icon': 'fas fa-heartbeat',
                'color': 'danger',
                'gradient_start': '#dc3545',
                'gradient_end': '#c82333',
                'sort_order': 4
            },
            {
                'name': 'Transportation & Travel',
                'description': 'Driver licenses, vehicle registration, travel permits, and transportation services',
                'icon': 'fas fa-car',
                'color': 'warning',
                'gradient_start': '#ffc107',
                'gradient_end': '#e0a800',
                'sort_order': 5
            },
            {
                'name': 'Property & Real Estate',
                'description': 'Property registration, building permits, real estate services, and housing',
                'icon': 'fas fa-home',
                'color': 'secondary',
                'gradient_start': '#6c757d',
                'gradient_end': '#545b62',
                'sort_order': 6
            },
            {
                'name': 'Financial Services',
                'description': 'Banking services, tax payments, financial certificates, and economic services',
                'icon': 'fas fa-university',
                'color': 'dark',
                'gradient_start': '#343a40',
                'gradient_end': '#1d2124',
                'sort_order': 7
            },
            {
                'name': 'Social Services',
                'description': 'Social security, welfare services, family support, and community services',
                'icon': 'fas fa-hands-helping',
                'color': 'primary',
                'gradient_start': '#007bff',
                'gradient_end': '#0056b3',
                'sort_order': 8
            }
        ]
        
        categories = []
        for data in categories_data:
            category, created = DigitalServiceCategory.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        return categories

    def create_services(self, categories):
        services_data = [
            # Identity & Documents
            {
                'name': 'National ID Card Renewal',
                'description': 'Renew your national ID card online with automatic document verification',
                'short_description': 'Quick and easy national ID renewal',
                'category': categories[0],
                'icon': 'fas fa-id-card',
                'color': 'primary',
                'difficulty': 'easy',
                'urgency': 'medium',
                'estimated_time': '5-10 minutes',
                'required_documents': 'Current ID card, recent photo',
                'fees': 'Free',
                'is_automated': True,
                'has_express_lane': True,
                'is_featured': True,
                'is_popular': True,
                'sort_order': 1
            },
            {
                'name': 'Passport Application',
                'description': 'Apply for a new passport or renew existing passport with online document submission',
                'short_description': 'Complete passport application process',
                'category': categories[0],
                'icon': 'fas fa-passport',
                'color': 'primary',
                'difficulty': 'medium',
                'urgency': 'high',
                'estimated_time': '15-20 minutes',
                'required_documents': 'National ID, birth certificate, recent photos, travel documents',
                'fees': 'Varies by type',
                'is_automated': False,
                'has_express_lane': True,
                'is_featured': True,
                'sort_order': 2
            },
            {
                'name': 'Birth Certificate',
                'description': 'Request birth certificate with online verification and digital delivery',
                'short_description': 'Get your birth certificate online',
                'category': categories[0],
                'icon': 'fas fa-baby',
                'color': 'primary',
                'difficulty': 'easy',
                'urgency': 'low',
                'estimated_time': '5-8 minutes',
                'required_documents': 'Parent ID, hospital records',
                'fees': 'Minimal fee',
                'is_automated': True,
                'has_express_lane': False,
                'sort_order': 3
            },
            
            # Business & Entrepreneurship
            {
                'name': 'Business Registration',
                'description': 'Register your new business with automatic tax ID assignment and business license',
                'short_description': 'Start your business journey',
                'category': categories[1],
                'icon': 'fas fa-building',
                'color': 'success',
                'difficulty': 'medium',
                'urgency': 'high',
                'estimated_time': '20-30 minutes',
                'required_documents': 'Personal ID, business plan, address proof',
                'fees': 'Registration fee',
                'is_automated': False,
                'has_express_lane': True,
                'is_featured': True,
                'is_popular': True,
                'sort_order': 1
            },
            {
                'name': 'Tax Registration',
                'description': 'Register for tax purposes and get your tax identification number',
                'short_description': 'Get your tax ID quickly',
                'category': categories[1],
                'icon': 'fas fa-calculator',
                'color': 'success',
                'difficulty': 'easy',
                'urgency': 'medium',
                'estimated_time': '10-15 minutes',
                'required_documents': 'Business registration, personal ID',
                'fees': 'Free',
                'is_automated': True,
                'has_express_lane': True,
                'sort_order': 2
            },
            
            # Education & Training
            {
                'name': 'Student Certificate',
                'description': 'Request official student certificates and academic records',
                'short_description': 'Get your academic certificates',
                'category': categories[2],
                'icon': 'fas fa-certificate',
                'color': 'info',
                'difficulty': 'easy',
                'urgency': 'medium',
                'estimated_time': '8-12 minutes',
                'required_documents': 'Student ID, enrollment proof',
                'fees': 'Processing fee',
                'is_automated': True,
                'has_express_lane': False,
                'is_popular': True,
                'sort_order': 1
            },
            
            # Health & Medical
            {
                'name': 'Health Insurance Registration',
                'description': 'Register for national health insurance with automatic eligibility verification',
                'short_description': 'Get health coverage online',
                'category': categories[3],
                'icon': 'fas fa-shield-alt',
                'color': 'danger',
                'difficulty': 'medium',
                'urgency': 'high',
                'estimated_time': '15-20 minutes',
                'required_documents': 'National ID, employment proof, family information',
                'fees': 'Monthly premium',
                'is_automated': False,
                'has_express_lane': True,
                'is_featured': True,
                'sort_order': 1
            },
            
            # Transportation & Travel
            {
                'name': 'Driver License Renewal',
                'description': 'Renew your driver license with online testing and automatic renewal',
                'short_description': 'Renew your driver license',
                'category': categories[4],
                'icon': 'fas fa-car',
                'color': 'warning',
                'difficulty': 'medium',
                'urgency': 'medium',
                'estimated_time': '15-25 minutes',
                'required_documents': 'Current license, medical certificate, recent photo',
                'fees': 'Renewal fee',
                'is_automated': False,
                'has_express_lane': True,
                'is_popular': True,
                'sort_order': 1
            },
            {
                'name': 'Vehicle Registration',
                'description': 'Register your vehicle and get license plates with online verification',
                'short_description': 'Register your vehicle online',
                'category': categories[4],
                'icon': 'fas fa-truck',
                'color': 'warning',
                'difficulty': 'medium',
                'urgency': 'high',
                'estimated_time': '20-30 minutes',
                'required_documents': 'Vehicle documents, insurance, personal ID',
                'fees': 'Registration fee',
                'is_automated': False,
                'has_express_lane': True,
                'sort_order': 2
            },
            
            # Property & Real Estate
            {
                'name': 'Property Registration',
                'description': 'Register your property and get official ownership documents',
                'short_description': 'Register your property',
                'category': categories[5],
                'icon': 'fas fa-home',
                'color': 'secondary',
                'difficulty': 'hard',
                'urgency': 'medium',
                'estimated_time': '30-45 minutes',
                'required_documents': 'Property documents, survey reports, personal ID',
                'fees': 'Registration fee',
                'is_automated': False,
                'has_express_lane': False,
                'sort_order': 1
            },
            
            # Financial Services
            {
                'name': 'Tax Payment',
                'description': 'Pay your taxes online with multiple payment options and automatic receipt',
                'short_description': 'Pay taxes online easily',
                'category': categories[6],
                'icon': 'fas fa-credit-card',
                'color': 'dark',
                'difficulty': 'easy',
                'urgency': 'high',
                'estimated_time': '5-10 minutes',
                'required_documents': 'Tax ID, payment method',
                'fees': 'Tax amount',
                'is_automated': True,
                'has_express_lane': True,
                'is_featured': True,
                'is_popular': True,
                'sort_order': 1
            },
            
            # Social Services
            {
                'name': 'Social Security Registration',
                'description': 'Register for social security benefits and get your social security number',
                'short_description': 'Get social security benefits',
                'category': categories[7],
                'icon': 'fas fa-hands-helping',
                'color': 'primary',
                'difficulty': 'medium',
                'urgency': 'medium',
                'estimated_time': '15-20 minutes',
                'required_documents': 'National ID, employment history, family information',
                'fees': 'Free',
                'is_automated': False,
                'has_express_lane': True,
                'sort_order': 1
            }
        ]
        
        services = []
        for data in services_data:
            service, created = DigitalService.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            services.append(service)
            if created:
                self.stdout.write(f'Created service: {service.name}')
        
        return services

    def create_life_events(self, services):
        life_events_data = [
            {
                'name': 'Getting Married',
                'description': 'Essential services for newlyweds including name changes, joint accounts, and family registration',
                'icon': 'fas fa-heart',
                'color': 'danger',
                'services': [services[0], services[1], services[8]],  # ID renewal, passport, social security
                'sort_order': 1
            },
            {
                'name': 'Starting a Business',
                'description': 'Complete business setup including registration, tax ID, and necessary permits',
                'icon': 'fas fa-rocket',
                'color': 'success',
                'services': [services[3], services[4]],  # Business registration, tax registration
                'sort_order': 2
            },
            {
                'name': 'Moving to a New Home',
                'description': 'Update your address, transfer utilities, and register your new property',
                'icon': 'fas fa-truck',
                'color': 'secondary',
                'services': [services[0], services[8], services[9]],  # ID renewal, property registration, social security
                'sort_order': 3
            },
            {
                'name': 'Having a Baby',
                'description': 'Register your newborn, get birth certificate, and update family records',
                'icon': 'fas fa-baby',
                'color': 'info',
                'services': [services[2], services[6]],  # Birth certificate, health insurance
                'sort_order': 4
            },
            {
                'name': 'Starting University',
                'description': 'Student services, certificates, and academic registration',
                'icon': 'fas fa-graduation-cap',
                'color': 'info',
                'services': [services[5]],  # Student certificate
                'sort_order': 5
            },
            {
                'name': 'Buying a Car',
                'description': 'Vehicle registration, insurance, and driver license services',
                'icon': 'fas fa-car',
                'color': 'warning',
                'services': [services[7], services[8]],  # Driver license, vehicle registration
                'sort_order': 6
            }
        ]
        
        life_events = []
        for data in life_events_data:
            life_event, created = LifeEvent.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'icon': data['icon'],
                    'color': data['color'],
                    'sort_order': data['sort_order']
                }
            )
            if created:
                life_event.services.set(data['services'])
                life_events.append(life_event)
                self.stdout.write(f'Created life event: {life_event.name}')
        
        return life_events

    def create_quick_actions(self, services):
        quick_actions_data = [
            {
                'name': 'Renew ID',
                'description': 'Quick ID card renewal',
                'icon': 'fas fa-id-card',
                'color': 'primary',
                'service': services[0],
                'sort_order': 1
            },
            {
                'name': 'Pay Taxes',
                'description': 'Pay taxes online',
                'icon': 'fas fa-credit-card',
                'color': 'dark',
                'service': services[10],
                'sort_order': 2
            },
            {
                'name': 'Register Business',
                'description': 'Start your business',
                'icon': 'fas fa-building',
                'color': 'success',
                'service': services[3],
                'sort_order': 3
            },
            {
                'name': 'Health Insurance',
                'description': 'Get health coverage',
                'icon': 'fas fa-shield-alt',
                'color': 'danger',
                'service': services[6],
                'sort_order': 4
            },
            {
                'name': 'Driver License',
                'description': 'Renew driver license',
                'icon': 'fas fa-car',
                'color': 'warning',
                'service': services[7],
                'sort_order': 5
            },
            {
                'name': 'Birth Certificate',
                'description': 'Get birth certificate',
                'icon': 'fas fa-baby',
                'color': 'primary',
                'service': services[2],
                'sort_order': 6
            }
        ]
        
        quick_actions = []
        for data in quick_actions_data:
            quick_action, created = QuickAction.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'icon': data['icon'],
                    'color': data['color'],
                    'service': data['service'],
                    'sort_order': data['sort_order']
                }
            )
            quick_actions.append(quick_action)
            if created:
                self.stdout.write(f'Created quick action: {quick_action.name}')
        
        return quick_actions

    def create_service_steps(self, services):
        # Create steps for a few key services
        steps_data = {
            services[0]: [  # National ID Card Renewal
                {'title': 'Verify Identity', 'description': 'Enter your current ID number and verify your identity', 'step_number': 1, 'estimated_time': 2},
                {'title': 'Upload Documents', 'description': 'Upload required documents including recent photo', 'step_number': 2, 'estimated_time': 3},
                {'title': 'Review Information', 'description': 'Review all information before submission', 'step_number': 3, 'estimated_time': 2},
                {'title': 'Submit Request', 'description': 'Submit your renewal request for processing', 'step_number': 4, 'estimated_time': 1},
            ],
            services[3]: [  # Business Registration
                {'title': 'Business Information', 'description': 'Enter your business details and type', 'step_number': 1, 'estimated_time': 5},
                {'title': 'Owner Information', 'description': 'Provide owner and partner information', 'step_number': 2, 'estimated_time': 5},
                {'title': 'Business Address', 'description': 'Enter business address and contact information', 'step_number': 3, 'estimated_time': 3},
                {'title': 'Upload Documents', 'description': 'Upload required business documents', 'step_number': 4, 'estimated_time': 5},
                {'title': 'Review & Submit', 'description': 'Review all information and submit application', 'step_number': 5, 'estimated_time': 2},
            ],
            services[10]: [  # Tax Payment
                {'title': 'Select Tax Type', 'description': 'Choose the type of tax you want to pay', 'step_number': 1, 'estimated_time': 1},
                {'title': 'Enter Amount', 'description': 'Enter the tax amount to be paid', 'step_number': 2, 'estimated_time': 2},
                {'title': 'Choose Payment Method', 'description': 'Select your preferred payment method', 'step_number': 3, 'estimated_time': 2},
                {'title': 'Complete Payment', 'description': 'Complete the payment and get receipt', 'step_number': 4, 'estimated_time': 3},
            ]
        }
        
        for service, steps in steps_data.items():
            for step_data in steps:
                step, created = ServiceStep.objects.get_or_create(
                    service=service,
                    step_number=step_data['step_number'],
                    defaults=step_data
                )
                if created:
                    self.stdout.write(f'Created step {step.step_number} for {service.name}')

    def create_notifications(self, services):
        notifications_data = [
            {
                'service': services[0],
                'title': 'ID Renewal Deadline',
                'message': 'Your national ID card expires in 30 days. Renew now to avoid delays.',
                'notification_type': 'reminder',
                'icon': 'fas fa-clock',
                'color': 'warning',
                'is_urgent': True,
                'start_date': timezone.now()
            },
            {
                'service': services[10],
                'title': 'Tax Payment Due',
                'message': 'Your quarterly tax payment is due this month. Pay online for convenience.',
                'notification_type': 'deadline',
                'icon': 'fas fa-calendar',
                'color': 'danger',
                'is_urgent': True,
                'start_date': timezone.now()
            },
            {
                'service': services[3],
                'title': 'New Business Features',
                'message': 'We\'ve added new features to make business registration even easier!',
                'notification_type': 'update',
                'icon': 'fas fa-star',
                'color': 'info',
                'is_urgent': False,
                'start_date': timezone.now()
            }
        ]
        
        for data in notifications_data:
            notification, created = ServiceNotification.objects.get_or_create(
                service=data['service'],
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created notification: {notification.title}') 