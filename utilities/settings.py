from django.conf import settings

ALLOW_DOT_IS_USERNAME = getattr(settings, 'ALLOW_DOT_IS_USERNAME', True)
