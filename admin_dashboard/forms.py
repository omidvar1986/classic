from django import forms
from django.utils.translation import gettext_lazy as _
from print_service.models import PrintPriceSettings, Accessory, PackageDeal, PaymentSettings
from typing_service.models import TypingPriceSettings

class PrintPriceSettingsForm(forms.ModelForm):
    """Form for managing print service pricing settings"""
    class Meta:
        model = PrintPriceSettings
        fields = ['base_price_per_page', 'color_price_multiplier', 'double_sided_discount']
        widgets = {
            'base_price_per_page': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1000',
                'step': '1000',
                'placeholder': '50000'
            }),
            'color_price_multiplier': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1.0',
                'max': '3.0',
                'step': '0.1',
                'placeholder': '1.5'
            }),
            'double_sided_discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.5',
                'max': '1.0',
                'step': '0.1',
                'placeholder': '0.8'
            }),
        }
        labels = {
            'base_price_per_page': _('Base Price Per Page (Tomans)'),
            'color_price_multiplier': _('Color Printing Multiplier'),
            'double_sided_discount': _('Double-Sided Discount'),
        }
        help_texts = {
            'base_price_per_page': _('Base price for black & white single-sided printing per page'),
            'color_price_multiplier': _('How much more expensive color printing is (1.5 = 50% more)'),
            'double_sided_discount': _('Discount for double-sided printing (0.8 = 20% discount)'),
        }

class TypingPriceSettingsForm(forms.ModelForm):
    """Form for managing typing service pricing settings"""
    class Meta:
        model = TypingPriceSettings
        fields = ['price_per_page']
        widgets = {
            'price_per_page': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1000',
                'step': '1000',
                'placeholder': '10000'
            }),
        }
        labels = {
            'price_per_page': _('Price Per Page (Tomans)'),
        }
        help_texts = {
            'price_per_page': _('Price per page for typing service'),
        }

class AccessoryForm(forms.ModelForm):
    """Form for creating/editing accessories"""
    class Meta:
        model = Accessory
        fields = ['name', 'description', 'base_price', 'category', 'service_type', 'is_active', 'icon', 'sort_order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., Premium Wire Binding')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Detailed description of the accessory')
            }),
            'base_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1000',
                'placeholder': '25000'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-star'
            }),
            'sort_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
        }
        labels = {
            'name': _('Accessory Name'),
            'description': _('Description'),
            'base_price': _('Base Price (Tomans)'),
            'category': _('Category'),
            'service_type': _('Service Type'),
            'is_active': _('Active'),
            'icon': _('Icon Class'),
            'sort_order': _('Sort Order'),
        }

class PackageDealForm(forms.ModelForm):
    """Form for creating/editing package deals"""
    class Meta:
        model = PackageDeal
        fields = ['name', 'description', 'discount_price', 'original_price', 'service_type', 'is_active', 'accessories']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., Professional Package')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('What is included in this package')
            }),
            'discount_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1000',
                'placeholder': '40000'
            }),
            'original_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1000',
                'placeholder': '45000'
            }),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'accessories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Package Name'),
            'description': _('Description'),
            'discount_price': _('Package Price (Tomans)'),
            'original_price': _('Original Price (Tomans)'),
            'service_type': _('Service Type'),
            'is_active': _('Active'),
            'accessories': _('Included Accessories'),
        }

class PaymentSettingsForm(forms.ModelForm):
    """Form for managing payment settings"""
    class Meta:
        model = PaymentSettings
        fields = ['bank_name', 'account_number', 'card_number', 'shaba_number']
        widgets = {
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., Bank Melli Iran')
            }),
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Account number')
            }),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Card number')
            }),
            'shaba_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Shaba number')
            }),
        }
        labels = {
            'bank_name': _('Bank Name'),
            'account_number': _('Account Number'),
            'card_number': _('Card Number'),
            'shaba_number': _('Shaba Number'),
        }

class AccessoryBulkEditForm(forms.Form):
    """Form for bulk editing accessories"""
    action = forms.ChoiceField(
        choices=[
            ('activate', _('Activate Selected')),
            ('deactivate', _('Deactivate Selected')),
            ('delete', _('Delete Selected')),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    accessories = forms.ModelMultipleChoiceField(
        queryset=Accessory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    ) 