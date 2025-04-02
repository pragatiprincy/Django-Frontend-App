import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
application = get_wsgi_application()

# Django Project Structure
# project/
# ├── project/
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   ├── wsgi.py
# ├── app/
# │   ├── __init__.py
# │   ├── views.py
# │   ├── urls.py
# │   ├── models.py
# │   ├── forms.py
# │   ├── templates/
# │   │   ├── base.html
# │   │   ├── home.html
# │   │   ├── login.html
# │   │   ├── category.html
# │   │   ├── products.html
# │   ├── static/
# │   │   ├── css/
# │   │   │   ├── styles.css
# │   │   ├── js/
# │   │   │   ├── scripts.js
# │   │   ├── images/
# ├── manage.py

# settings.py (Basic Setup for Django Project)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# urls.py (Setting up URL Routing)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]

# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('category/', views.category, name='category'),
    path('products/<str:category>/', views.products, name='products'),
    path('logout/', views.logout_view, name='logout'),
]

# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import LoginForm, SignupForm

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('category')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def category(request):
    return render(request, 'category.html')

def products(request, category):
    products_data = {
        'Men': ['Shirt', 'Pants', 'Shoes'],
        'Women': ['Dress', 'Handbag', 'Sandals']
    }
    return JsonResponse({'products': products_data.get(category, [])})

# static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('men-btn').addEventListener('click', function() {
        loadProducts('Men');
    });
    document.getElementById('women-btn').addEventListener('click', function() {
        loadProducts('Women');
    });
});

function loadProducts(category) {
    fetch(`/products/${category}/`)
        .then(response => response.json())
        .then(data => {
            const productsContainer = document.getElementById('products-container');
            productsContainer.innerHTML = '';
            data.products.forEach(product => {
                let productElement = document.createElement('div');
                productElement.className = 'product-item';
                productElement.textContent = product;
                productsContainer.appendChild(productElement);
            });
        })
        .catch(error => console.error('Error fetching products:', error));
}

# README.md
# Django Multi-Page Frontend App

## Overview
This is a Django-based multi-page frontend application implementing category selection and AJAX-based product loading.

## Features
- AJAX optimization for fast loading
- Responsive design for all devices
- Smooth UI transitions

## Installation
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Usage
1. Open `http://127.0.0.1:8000/`
2. Navigate through the login/signup and category selection
3. Enjoy smooth product loading!

# requirements.txt
django
