from django import forms

class PaymentSlipUploadForm(forms.Form):
    payment_slip = forms.ImageField(label="Upload Payment Slip") 