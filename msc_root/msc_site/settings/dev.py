from .base import *
import datetime

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z7zy3y-od5m8gvw2+gh-&4xr-i+ppo^mm6ehq5mtz7lb#cq9fb'

ALLOWED_HOSTS = ['test.alkazarassociates.com', '127.0.0.1', 'localhost']

# Use test database
DATABASES['default']['NAME'] = 'django_test'

CURRENT_PHASE.switch_to_test_server()
CURRENT_PHASE.challenge_start_date = datetime.date(2023, 8, 27)
CURRENT_PHASE.allow_step_entry = True

print("Development Settings. " + CURRENT_PHASE.Name())
