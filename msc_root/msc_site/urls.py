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
from django.conf import settings
from django.contrib import admin
import django.contrib.auth
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from steps.views import Register, peaker_modification, activate

urlpatterns = [
    path('steps/', include('steps.urls')),
    path('admin/', admin.site.urls),
    path('register/success/', TemplateView.as_view(template_name='registration/success.html', extra_context={'phase': settings.CURRENT_PHASE}), name='register-success'),
    path('register/', Register.as_view(extra_context={'phase': settings.CURRENT_PHASE}), name='peaker_register'),
    path('peaker/', peaker_modification, name='peaker'),
    # This line needs to be above the django.contrib.auth.urls one to catch the ones we want to give extra info to.
    path('login/', auth_views.LoginView.as_view(extra_context={'phase': settings.CURRENT_PHASE})),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/',  
        activate, name='activate'),
    path('account/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html', 
        extra_context={'phase': settings.CURRENT_PHASE},
        from_email=settings.EMAIL_OUR_ADDRESS), name='password-reset'),
    path('', include('django.contrib.auth.urls')),
    path('', include('landing.urls')),
    path('teams', include('teams.urls')),
    path('groups/', include('mpc_groups.urls')),
    path('faq/', include('faq_page.urls')),
    path('contact', include('contact.urls')),
    path('change-password', django.contrib.auth.views.PasswordChangeView.as_view(), name='change-password'),
]
