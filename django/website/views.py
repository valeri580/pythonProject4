from django.shortcuts import render
from datetime import datetime

def home(request):
    """Главная страница сайта"""
    context = {
        'current_year': datetime.now().year,
    }
    return render(request, 'website/home.html', context)

def about(request):
    """Страница О нас"""
    context = {
        'current_year': datetime.now().year,
    }
    return render(request, 'website/about.html', context)

def services(request):
    """Страница Услуги"""
    context = {
        'current_year': datetime.now().year,
    }
    return render(request, 'website/services.html', context)

def contact(request):
    """Страница Контакты"""
    context = {
        'current_year': datetime.now().year,
    }
    return render(request, 'website/contact.html', context)
