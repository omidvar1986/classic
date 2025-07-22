from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import translation
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    """Main landing page for Smart Office"""
    return render(request, 'core/home.html')

def redirect_to_print_service(request):
    """Redirect root URL to print service"""
    return redirect('print_service:order_create')

def change_language(request):
    """Change language and redirect back"""
    if request.method == 'GET':
        lang = request.GET.get('lang')
        if lang in ['en', 'fa']:
            translation.activate(lang)
            request.session['django_language'] = lang
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            response.set_cookie('django_language', lang)
            return response
    return redirect('core:home')
