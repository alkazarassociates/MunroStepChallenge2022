"""msc_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import django.contrib.auth
from django.urls import include, path
from django.views.generic import TemplateView
from steps.views import Register, peaker_modification

urlpatterns = [
    path('steps/', include('steps.urls')),
    path('admin/', admin.site.urls),
    path('register/success/', TemplateView.as_view(template_name='registration/success.html'), name='register-success'),
    path('register/', Register.as_view(), name='peaker_register'),
    path('peaker/', peaker_modification, name='peaker'),
    path('', include('django.contrib.auth.urls')),
    path('', include('landing.urls')),
    path('teams', include('teams.urls')),
    path('groups/', include('mpc_groups.urls')),
    path('faq/', include('faq_page.urls')),
    path('contact', include('contact.urls')),
    path('change-password', django.contrib.auth.views.PasswordChangeView.as_view(), name='change-password'),
]
