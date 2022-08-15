from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z7zy3y-od5m8gvw2+gh-&4xr-i+ppo^mm6ehq5mtz7lb#cq9fb'

ALLOWED_HOSTS = ['test.alkazarassociates.com', '127.0.0.1']

# Use test database
DATABASES['default']['NAME'] = 'django_test'


print("Development Settings")
