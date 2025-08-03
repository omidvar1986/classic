from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
# DEPRECATED: This setup script is for the old government services models and is no longer used.
# from government_services.models import ServiceCategory, GovernmentService, ServiceGuide, ServiceFAQ

# This script is deprecated. Use setup_digital_life_assistant.py instead.

class Command(BaseCommand):
    help = 'Setup initial government services data'

    def handle(self, *args, **options):
        self.stdout.write('Creating government service categories...')
        
        # Create categories
        categories = {
            'subsidies': {
                'name': _('Subsidies & Financial Services'),
                'description': _('Government subsidies, financial assistance, and economic support services'),
                'icon': 'fas fa-hand-holding-usd',
                'color': 'success',
                'sort_order': 1,
            },
            'transportation': {
                'name': _('Transportation & Vehicles'),
                'description': _('Vehicle registration, driving licenses, and transportation services'),
                'icon': 'fas fa-car',
                'color': 'primary',
                'sort_order': 2,
            },
            'legal': {
                'name': _('Legal & Judiciary'),
                'description': _('Legal services, court matters, and judicial procedures'),
                'icon': 'fas fa-gavel',
                'color': 'warning',
                'sort_order': 3,
            },
            'police': {
                'name': _('Police & Security'),
                'description': _('Police services, passports, and security-related procedures'),
                'icon': 'fas fa-shield-alt',
                'color': 'info',
                'sort_order': 4,
            },
            'postal': {
                'name': _('Postal & Address Services'),
                'description': _('Postal services, address changes, and mail-related services'),
                'icon': 'fas fa-mail-bulk',
                'color': 'secondary',
                'sort_order': 5,
            },
            'insurance': {
                'name': _('Insurance & Social Security'),
                'description': _('Insurance services, social security, and employment benefits'),
                'icon': 'fas fa-umbrella',
                'color': 'dark',
                'sort_order': 6,
            },
            'education': {
                'name': _('Education & University'),
                'description': _('Educational services, university admissions, and academic procedures'),
                'icon': 'fas fa-graduation-cap',
                'color': 'danger',
                'sort_order': 7,
            },
            'identity': {
                'name': _('Identity & Civil Registry'),
                'description': _('National ID services, birth certificates, and civil registration'),
                'icon': 'fas fa-id-card',
                'color': 'primary',
                'sort_order': 8,
            },
        }
        
        created_categories = {}
        for key, data in categories.items():
            category, created = ServiceCategory.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            created_categories[key] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        self.stdout.write('Creating government services...')
        
        # Define services
        services_data = [
            {
                'name': _('Subsidy Registration (Yaraneh)'),
                'description': _('Register for government subsidies and financial assistance. This service allows citizens to apply for various government subsidies including housing, food, and other essential needs.'),
                'category': 'subsidies',
                'official_website': 'https://hemayat.mcls.gov.ir',
                'difficulty': 'easy',
                'estimated_time': _('15-30 minutes'),
                'required_documents': _('National ID, Bank account information, Proof of income'),
                'fees': _('Free'),
                'is_featured': True,
                'is_popular': True,
                'sort_order': 1,
            },
            {
                'name': _('Car Purchase (Iran Khodro)'),
                'description': _('Participate in the lottery system for purchasing cars from Iran Khodro. This service manages the allocation of vehicles through a fair lottery system.'),
                'category': 'transportation',
                'official_website': 'https://esale.ikco.ir',
                'difficulty': 'medium',
                'estimated_time': _('30-45 minutes'),
                'required_documents': _('National ID, Driver\'s license, Proof of residence'),
                'fees': _('Registration fee may apply'),
                'is_featured': True,
                'is_popular': True,
                'sort_order': 2,
            },
            {
                'name': _('Judiciary Portal (Sana)'),
                'description': _('Access legal services and court notices through the official judiciary portal. Handle legal matters, view court schedules, and access legal documents.'),
                'category': 'legal',
                'official_website': 'https://sana.adliran.ir',
                'difficulty': 'medium',
                'estimated_time': _('20-40 minutes'),
                'required_documents': _('National ID, Case number (if applicable)'),
                'fees': _('Varies by service'),
                'is_featured': False,
                'is_popular': True,
                'sort_order': 3,
            },
            {
                'name': _('Police Services (Sakha)'),
                'description': _('Access various police services including passport applications, military service information, and driving license services.'),
                'category': 'police',
                'official_website': 'https://sakhapolice.ir',
                'difficulty': 'medium',
                'estimated_time': _('25-50 minutes'),
                'required_documents': _('National ID, Previous documents (if applicable)'),
                'fees': _('Service fees apply'),
                'is_featured': True,
                'is_popular': True,
                'sort_order': 4,
            },
            {
                'name': _('Change of Address / Post Services'),
                'description': _('Update your official address and access postal services. This service allows you to change your registered address and manage postal deliveries.'),
                'category': 'postal',
                'official_website': 'https://post.ir',
                'difficulty': 'easy',
                'estimated_time': _('10-20 minutes'),
                'required_documents': _('National ID, Proof of new address'),
                'fees': _('Minimal fee'),
                'is_featured': False,
                'is_popular': False,
                'sort_order': 5,
            },
            {
                'name': _('E-Bimeh (Insurance)'),
                'description': _('Check and manage your insurance information online. Access insurance policies, claims, and coverage details.'),
                'category': 'insurance',
                'official_website': 'https://bimeh.ir',
                'difficulty': 'easy',
                'estimated_time': _('15-25 minutes'),
                'required_documents': _('National ID, Insurance policy number'),
                'fees': _('Free'),
                'is_featured': False,
                'is_popular': True,
                'sort_order': 6,
            },
            {
                'name': _('Social Security (Tamin Ejtemaei)'),
                'description': _('Access retirement and employment insurance services. Manage your social security benefits and employment insurance.'),
                'category': 'insurance',
                'official_website': 'https://eservices.tamin.ir',
                'difficulty': 'medium',
                'estimated_time': _('20-35 minutes'),
                'required_documents': _('National ID, Employment information'),
                'fees': _('Based on employment status'),
                'is_featured': True,
                'is_popular': True,
                'sort_order': 7,
            },
            {
                'name': _('University Portal (Sanjesh)'),
                'description': _('Access university entrance exams and educational services. Register for university entrance exams and manage educational records.'),
                'category': 'education',
                'official_website': 'https://sanjesh.org',
                'difficulty': 'hard',
                'estimated_time': _('45-60 minutes'),
                'required_documents': _('National ID, Educational certificates, Photo'),
                'fees': _('Exam registration fees'),
                'is_featured': True,
                'is_popular': True,
                'sort_order': 8,
            },
            {
                'name': _('National ID Services (Nadraaj)'),
                'description': _('Correct personal information and manage national ID services. Update personal details and access ID-related services.'),
                'category': 'identity',
                'official_website': 'https://nid.bmi.ir',
                'difficulty': 'medium',
                'estimated_time': _('30-45 minutes'),
                'required_documents': _('Current National ID, Supporting documents'),
                'fees': _('Service fees apply'),
                'is_featured': False,
                'is_popular': True,
                'sort_order': 9,
            },
            {
                'name': _('Civil Registry (Sabte Ahval)'),
                'description': _('Register births, deaths, and marriages. Access civil registry services for official documentation.'),
                'category': 'identity',
                'official_website': 'https://sabteahval.ir',
                'difficulty': 'medium',
                'estimated_time': _('25-40 minutes'),
                'required_documents': _('National ID, Supporting documents for registration'),
                'fees': _('Registration fees'),
                'is_featured': False,
                'is_popular': False,
                'sort_order': 10,
            },
        ]
        
        for service_data in services_data:
            category = created_categories[service_data['category']]
            service, created = GovernmentService.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'description': service_data['description'],
                    'category': category,
                    'official_website': service_data['official_website'],
                    'difficulty': service_data['difficulty'],
                    'estimated_time': service_data['estimated_time'],
                    'required_documents': service_data['required_documents'],
                    'fees': service_data['fees'],
                    'is_featured': service_data['is_featured'],
                    'is_popular': service_data['is_popular'],
                    'sort_order': service_data['sort_order'],
                }
            )
            if created:
                self.stdout.write(f'Created service: {service.name}')
        
        self.stdout.write('Creating sample guides and FAQs...')
        
        # Create sample guides for subsidy registration
        subsidy_service = GovernmentService.objects.get(name__icontains='Subsidy')
        guides_data = [
            {
                'title': _('Step 1: Prepare Required Documents'),
                'content': _('Gather your National ID, bank account information, and proof of income. Make sure all documents are current and valid.'),
                'step_number': 1,
            },
            {
                'title': _('Step 2: Visit the Official Website'),
                'content': _('Go to hemayat.mcls.gov.ir and click on the registration link. Create an account if you don\'t have one.'),
                'step_number': 2,
            },
            {
                'title': _('Step 3: Fill Out the Application'),
                'content': _('Complete the online application form with your personal and financial information. Double-check all entries for accuracy.'),
                'step_number': 3,
            },
            {
                'title': _('Step 4: Submit and Track'),
                'content': _('Submit your application and note your reference number. You can track the status of your application online.'),
                'step_number': 4,
            },
        ]
        
        for guide_data in guides_data:
            guide, created = ServiceGuide.objects.get_or_create(
                service=subsidy_service,
                step_number=guide_data['step_number'],
                defaults=guide_data
            )
            if created:
                self.stdout.write(f'Created guide: {guide.title}')
        
        # Create sample FAQs
        faqs_data = [
            {
                'question': _('What documents do I need for subsidy registration?'),
                'answer': _('You need your National ID, bank account information, and proof of income. Additional documents may be required based on your specific situation.'),
                'sort_order': 1,
            },
            {
                'question': _('How long does the registration process take?'),
                'answer': _('The online registration typically takes 15-30 minutes. Processing time for approval varies and can take several days to weeks.'),
                'sort_order': 2,
            },
            {
                'question': _('Can I register for multiple subsidies?'),
                'answer': _('Yes, you can register for multiple types of subsidies if you qualify. Each subsidy may have different eligibility criteria.'),
                'sort_order': 3,
            },
            {
                'question': _('How do I check my application status?'),
                'answer': _('You can check your application status online using your reference number or by logging into your account on the official website.'),
                'sort_order': 4,
            },
        ]
        
        for faq_data in faqs_data:
            faq, created = ServiceFAQ.objects.get_or_create(
                service=subsidy_service,
                question=faq_data['question'],
                defaults=faq_data
            )
            if created:
                self.stdout.write(f'Created FAQ: {faq.question}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created government services data!')
        ) 