# ✅ forms.py (کامل، شامل فرم‌های قبلی + فرم جدید مدیریت)

from django import forms
from .models import PrintOrder, UploadedFile, Accessory, PackageDeal
from .models import PaymentSettings

class PrintOrderForm(forms.ModelForm):
    # Accessories selection fields
    accessories = forms.ModelMultipleChoiceField(
        queryset=Accessory.objects.filter(service_type__in=['print', 'both'], is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Accessories & Finishing Options"
    )
    
    class Meta:
        model = PrintOrder
        fields = [
            'name', 'phone', 'color_mode', 'side_type', 
            'paper_size', 'num_copies', 'delivery_method', 'address', 'payment_method'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'color_mode': forms.Select(attrs={'class': 'form-control'}),
            'side_type': forms.Select(attrs={'class': 'form-control'}),
            'paper_size': forms.Select(attrs={'class': 'form-control'}),
            'num_copies': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'delivery_method': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Delivery address (if delivery selected)'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Group accessories by category
        accessories = Accessory.objects.filter(service_type__in=['print', 'both'], is_active=True)
        self.fields['accessories'].queryset = accessories
        
        # Add custom widget attributes for JavaScript
        self.fields['accessories'].widget.attrs.update({
            'class': 'accessory-checkboxes',
            'data-base-price': '5.00'  # Base price for print service
        })
    
    def get_accessories_by_category(self):
        """Group accessories by category for template rendering"""
        accessories = self.fields['accessories'].queryset
        categories = {}
        for accessory in accessories:
            if accessory.category not in categories:
                categories[accessory.category] = []
            categories[accessory.category].append(accessory)
        return categories

class AccessorySelectionForm(forms.Form):
    """Form for selecting accessories with quantity and pricing"""
    
    def __init__(self, service_type='print', *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get accessories for the service type
        accessories = Accessory.objects.filter(
            service_type__in=[service_type, 'both'], 
            is_active=True
        ).order_by('category', 'sort_order')
        
        # Group accessories by category
        categories = {}
        for accessory in accessories:
            if accessory.category not in categories:
                categories[accessory.category] = []
            categories[accessory.category].append(accessory)
        
        # Create form fields for each accessory
        for category, category_accessories in categories.items():
            for accessory in category_accessories:
                field_name = f'accessory_{accessory.id}'
                quantity_field_name = f'quantity_{accessory.id}'
                
                # Checkbox for accessory selection
                self.fields[field_name] = forms.BooleanField(
                    required=False,
                    label=accessory.name,
                    help_text=f"{accessory.description} (+${accessory.base_price})",
                    widget=forms.CheckboxInput(attrs={
                        'class': 'accessory-checkbox',
                        'data-accessory-id': accessory.id,
                        'data-price': str(accessory.base_price),
                        'data-category': accessory.category,
                        'data-icon': accessory.icon
                    })
                )
                
                # Quantity field for the accessory
                self.fields[quantity_field_name] = forms.IntegerField(
                    required=False,
                    min_value=1,
                    max_value=10,
                    initial=1,
                    widget=forms.NumberInput(attrs={
                        'class': 'accessory-quantity',
                        'data-accessory-id': accessory.id,
                        'style': 'display: none;'
                    })
                )

class PackageDealForm(forms.Form):
    """Form for package deals"""
    
    def __init__(self, service_type='print', *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get package deals for the service type
        package_deals = PackageDeal.objects.filter(
            service_type__in=[service_type, 'both'], 
            is_active=True
        )
        
        for deal in package_deals:
            field_name = f'package_{deal.id}'
            self.fields[field_name] = forms.BooleanField(
                required=False,
                label=deal.name,
                help_text=f"{deal.description} (Save ${deal.savings})",
                widget=forms.CheckboxInput(attrs={
                    'class': 'package-deal-checkbox',
                    'data-deal-id': deal.id,
                    'data-discount-price': str(deal.discount_price),
                    'data-original-price': str(deal.original_price),
                    'data-savings': str(deal.savings),
                    'data-accessories': ','.join([str(acc.id) for acc in deal.accessories.all()])
                })
            )

class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx'})
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 10MB")
            import os
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']:
                raise forms.ValidationError("Unsupported file format")
        return file

class AdminPaymentReviewForm(forms.ModelForm):
    payment_note = forms.CharField(
        label="Note (Optional)",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    class Meta:
        model = PrintOrder
        fields = ['payment_status', 'payment_note']
        widgets = {
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
        }

class PaymentSettingsForm(forms.ModelForm):
    class Meta:
        model = PaymentSettings
        fields = ['bank_name', 'account_number', 'card_number', 'shaba_number']
        widgets = {
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Bank Melli Iran'
            }),
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Account number (e.g., 1234567890)'
            }),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Card number (e.g., 6037-1234-5678-9012)'
            }),
            'shaba_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Shaba number (e.g., IR123456789012345678901234)'
            }),
        }
        labels = {
            'bank_name': 'Bank Name',
            'account_number': 'Account Number',
            'card_number': 'Card Number',
            'shaba_number': 'Shaba Number',
        }
        help_texts = {
            'bank_name': 'Enter the full name of the bank',
            'account_number': 'Enter the bank account number',
            'card_number': 'Enter the bank card number (can include dashes)',
            'shaba_number': 'Enter the IBAN/Shaba number',
        }

    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        if account_number:
            # Remove any non-digit characters
            account_number = ''.join(filter(str.isdigit, account_number))
            if len(account_number) < 8:
                raise forms.ValidationError("Account number must be at least 8 digits")
        return account_number

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if card_number:
            # Remove any non-digit characters
            card_number = ''.join(filter(str.isdigit, card_number))
            if len(card_number) < 13 or len(card_number) > 19:
                raise forms.ValidationError("Card number must be between 13 and 19 digits")
        return card_number

    def clean_shaba_number(self):
        shaba_number = self.cleaned_data.get('shaba_number')
        if shaba_number:
            # Remove spaces and convert to uppercase
            shaba_number = shaba_number.replace(' ', '').upper()
            if not shaba_number.startswith('IR'):
                raise forms.ValidationError("Shaba number must start with 'IR'")
            if len(shaba_number) != 26:
                raise forms.ValidationError("Shaba number must be exactly 26 characters")
        return shaba_number