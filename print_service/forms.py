# ✅ forms.py (کامل، شامل فرم‌های قبلی + فرم جدید مدیریت)

from django import forms
from .models import PrintOrder, UploadedFile

class PrintOrderForm(forms.ModelForm):
    class Meta:
        model = PrintOrder
        fields = [
            'name', 'email', 'phone', 'color_mode', 'side_type', 
            'paper_size', 'num_copies', 'delivery_method', 'address', 'payment_method'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'color_mode': forms.Select(attrs={'class': 'form-control'}),
            'side_type': forms.Select(attrs={'class': 'form-control'}),
            'paper_size': forms.Select(attrs={'class': 'form-control'}),
            'num_copies': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'delivery_method': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Delivery address (if delivery selected)'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

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

class PrintOrderSlipForm(forms.ModelForm):
    class Meta:
        model = PrintOrder
        fields = ['payment_slip']
        widgets = {
            'payment_slip': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': True
            })
        }

    def clean_payment_slip(self):
        slip = self.cleaned_data.get('payment_slip')
        if slip:
            if slip.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5MB")
            import os
            ext = os.path.splitext(slip.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Only image files are allowed (JPG, PNG)")
        return slip

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