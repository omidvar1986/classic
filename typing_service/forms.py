# typing_service/forms.py

from django import forms
from .models import TypingOrder
from django.utils.translation import gettext_lazy as _
import os
from .models import TypingPriceSettings


class TypingOrderForm(forms.ModelForm):
    """Form for users to submit a new typing order for review."""
    class Meta:
        model = TypingOrder
        fields = ['user_name', 'user_email', 'user_phone', 'description', 'document_file']
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('e.g., John Doe')}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('e.g., john.doe@example.com')}),
            'user_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('e.g., 09123456789')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Please provide any details about your document, such as formatting requirements.')}),
            'document_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_upload_file(self):
        file = self.cleaned_data.get('upload_file')
        if file:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("حداکثر اندازه فایل ۱۰ مگابایت است.")
            allowed_extensions = ['.doc', '.docx', '.pdf', '.txt']
            import os
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError("فرمت فایل مجاز نیست. فقط .doc, .docx, .pdf, .txt")
        return file


class TypingOrderStatusForm(forms.ModelForm):
    class Meta:
        model = TypingOrder
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }


class PaymentSlipForm(forms.ModelForm):
    """Form for users to upload their payment slip."""
    class Meta:
        model = TypingOrder
        fields = ['payment_slip']
        widgets = {
            'payment_slip': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': True}),
        }

    def clean_payment_slip(self):
        slip = self.cleaned_data.get('payment_slip')
        if not slip:
            raise forms.ValidationError(_("This field is required."))
        # Add any other validation like file size or type if needed
        return slip


class TypingPriceSettingsForm(forms.ModelForm):
    """Form for admin to update the price per page for typing services."""
    class Meta:
        model = TypingPriceSettings
        fields = ['price_per_page']
        widgets = {
            'price_per_page': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'price_per_page': _('Set Price Per Page (Toman)')
        }


# Final approval form
class FinalApprovalForm(forms.ModelForm):
    class Meta:
        model = TypingOrder
        fields = ['final_note']
        widgets = {
            'final_note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your final note...'})
        }