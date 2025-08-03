from django import forms
from django.utils.translation import gettext_lazy as _
from .models import UserServiceRequest, ServiceReview, DigitalService, DigitalServiceCategory, UserProfile

class ServiceRequestForm(forms.ModelForm):
    """Enhanced form for service requests"""
    class Meta:
        model = UserServiceRequest
        fields = ['title', 'description', 'contact_phone', 'contact_email', 'documents', 'additional_files']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter a descriptive title for your request')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Describe your request in detail...')
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your contact phone number')
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your contact email address')
            }),
            'documents': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            }),
            'additional_files': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            })
        }

class ServiceReviewForm(forms.ModelForm):
    """Enhanced form for service reviews"""
    class Meta:
        model = ServiceReview
        fields = ['rating', 'comment', 'ease_of_use', 'speed', 'helpfulness']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Share your experience with this service...')
            }),
            'ease_of_use': forms.Select(attrs={'class': 'form-control'}),
            'speed': forms.Select(attrs={'class': 'form-control'}),
            'helpfulness': forms.Select(attrs={'class': 'form-control'})
        }

class ServiceSearchForm(forms.Form):
    """Enhanced search form for services"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search for services...')
        })
    )
    category = forms.ModelChoiceField(
        queryset=DigitalServiceCategory.objects.filter(is_active=True),
        required=False,
        empty_label=_('All Categories'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    difficulty = forms.ChoiceField(
        choices=[('', _('All Difficulties'))] + DigitalService.DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', _('All Statuses'))] + DigitalService.SERVICE_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ServiceFilterForm(forms.Form):
    """Advanced filter form for services"""
    featured_only = forms.BooleanField(
        required=False,
        label=_('Featured Only'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    popular_only = forms.BooleanField(
        required=False,
        label=_('Popular Only'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    new_only = forms.BooleanField(
        required=False,
        label=_('New Services Only'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    automated_only = forms.BooleanField(
        required=False,
        label=_('Automated Services Only'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    express_lane_only = forms.BooleanField(
        required=False,
        label=_('Express Lane Available'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('', _('Default')),
            ('name', _('Name A-Z')),
            ('-name', _('Name Z-A')),
            ('-view_count', _('Most Popular')),
            ('-created_at', _('Newest First')),
            ('sort_order', _('Sort Order')),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ContactForm(forms.Form):
    """Enhanced contact form"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your full name')
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your email address')
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your phone number (optional)')
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Subject of your message')
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': _('Your message...')
        })
    )
    service_category = forms.ModelChoiceField(
        queryset=DigitalServiceCategory.objects.filter(is_active=True),
        required=False,
        empty_label=_('Select a service category (optional)'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ServiceFeedbackForm(forms.Form):
    """Enhanced feedback form"""
    FEEDBACK_TYPES = [
        ('general', _('General Feedback')),
        ('bug_report', _('Bug Report')),
        ('feature_request', _('Feature Request')),
        ('service_improvement', _('Service Improvement')),
        ('user_experience', _('User Experience')),
    ]
    
    feedback_type = forms.ChoiceField(
        choices=FEEDBACK_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your name (optional)')
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your email (optional)')
        })
    )
    service = forms.ModelChoiceField(
        queryset=DigitalService.objects.filter(status='active'),
        required=False,
        empty_label=_('Select a service (optional)'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    rating = forms.ChoiceField(
        choices=[('', _('Select rating'))] + [(str(i), f'{i} Stars') for i in range(1, 6)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': _('Please share your feedback...')
        })
    )
    allow_contact = forms.BooleanField(
        required=False,
        label=_('Allow us to contact you for follow-up'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class UserProfileForm(forms.ModelForm):
    """Form for user profile updates"""
    class Meta:
        model = UserProfile
        fields = ['national_id', 'phone_number', 'address', 'city', 'postal_code', 'preferred_language']
        widgets = {
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your national ID number')
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your phone number')
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Your full address')
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your city')
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your postal code')
            }),
            'preferred_language': forms.Select(attrs={'class': 'form-control'})
        } 