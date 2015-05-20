# coding: utf-8
from django.conf import settings

CURRENT_THEME = getattr(settings, 'CURRENT_THEME', None)
DEFAULT_THEME = getattr(settings, 'DEFAULT_THEME', None)
