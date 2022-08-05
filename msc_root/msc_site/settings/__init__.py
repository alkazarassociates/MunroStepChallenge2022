import os
if 'DJANGO_SETTINGS_MODULE' not in os.environ or os.environ['DJANGO_SETTINGS_MODULE'].endswith('settings'):
    from .dev import *
else:
    if os.environ['DJANGO_SETTINGS_MODULE'].endswith('dev'):
        from .dev import *
    elif os.environ['DJANGO_SETTINGS_MODULE'].endswith('prod'):
        from .prod import *
    else:
        print(os.environ['DJANGO_SETTINGS_MODULE'])
        assert False 