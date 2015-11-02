from django.conf import settings

ENABLE_PASSWORD_RESET = getattr(settings, 'ENABLE_PASSWORD_RESET', False)
