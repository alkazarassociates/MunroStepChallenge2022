from .base import *

# Production settings
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = ['44.194.8.93', '.alkazarassociates.com']

SECURE_HSTS_SECONDS=3600
# SSL Redirects are handled by outer server.  Enabling here
# causes infinite redirect loop
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
    
STATIC_ROOT='/opt/bitnami/projects/TSC22/static'

print("Production Settings")
